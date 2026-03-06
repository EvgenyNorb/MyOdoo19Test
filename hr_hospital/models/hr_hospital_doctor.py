
from odoo import models , fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class HrHospitalDoctor(models.Model):
    """
       Модель для управління лікарями та медичним персоналом.

       Ця модель зберігає інформацію про лікарів, включаючи їх особисті дані,
       спеціалізації, кваліфікації, та відносини ментор-інтерн.
    """

    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = 'hr.hospital.abstract.person'

    license_number = fields.Char(string='Licence Number',copy= False)
    license_date = fields.Date(string='Licence Date')
    active = fields.Boolean(string='Active', default=True)

    patient_ids = fields.One2many(comodel_name='hr.hospital.patient',inverse_name='doctor_id',string='Patients')
    user_id = fields.Many2one(comodel_name='res.users',string='Related User',help='Link doctor to system user for access rights')
    speciality_id = fields.Many2one(comodel_name='hr.hospital.doctor.speciality',string='Speciality')
    doctor_schedule_ids = fields.One2many(comodel_name='hr.hospital.doctor.schedule', inverse_name='doctor_id', string='Doctor Schedule')
    Country_of_study_id = fields.Many2one(comodel_name='res.country',string='Country of Study')
    intern_ids = fields.One2many(comodel_name='hr.hospital.doctor',inverse_name='doc_mentor_id',string='Interns',help='Doctors mentored by this doctor')


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
        comodel_name='res.country',
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
                            record.name,  # type: ignore
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


    # Відображати "Ім'я (Спеціальність)

    def name_get(self):
        result = []
        for record in self:
            # Отримуємо базове ім'я
            base_name = record.name if record.name else 'Doctor #{}'.format(record.id) # type: ignore

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

    # для звітів
    # Повертає історію візитів до лікаря
    def get_doctor_visits_history(self):

        self.ensure_one()
        return self.env['hr.hospital.visit'].search(domain=[
            ('doctor_id', '=', self.id)
        ], order='scheduled_datatime desc')  # Найновіші зверху


    # Повертає пацієнтів з інформацією про останній візит
    def get_doctor_patients_with_status(self):

        self.ensure_one()

        # Знаходимо всіх пацієнтів лікаря
        patients = self.env['hr.hospital.patient'].search([
            ('doctor_id', '=', self.id)
        ])

        result = []
        for patient in patients:
            # Знаходимо останній візит пацієнта до цього лікаря
            last_visit = self.env['hr.hospital.visit'].search(domain=[
                ('patient_id', '=', patient.id),
                ('doctor_id', '=', self.id)
            ], order='scheduled_datatime desc', limit=1)

            result.append({
                'patient': patient,
                'visit_status': last_visit.visit_status if last_visit else False, # type: ignore
                'visit_date': last_visit.scheduled_datatime if last_visit else False, # type: ignore
            })

        return result