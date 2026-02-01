from odoo import models , fields

class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'HR Hospital Visit'

    visit_date = fields.Date(string='Visit Date',required=True)
    patient_id = fields.Many2one(comodel_name='hr.hospital.patient',string='Patient',required=True)
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Doctor',required=True)
    comment = fields.Text(string='Comment')
    