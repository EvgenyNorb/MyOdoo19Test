import re
from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class HrHospitalAbstractPerson(models.AbstractModel):
    _name = 'hr.hospital.abstract.person'
    _description = 'HR Hospital Abstract Person'
    _inherit = ['image.mixin']

    name = fields.Char(string='Name')

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    middle_name = fields.Char(string='Middle Name')

    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'),('Other', 'Other')],default='Other',string='Gender')
    date_of_birth = fields.Date(string='Date of Birth')
    country_citizenship_id = fields.Many2one(comodel_name='res.country', string='Country Citizenship')
    language_id = fields.Many2one(comodel_name='res.lang', string='Language')

    # Поля що обчислюються
    full_name = fields.Char(string='Full Name',compute='_compute_full_name')
    age = fields.Integer(string='Age',compute='_compute_age')

    # Поля що валідуються
    telephone = fields.Char(string='Telephone',size=16)
    email = fields.Char(string='Email')

    # збираємо повне ім'я з перевіркою на заповненність поля middle_name , так як воно не обов'язкове
    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            if record.middle_name:
                record.full_name = record.first_name + ' ' + record.middle_name + ' ' + record.last_name # type: ignore
            else:
                record.full_name = record.first_name + ' ' + record.last_name # type: ignore


    # Рахуємо скількі років з перевіркою на заповненність поля date_of_birth , так як воно не обов'язкове
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                record.age = relativedelta(today, record.date_of_birth).years # type: ignore
            else:
                record.age = 0  # ← ДОБАВИТЬ!


    @api.constrains('email')
    def _email_validation(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.email:
                if not re.match(email_pattern, record.email): # type: ignore
                    raise ValidationError("Не вірний формат email: {}".format(record.email))


    @api.constrains('telephone')
    def _telephone_validation(self):
        for record in self:
            if record.telephone:
                # Прибераємо все, окрім цифр та +
                phone_clean = re.sub(r'[^\d+]', '', record.telephone) # type: ignore

                # Проверяем формат
                # Должен начинаться с + и содержать 10-15 цифр
                if not re.match(r'^\+\d{10,15}$', phone_clean):
                    raise ValidationError(
                        "Невірний формат телефона, має бути +3801234567 : {}".format(phone_clean))












