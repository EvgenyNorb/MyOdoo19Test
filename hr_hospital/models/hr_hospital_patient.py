
from odoo import models , fields, api
from odoo.exceptions import ValidationError
import datetime


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'HR Hospital Patient'
    _inherit = 'hr.hospital.abstract.person'

    name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)

    passport_number = fields.Char(string='Passport Number', size=10)
    blood_type = fields.Selection([('1','O(I)'),('2','A(II)'),('3','B(III)'),('4','AB(IV)'),('none','None')], string='Blood Type', default='None')
    allergy = fields.Text(string='Allergy')
    insurance_number = fields.Char(string='Insurance Number')

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Personal Doctor')
    disease_ids = fields.One2many(comodel_name='hr.hospital.disease',string='disease',inverse_name='patient_id')
    contact_person_id = fields.Many2one(comodel_name='hr.hospital.contact.person',string='Contact Person')
    insurance_company_id = fields.Many2one(comodel_name='res.partner',domain=[('is_company', '=', True)],string='Insurance Company')
    patient_doc_history_ids = fields.One2many(comodel_name='hr.hospital.patient.doctor.history',inverse_name='patient_id',string='Patient Doctor History')

    country_language_patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        compute='_compute_filtered_patients',
        store=False
    )

    filter_country_id = fields.Many2one(comodel_name='res.country', string='Filter by Country')
    filter_language = fields.Selection([
        ('uk_UA', 'Ukrainian'),
        ('en_US', 'English'),
        ('de_DE', 'German'),
    ], string='Filter by Language')

    # Автоматичне створення запису в історії при зміні лікаря
    def write(self, vals):
        """"""
        if 'doctor_id' in vals:
            for record in self:
                old_doctor_id = record.doctor_id.id if record.doctor_id else False
                new_doctor_id = vals['doctor_id']

                # Якщо лікар змінився
                if old_doctor_id != new_doctor_id and new_doctor_id:
                    # Створюємо запис в історії (СПИСОК словників!)
                    self.env['hr.hospital.patient.doctor.history'].create([{
                        'name': 'Зміна лікаря - {}'.format(fields.Datetime.now().strftime("%d.%m.%Y %H:%M")),
                        'patient_id': record.id,
                        'doctor_id': new_doctor_id,
                        'appointment_date': fields.Datetime.now(),
                        'change_data': fields.Datetime.now(),
                        'change_reason': 'Автоматична зміна персонального лікаря',
                        'is_active': True,
                    }])

        return super(HrHospitalPatient, self).write(vals)


    # Зберемо повне ім'я
    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_full_name(self):
        for record in self:
            parts = [record.first_name, record.last_name] # type: ignore
            if record.middle_name: # type: ignore
                parts.insert(1, record.middle_name) # type: ignore
            record.full_name = ' '.join(filter(None, parts))


    @api.depends('filter_country_id', 'filter_language')
    def _compute_filtered_patients(self):
        for record in self:
            domain = []

            if record.filter_country_id:
                domain.append(('county_ids', 'in', record.filter_country_id.ids))

            if record.filter_language:
                domain.append(('language_id.code', '=', record.filter_language))

            record.country_language_patient_ids = self.env['hr.hospital.patient'].search(domain)



    # Вік пацієнта не може бути 0
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth >= datetime.date.today(): # type: ignore
                raise ValidationError('Дата паціента не може бути більшою за теперішню')


    @api.onchange('country_citizenship_id')
    def _onchange_country_language(self):
        if self.country_citizenship_id: # type: ignore
            # Мапінг країн на мови (приклад)
            country_language_map = {
                'UA': 'uk_UA',  # Україна → Українська
                'US': 'en_US',  # США → Англійська
                'GB': 'en_GB',  # Великобританія → Англійська
                'DE': 'de_DE',  # Німеччина → Німецька
                'FR': 'fr_FR',  # Франція → Французька
                'PL': 'pl_PL',  # Польща → Польська
            }

            country_code = self.country_citizenship_id.code # type: ignore
            language_code = country_language_map.get(country_code)

            if language_code:
                # Шукаємо мову в системі
                language = self.env['res.lang'].search([
                    ('code', '=', language_code)
                ], limit=1)

                if language:
                    self.language_id = language

    # Кнопка для відкриття форм візитів з відбором по паціенту.
    def action_view_visits(self):
        """Відкриває історію візитів поточного пацієнта"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit History: {}'.format(self.name),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],  # ← Фільтр по поточному пацієнту!
            'context': {
                'default_patient_id': self.id,  # Автопідстановка при створенні
            },
        }

    #  Кнопка для швиткого створення візиту до лікаря.
    def action_create_visit(self):
        """Швидке створення візиту для пацієнта"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'New Visit for {}'.format(self.name),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id if self.doctor_id else False,
            },
        }