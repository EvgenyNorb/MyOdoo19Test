from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrHospitalRescheduleVisitWizard(models.TransientModel):
    _name = 'hr.hospital.reschedule.visit.wizard'
    _description = 'Reschedule Visit Wizard'

    current_visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Current Visit',
        readonly=True,
        required=True
    )

    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor'
    )

    new_date = fields.Date(
        string='New Date',
        required=True
    )

    new_time = fields.Float(
        string='New Time',
        required=True,
        help='Time in hours (e.g., 14.5 for 14:30)'
    )

    reason = fields.Text(
        string='Reason for Rescheduling',
        required=True
    )

    # Відображення інформації про поточний візит
    current_patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        related='current_visit_id.patient_id',
        readonly=True
    )

    current_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Current Doctor',
        related='current_visit_id.doctor_id',
        readonly=True
    )

    current_date = fields.Datetime(
        string='Current Date',
        related='current_visit_id.scheduled_datatime',
        readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        """Автоматично заповнюємо поточний візит з контексту"""
        res = super(HrHospitalRescheduleVisitWizard, self).default_get(fields_list)

        # Отримуємо ID візиту з контексту
        visit_id = self.env.context.get('active_id')
        if visit_id:
            visit = self.env['hr.hospital.visit'].browse(visit_id)
            res['current_visit_id'] = visit_id
            # За замовчуванням залишаємо того самого лікаря
            res['new_doctor_id'] = visit.doctor_id.id # type: ignore
            # За замовчуванням завтрашня дата
            if visit.scheduled_datatime: # type: ignore
                from datetime import timedelta
                new_datetime = visit.scheduled_datatime + timedelta(days=1) # type: ignore
                res['new_date'] = new_datetime.date()
                res['new_time'] = new_datetime.hour + new_datetime.minute / 60.0

        return res

    @api.constrains('new_time')
    def _check_time(self):
        """Перевірка що час в робочому діапазоні"""
        for wizard in self:
            if wizard.new_time < 0 or wizard.new_time >= 24:
                raise ValidationError("Час має бути від 0.0 до 23.99!")

    def action_reschedule(self):
        """Перенесення візиту"""
        self.ensure_one()

        from datetime import datetime, timedelta

        # Формуємо нову дату і час
        hours = int(self.new_time)
        minutes = int((self.new_time - hours) * 60)
        new_datetime = datetime.combine(
            self.new_date, # type: ignore
            datetime.min.time()
        ) + timedelta(hours=hours, minutes=minutes)

        # Скасовуємо старий візит
        self.current_visit_id.write({
            'visit_status': 'cancelled',
        })

        # Створюємо новий візит
        new_visit = self.env['hr.hospital.visit'].create([{
            'name': 'Rescheduled from {}'.format(self.current_visit_id.name),  # type: ignore
            'patient_id': self.current_visit_id.patient_id.id,  # type: ignore
            'doctor_id': self.new_doctor_id.id if self.new_doctor_id else self.current_visit_id.doctor_id.id,  # type: ignore
            'scheduled_datatime': new_datetime,
            'visit_status': 'scheduled',
            'type_visit': self.current_visit_id.type_visit,  # type: ignore
            'recommendations': 'Rescheduled. Reason: {}'.format(self.reason),
        }])

        # Відкриваємо новий візит
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'res_id': new_visit.id,
            'view_mode': 'form',
            'target': 'current',
        }

