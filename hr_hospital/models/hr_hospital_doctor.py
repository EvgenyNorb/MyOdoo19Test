from odoo import models , fields


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name',required=True)
    # doc_id = fields.Many2one('hr.hospital.doctor',string='Doctor')
    patient_ids = fields.One2many(comodel_name='hr.hospital.patient',inverse_name='doctor_id',string='Patients')
