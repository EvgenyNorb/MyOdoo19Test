from datetime import timedelta

from odoo import models, fields, api


class HrHospitalMedicalDiagnosis(models.Model):
    _name = 'hr.hospital.medical.diagnosis'
    _description = 'Hospital Medical Diagnosis'

    name = fields.Char(string='Medical Diagnosis')
    description_disease = fields.Text(string='Medical Diagnosis')
    prescribed_treatment = fields.Html(string='Prescribed Treatment')
    approved = fields.Boolean(string='Approved',default=False)
    doctor_approved_id = fields.Many2one(comodel_name='hr.hospital.doctor',string='Approved',readonly=True)
    approved_datetime = fields.Datetime(string='Approved Date',readonly=True)

    severity = fields.Selection([
        ('light','Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
        ('critical', 'Critical'),
    ],string='Severity',default='light')


    visit_id = fields.Many2one(comodel_name='hr.hospital.visit',string='Visit',domain=lambda self: self._get_recent_completed_visits_domain())
    disease_id = fields.Many2one(comodel_name='hr.hospital.disease', string='Disease',domain="[('is_contagious', '=', True), ('danger_level', 'in', ['high', 'critical'])]")

    @api.model
    def _get_recent_completed_visits_domain(self):
        date_30_days_ago = fields.Date.today() - timedelta(days=30)
        return [
            ('visit_status', '=', 'completed'),
            ('visit_datetime', '>=', date_30_days_ago)
        ]

    # Поля що обчислюються

    # Поля що валідуються

    # Автоматичне затвердження при призначенні ментора
    def write(self, vals):
        """При затвердженні діагнозу ментором - оновлювати поля"""
        # Якщо призначається лікар-затверджувач
        if 'doctor_approved_id' in vals and vals['doctor_approved_id']:
            # Автоматично встановлюємо затвердження
            vals['approved'] = True
            vals['approved_datetime'] = fields.Datetime.now()

        # Якщо прибирають лікаря-затверджувача
        if 'doctor_approved_id' in vals and not vals['doctor_approved_id']:
            # Скидаємо затвердження
            vals['approved'] = False
            vals['approved_datetime'] = False

        return super(HrHospitalMedicalDiagnosis, self).write(vals)

   # def action_approved(self):
   #     for rec in self:
   #         if rec.is_approved:
   #             raise UserError(_("Diagnosis is already approved."))
   #
   #     current_doctor = self.env['hr.hospital.doctor'].search(
   #         [('user_id', '=', self.env.user.id)], limit=1
   #     )
   #
   #     if not current_doctor:
   #         raise UserError(_("Your user is not linked to any Doctor profile."))
   #
   #     rec.write({
   #         'is_approved': True,
   #         'approved_by_id': current_doctor.id,
   #         'approved_date': fields.Datetime.now()
   #     })



