from odoo import models,fields


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'HR Hospital Disease'

    name = fields.Char(string='Name',required=True)
    description = fields.Char(string='Description',required=True)
    patient_id = fields.Many2one(comodel_name='hr.hospital.patient', string='Patient')