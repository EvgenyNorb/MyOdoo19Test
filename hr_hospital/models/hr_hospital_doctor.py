
from odoo import models , fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = 'hr.hospital.abstract.person'

    name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)

    license_number = fields.Char(string='Licence Number',copy= False)
    license_date = fields.Date(string='Licence Date')
    active = fields.Boolean(string='Active', default=True)

    patient_ids = fields.One2many(comodel_name='hr.hospital.patient',inverse_name='doctor_id',string='Patients')
    user_id = fields.Many2one(comodel_name='res.users',string='User')
    speciality_id = fields.Many2one(comodel_name='hr.hospital.doctor.speciality',string='Speciality')
    doctor_schedule_ids = fields.One2many(comodel_name='hr.hospital.doctor.schedule', inverse_name='doctor_id', string='Doctor Schedule')
    Country_of_study_id = fields.Many2one(comodel_name='res.country',string='Country of Study')

    filtered_doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        compute='_compute_filtered_doctors',
        store=False,
        string='Filtered Doctors'
    )

    # Поля що обчислюються
    experience_years = fields.Integer(string='Experience Years',compute='_compute_experience_years')


    # Поля що валідуються
    is_intern = fields.Boolean(default=False, string='Is Intern')
    doc_mentor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string=' Mentor Doctor',
                                    domain=[('is_intern', '=', False)])

    rating = fields.Float(string='Rating',digits=(3, 2),default=0.0)

    filter_study_country_id = fields.Many2one(
        'res.country',
        string='Filter by Study Country',
        store=False,
        help='Select country to filter doctors'
    )


     # Заборона архівування лікарів з активними візитами
    def write(self, vals):
        if 'active' in vals and not vals['active']:
            for record in self:
                # Шукаємо активні візити
                active_visits = self.env['hr.hospital.visit'].search([
                    ('doctor_id', '=', record.id),
                    ('visit_status', 'in', ['scheduled', 'completed'])  # Активні статуси
                ])

                if active_visits:
                    raise UserError(
                        "Неможливо архівувати лікаря '{}'!\n"
                        "Лікар має {} активних візитів. "
                        "Спочатку скасуйте або завершіть всі візити.".format(
                            record.name,
                            len(active_visits)
                        )
                    )

        return super(HrHospitalDoctor, self).write(vals)


    #  SQL обеження

    _sql_constraints = [

        # Унікальний номер ліцензії

        ('unique_license_number','UNIQUE(license_number)',
         'Ліцензійний номер має бути унікальний!'),

        # діапазон рейтингу від 0.00 до 5.00

        ('rating_range',
         'CHECK(rating >= 0.0 AND rating <= 5.0)',
         'Рейтинг має бути в діапазоні від 0.00 до 5.00!'),
    ]

    # Зберемо повне ім'я
    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_full_name(self):
        for record in self:
            parts = [record.first_name, record.last_name] # type: ignore
            if record.middle_name: # type: ignore
                parts.insert(1, record.middle_name) # type: ignore
            record.full_name = ' '.join(filter(None, parts))

    # Відображати "Ім'я (Спеціальність)

    def name_get(self):
        result = []
        for record in self:
            # Отримуємо базове ім'я
            base_name = record.name if record.name else 'Doctor #{}'.format(record.id)

            # Формуємо повне відображення
            if record.speciality_id and record.speciality_id.name: # type: ignore
                display_name = '{} ({})'.format(base_name, record.speciality_id.name) # type: ignore
            else:
                display_name = base_name
            result.append((record.id, display_name))
        return result


    # Вираховуємо кількість років досвіду від дати видачі ліцензії
    @api.depends('license_date')
    def _compute_experience_years(self):
        today = date.today()
        for record in self:
            if record.license_date:
                record.experience_years = relativedelta(today, record.license_date).years # type: ignore
            else:
                record.experience_years = 0

    @api.depends('filter_study_country_id')
    def _compute_filtered_doctors(self):
        for record in self:
            if record.filter_study_country_id:
                doctors = self.env['hr.hospital.doctor'].search([
                    ('Country_of_study_id', '=', record.filter_study_country_id.id)
                ])
                record.filtered_doctor_ids = doctors
            else:
                # Якщо фільтр порожній - показуємо всіх
                record.filtered_doctor_ids = self.env['hr.hospital.doctor'].search([])


    # Якщо не інтерн то ментора бути не повинно
    @api.constrains('is_intern', 'doc_mentor_id')
    def _check_mentor(self):
        for record in self:
            if record.doc_mentor_id and not record.is_intern:
                raise ValidationError("Ментор може бути призначений лише інтернам!")


    # # Рейтинг має бути в діапазоні 0.0 до 5.0
    # @api.constrains('rating')
    # def _check_rating(self):
    #     for record in self:
    #         if record.rating < 0.0 or record.rating > 5.0:
    #             raise ValidationError("Рейтинг має бути в діапазоні від 0.00 до 5.00!")


    # Прибераємо ментора, якщо це не інтерн
    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.doc_mentor_id = False


    #  Перевірка що лікар не може бути сам собі ментором.
    @api.constrains('doc_mentor_id')
    def _check_mentor_not_self(self):
        for record in self:
            if record.doc_mentor_id and record.doc_mentor_id.id == record.id: # type: ignore
                raise ValidationError(
                    "Лікар не може бути ментором самому собі!"
                )