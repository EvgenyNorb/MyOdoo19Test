from odoo import models , fields


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'HR Hospital Patient'

    name = fields.Char(string='Name',required=True)
    # patient_id = fields.Many2one(comodel_name='hr.hospital.patient',string='Patient')
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Doctor')
    disease_ids = fields.One2many(comodel_name='hr.hospital.disease',string='disease',inverse_name='patient_id')

