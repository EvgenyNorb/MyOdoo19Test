from odoo import fields, models, api

class HrHospitalContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _description = 'HR Hospital Contact Person'
    _inherit = 'hr.hospital.abstract.person'

    name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)

    description = fields.Char(string='Note')

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        domain="[('allergy', '!=', False)]"
    )

    # Зберемо повне ім'я
    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_full_name(self):
        for record in self:
            parts = [record.first_name, record.last_name]
            if record.middle_name:
                parts.insert(1, record.middle_name)
            record.full_name = ' '.join(filter(None, parts))

