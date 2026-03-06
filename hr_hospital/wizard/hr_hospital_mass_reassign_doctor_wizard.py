from datetime import datetime
from odoo import fields, models

class  HrHospitalMassReassignDoctorWizard(models.TransientModel):
    """
        Wizard для масового перепризначення пацієнтів іншому лікарю.

        Дозволяє адміністраторам швидко перемістити всіх пацієнтів
        від одного лікаря до іншого з автоматичним створенням історії змін.
    """
    _name = 'hr.hospital.mass.reassign.doctor'
    _description = 'HR Hospital Mass Reassign Doctor'

    change_date = fields.Date(string='Date of change',default=datetime.today())
    reason = fields.Text(string='Reason', required=True)

    previous_doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='Previous Doctor')
    new_doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='New Doctor',required=True)
    patient_ids = fields.Many2many(comodel_name='hr.hospital.patient', string='Patients', domain="[('doctor_id', '=', previous_doctor_id)]")

