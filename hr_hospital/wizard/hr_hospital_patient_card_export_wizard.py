from odoo import fields, models, api
from odoo.exceptions import ValidationError
import json
import base64
from io import StringIO
import csv


class HrHospitalPatientCardExportWizard(models.TransientModel):
    _name = 'hr.hospital.patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(comodel_name='hr.hospital.patient', string='Patient', required=True)

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    is_include_diagnoses = fields.Boolean(string='Include Diagnoses', default=True)
    is_include_recommendations = fields.Boolean(string='Include Recommendations', default=True)

    language_id = fields.Many2one(comodel_name='res.lang', string='Report Language')

    export_format = fields.Selection([
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ], string='Export Format', default='json', required=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_from > wizard.date_to: # type: ignore
                raise ValidationError("Дата початку не може бути пізніше дати закінчення!")

    @api.model
    def default_get(self, fields_list):
        res = super(HrHospitalPatientCardExportWizard, self).default_get(fields_list)

        patient_id = self.env.context.get('active_id')
        if patient_id:
            res['patient_id'] = patient_id

        return res

    def _get_patient_data(self):
        """Збираємо дані пацієнта"""
        self.ensure_one()

        domain = [('patient_id', '=', self.patient_id.id)]

        if self.date_from:
            domain.append(('scheduled_datatime', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_datatime', '<=', self.date_to))

        visits = self.env['hr.hospital.visit'].search(domain, order='scheduled_datatime desc')

        patient_data = {
            'patient': {
                'name': self.patient_id.name, # type: ignore
                'date_of_birth': str(self.patient_id.date_of_birth) if self.patient_id.date_of_birth else '', # type: ignore
                'gender': self.patient_id.gender, # type: ignore
                'blood_type': dict(self.patient_id._fields['blood_type'].selection).get(self.patient_id.blood_type, ''), # type: ignore
                'email': self.patient_id.email or '', # type: ignore
                'phone': self.patient_id.telephone or '', # type: ignore
            },
            'visits': []
        }

        for visit in visits:
            visit_data = {
                'date': str(visit.scheduled_datatime), # type: ignore
                'doctor': visit.doctor_id.name, # type: ignore
                'status': visit.visit_status, # type: ignore
                'type': visit.type_visit, # type: ignore
            }

            if self.is_include_recommendations and visit.recommendations: # type: ignore
                visit_data['recommendations'] = visit.recommendations # type: ignore

            if self.is_include_diagnoses and visit.medical_diagnosis_ids: # type: ignore
                visit_data['diagnoses'] = []
                for diagnosis in visit.medical_diagnosis_ids: # type: ignore
                    diag_data = {
                        'name': diagnosis.name,
                        'disease': diagnosis.disease_id.name if diagnosis.disease_id else '',
                        'severity': diagnosis.severity,
                        'treatment': diagnosis.prescribed_treatment or '',
                        'approved': diagnosis.approved,
                    }
                    visit_data['diagnoses'].append(diag_data)

            patient_data['visits'].append(visit_data)

        return patient_data

    def action_export_json(self):
        """Експорт в JSON"""
        self.ensure_one()

        data = self._get_patient_data()
        json_data = json.dumps(data, indent=2, ensure_ascii=False)

        filename = 'patient_card_{}.json'.format(self.patient_id.id)

        attachment = self.env['ir.attachment'].create([{
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(json_data.encode('utf-8')),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/json',
        }])

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment.id),
            'target': 'self',
        }

    def action_export_csv(self):
        """Експорт в CSV"""
        self.ensure_one()

        data = self._get_patient_data()

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(['Patient Name', self.patient_id.name]) # type: ignore
        writer.writerow(['Date of Birth', data['patient']['date_of_birth']])
        writer.writerow(['Gender', data['patient']['gender']])
        writer.writerow(['Blood Type', data['patient']['blood_type']])
        writer.writerow([])
        writer.writerow(['Visits'])
        writer.writerow(['Date', 'Doctor', 'Status', 'Type', 'Diagnoses', 'Recommendations'])

        for visit in data['visits']:
            diagnoses_text = ''
            if self.is_include_diagnoses and 'diagnoses' in visit:
                diagnoses_text = '; '.join([d['name'] for d in visit['diagnoses']]) # type: ignore

            recommendations_text = visit.get('recommendations', '') if self.is_include_recommendations else ''

            writer.writerow([
                visit['date'], # type: ignore
                visit['doctor'], # type: ignore
                visit['status'], # type: ignore
                visit['type'], # type: ignore
                diagnoses_text,
                recommendations_text,
            ])

        csv_data = output.getvalue()
        filename = 'patient_card_{}.csv'.format(self.patient_id.id)

        attachment = self.env['ir.attachment'].create([{
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(csv_data.encode('utf-8')),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'text/csv',
        }])

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment.id),
            'target': 'self',
        }

    def action_export(self):
        """Експорт в обраному форматі"""
        self.ensure_one()

        if self.export_format == 'json':
            return self.action_export_json()
        else:
            return self.action_export_csv()