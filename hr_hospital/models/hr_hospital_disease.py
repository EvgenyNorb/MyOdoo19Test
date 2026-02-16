from odoo import models,fields

class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'HR Hospital Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    parent_path = fields.Char(index=True)

    name = fields.Char(string='Name',required=True)
    description = fields.Char(string='Description',required=True)

    code_MKX_10 = fields.Char(string='Code MKX-10',size=10)
    danger_level = fields.Selection([
        ('low','Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])

    is_contagious = fields.Boolean(string='Contagious')
    symptoms = fields.Text(string='Symptoms')

    patient_id = fields.Many2one(comodel_name='hr.hospital.patient', string='Patient')
    parent_id = fields.Many2one(comodel_name='hr.hospital.disease', string='Parent Disease', index=True)
    child_ids = fields.One2many(comodel_name='hr.hospital.disease', inverse_name='parent_id', string='Child Diseases')
    distribution_region_ids = fields.Many2many(comodel_name='res.country',string='Distribution regions')

