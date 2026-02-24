from odoo import fields, models

class HrHospitalContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _description = 'HR Hospital Contact Person'
    _inherit = 'hr.hospital.abstract.person'


    description = fields.Char(string='Note')

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        domain="[('allergy', '!=', False)]"
    )

