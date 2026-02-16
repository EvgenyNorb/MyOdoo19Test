from odoo import fields,models


class HrHospitalDoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'HR Hospital Doctor Schedule'

    name = fields.Char(string='Name',required=True)

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Doctor',required=True,domain="[('speciality_id', '!=', False)]")

    week_day = fields.Selection([
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday')
    ],string='Weekday',default='Monday')

    date = fields.Datetime(string='Date')
    start_time = fields.Float(string='Start Time')
    end_time = fields.Float(string='End Time')

    type = fields.Selection([
        ('working_day','Working Day'),
        ('vacation','Vacation'),
        ('sick','Sick'),
        ('conference','Conference')
    ],string='Type',default='working_day')

    notes = fields.Char(string='Notes')

    #  SQL обеження

    _sql_constraints = [

        # Час закінчення візиту має бути більшим за час початку.

        ('check_time_range',
         'CHECK(end_time > start_time)',
         'Час закінчення має бути пізніше часу початку!'),
    ]


