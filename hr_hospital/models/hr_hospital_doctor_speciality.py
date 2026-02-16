from odoo import fields,models

class HrHospitalDoctorSpeciality(models.Model):
    _name = 'hr.hospital.doctor.speciality'
    _description = 'Hospital Doctor Speciality'
    _order = 'name'

    name = fields.Char(string='Name',required=True)

    specialty_code = fields.Char(string='Special Code',required=True,size=10)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)

    doctor_ids = fields.One2many(comodel_name='hr.hospital.doctor',inverse_name='speciality_id',string='Doctors')
