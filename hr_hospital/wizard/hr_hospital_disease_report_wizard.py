
from odoo import fields, models , api
from odoo.exceptions import ValidationError

class  HrHospitalDiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'HR hospital disease report wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    report_type = fields.Selection([
        ('detailed', 'Detailed'),
        ('summary', 'Summary'),
    ], string='Report Type', default='detailed', required=True)

    group_by = fields.Selection([
        ('doctor', 'By Doctor'),
        ('disease', 'By Disease'),
        ('month', 'By Month'),
        ('country', 'By Country'),
    ], string='Group By', default='doctor')

    doctor_ids = fields.Many2many(comodel_name='hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many(comodel_name='hr.hospital.disease', string='Diseases')
    country_ids = fields.Many2many(comodel_name='res.country', string='country')

    # Валідація дат
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from > wizard.date_to: # type: ignore
                raise ValidationError(
                    "Дата початку не може бути пізніше дати закінчення!"
                )

    def action_generate_report(self):
        """Генерація звіту по діагнозах"""
        self.ensure_one()

        # Будуємо domain для пошуку
        domain = [
            ('visit_id.visit_datetime', '>=', self.date_from),
            ('visit_id.visit_datetime', '<=', self.date_to),
        ]

        # Якщо вибрані лікарі - фільтруємо, інакше - всі лікарі
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))  # type: ignore

        # Якщо вибрані хвороби - фільтруємо, інакше - всі хвороби
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids)) # type: ignore

        # Якщо вибрані країни - фільтруємо за пацієнтами з цих країн
        if self.country_ids:
            patients = self.env['hr.hospital.patient'].search([
                ('country_citizenship_id', 'in', self.country_ids.ids)
            ])
            if patients:
                domain.append(('visit_id.patient_id', 'in', patients.ids)) # type: ignore
            else:
                # Якщо немає пацієнтів з цих країн - порожній результат
                domain.append(('id', '=', False))

        # Шукаємо діагнози за критеріями
        diagnoses = self.env['hr.hospital.medical.diagnosis'].search(domain)

        # Формуємо назву вікна
        title = 'Disease Report: {} to {}'.format(
            self.date_from.strftime('%d.%m.%Y'),
            self.date_to.strftime('%d.%m.%Y')
        )

        # Відкриваємо список діагнозів
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.medical.diagnosis',
            'view_mode': 'list,form',
            'domain': [('id', 'in', diagnoses.ids)],
            'context': {
                'group_by': self._get_group_by_field(),
            },
        }

    def _get_group_by_field(self):
        group_by_map = {
            'doctor': 'doctor_id',  # <-- ВАЖНО
            'disease': 'disease_id',
            'month': 'visit_id.visit_datetime:month',
            'country': 'country_id',  # создадим отдельное поле
        }
        return group_by_map.get(self.group_by) # type: ignore



