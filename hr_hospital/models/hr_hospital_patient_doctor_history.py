from odoo import models , fields

class HrHospitalPatientDoctorHistory(models.Model):
    _name = 'hr.hospital.patient.doctor.history'
    _description = 'Hospital Patient Doctor History'

    name = fields.Char(string='Name')

    appointment_date = fields.Date(string='Appointment Date', required=True,default=fields.Date.today())
    change_data = fields.Date(string='Change Data')
    change_reason = fields.Text(string='Change Reason')
    is_active = fields.Boolean(string='Is Active', default=True)

    patient_id = fields.Many2one(comodel_name='hr.hospital.patient', string='Patient')
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='Doctor')

    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        help='Doctor assigned after the change'
    )

    def create(self, vals_list):
        """При створенні нового запису - деактивувати попередній"""
        # Створюємо новий запис
        records = super(HrHospitalPatientDoctorHistory, self).create(vals_list)

        # Для кожного створеного запису
        for record in records:
            # Шукаємо попередні активні записи цього пацієнта (крім поточного)
            previous_histories = self.search([
                ('patient_id', '=', record.patient_id.id), # type: ignore
                ('is_active', '=', True),
                ('id', '!=', record.id),
            ])

            # Деактивуємо їх
            if previous_histories:
                previous_histories.write({'is_active': False})

        return records




