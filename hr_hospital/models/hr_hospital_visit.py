
from odoo import models , fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class HrHospitalVisit(models.Model):
    """
        Модель для управління візитами пацієнтів до лікарів.

        Відстежує заплановані та завершені візити, включаючи
        статус, вартість, рекомендації та зв'язок з діагнозами.
    """

    _name = 'hr.hospital.visit'
    _description = 'HR Hospital Visit'

    name = fields.Char(string='Name')

    visit_status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('did_not_show_up', 'Did Not Show Up'),
    ], default='scheduled', string='Visit Status')

    scheduled_datatime = fields.Datetime(string='Scheduled Datatime')
    visit_datetime = fields.Datetime(string='Visit Date', readonly=True)

    type_visit = fields.Selection([
        ('primary','Primary'),
        ('repeat','Repeat'),
        ('preventive','Preventive'),
        ('unpreventive','Unpreventive')
    ],default='primary', string='Visit Type')

    medical_diagnosis_ids = fields.One2many(comodel_name='hr.hospital.medical.diagnosis', inverse_name='visit_id',string='Medical Diagnosis')
    recommendations = fields.Html(string='Recommendations')

    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    visit_cost = fields.Monetary(string='Visit Cost',currency_field='currency_id')

    patient_id = fields.Many2one(comodel_name='hr.hospital.patient',string='Patient',required=True)
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Doctor',required=True,domain=[('license_number', '!=', False)])

    specialty_id = fields.Many2one(comodel_name='hr.hospital.doctor.speciality', string='Required Specialty')

    available_doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        compute='_compute_available_doctors',
        store=False
    )

    # Поля що обчислюються
    diagnosis_count = fields.Integer(
        string='Diagnosis Count',
        compute='_compute_diagnosis_count',
        store=True  # Зберігати в БД для швидкого пошуку
    )

    # Перевизначаю метод - заборона видалення візитів + перевірка чи є діагноз.

    def unlink(self):
        for record in self:
            if record.medical_diagnosis_ids:
                raise UserError(
                    "Неможливо видалити візит '{}'!\n"
                    "Візит має {} діагноз(ів). "
                    "Спочатку видаліть всі діагнози.".format(
                        record.name,
                        len(record.medical_diagnosis_ids)
                    )
                )
        return super(HrHospitalVisit, self).unlink()

    def write(self, vals):
        for record in self:
            if record.visit_status == 'completed':
                # Перевірка полів
                forbidden_fields = ['doctor_id', 'scheduled_datatime', 'visit_datetime']
                changed_fields = [field for field in forbidden_fields if field in vals]

                if changed_fields:
                    raise UserError(
                        "Неможливо змінити візит '{}'!\n"
                        "Візит вже відбувся (статус: Завершено).\n"
                        "Заборонено змінювати: лікаря, дату або час візиту.".format(
                            record.name
                        )
                    )

        return super(HrHospitalVisit, self).write(vals)



    @api.depends('medical_diagnosis_ids')
    def _compute_diagnosis_count(self):
        for record in self:
            record.diagnosis_count = len(record.medical_diagnosis_ids)



    @api.depends('specialty_id', 'scheduled_datatime')
    def _compute_available_doctors(self):
        for record in self:
            domain = []

            # Фільтр за спеціальністю
            if record.specialty_id:
                domain.append(('speciality_id', '=', record.specialty_id.id))

            # Фільтр за розкладом (якщо є дата)
            if record.scheduled_datatime:
                # Знаходимо лікарів які працюють в цей день/час
                weekday = record.scheduled_datatime.weekday()
                weekday_map = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

                schedules = self.env['hr.hospital.doctor.schedule'].search([
                    ('week_day', '=', weekday_map[weekday]),
                    ('date', '=', record.scheduled_datatime.date()),
                ])

                if schedules:
                    domain.append(('id', 'in', schedules.mapped('doctor_id').ids))

            record.available_doctor_ids = self.env['hr.hospital.doctor'].search(domain)


    # перевіряємо статус, накидуємо або зануляємо дату
    @api.onchange('visit_status')
    def _onchange_visit_datetime(self):
        if self.visit_status == 'completed':
            self.visit_datetime = fields.Datetime.now()
        else:
            self.visit_datetime = False


    # Автоматично заповнюємо ментора
    # @api.onchange('doctor_id')
    # def _onchange_doctor_mentor(self):
    #     if self.doctor_id and self.doctor_id.is_intern: # type: ignore
    #
    #         self.mentor_doctor_id = self.doctor_id.doc_mentor_id # type: ignore
    #
    #         # Опціонально: показати інформацію
    #         if self.doctor_id.doc_mentor_id: # type: ignore
    #             return {
    #                 'warning': {
    #                     'title': 'Інформація',
    #                     'message': 'Лікар {} є інтерном. Ментор: {}'.format(
    #                         self.doctor_id.name, # type: ignore
    #                         self.doctor_id.doc_mentor_id.name # type: ignore
    #                     ),
    #                 }
    #             }
    #         return {}
    #     return {}

    @api.onchange('doctor_id')
    def _onchange_doctor_mentor(self):
        """Показати попередження якщо обрано лікаря-інтерна"""
        if self.doctor_id and self.doctor_id.is_intern: # type: ignore
            mentor = self.doctor_id.doc_mentor_id # type: ignore
            if mentor:
                return {
                    'warning': {
                        'title': 'Увага! Лікар-інтерн',
                        'message': 'Обраний лікар {} є інтерном.\nМентор: {}'.format(
                            self.doctor_id.name, # type: ignore
                            mentor.name
                        ),
                    }
                }
            else:
                return {
                    'warning': {
                        'title': 'Увага!',
                        'message': 'Обраний лікар {} є інтерном без призначеного ментора!'.format(
                            self.doctor_id.name # type: ignore
                        ),
                    }
                }
        return {}


        # показувати алергію при виборі паціента
    @api.onchange('patient_id')
    def _onchange_patient_allergy_warning(self):
        if self.patient_id and self.patient_id.allergy: # type: ignore
            return {
                'warning': {
                    'title': 'Увага! Алергії',
                    'message': 'У пацієнта {} є алергії:\n{}'.format(
                        self.patient_id.name, # type: ignore
                        self.patient_id.allergy # type: ignore
                    ),
                }
            }
        return {}

    #  Повертає повідомлення про доступні дні"
    @api.onchange('doctor_id')
    def _onchange_doctor_available_dates(self):
        if self.doctor_id: # type: ignore
            schedules = self.env['hr.hospital.doctor.schedule'].search([
                ('doctor_id', '=', self.doctor_id.id)
            ])

            available_days = schedules.mapped('week_day')

            if available_days:
                return {
                    'warning': {
                        'title': 'Available Days',
                        'message': 'Doctor works on: {}'.format(', '.join(available_days)),
                    }
                }
        return {}


    # Перевірка на дубль, що б в один день не було ще одного візита до одного лікаря від пацієнта

    @api.constrains('patient_id', 'doctor_id', 'scheduled_datatime')
    def _check_one_visit_per_day(self):
        for record in self:
            # Перевіримо на заповненність
            if not (record.patient_id and record.doctor_id and record.scheduled_datatime):
                continue

            visit_date = record.scheduled_datatime.date()


            date_start = datetime.combine(visit_date, datetime.min.time())
            date_end = datetime.combine(visit_date, datetime.max.time())

            # Перевірка на дубль
            duplicate = self.search([
                ('patient_id', '=', record.patient_id.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('scheduled_datatime', '>=', date_start),
                ('scheduled_datatime', '<=', date_end),
                ('id', '!=', record.id),
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    "Пацієнт '{}' вже записаний до лікаря '{}' на {}!\n"
                    "Неможливо записати одного пацієнта до одного лікаря "
                    "більше одного разу на день.".format(
                        record.patient_id.name,         # type: ignore
                        record.doctor_id.name,              # type: ignore
                        visit_date.strftime('%d.%m.%Y')
                    )
                )

    @api.constrains('scheduled_datatime')
    def _check_scheduled_datetime(self):
        """
        Валідує що дата візиту не в минулому.

        Перевіряє що заплановані візити мають дату в майбутньому.

        :raises ValidationError: Якщо дата візиту раніше поточного часу
        :return: None
        """
        for visit in self:
            if visit.scheduled_datatime and visit.scheduled_datatime < datetime.now():
                raise ValidationError(
                    "Scheduled date cannot be in the past!"
                )