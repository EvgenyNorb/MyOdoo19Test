from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class HrHospitalDoctorScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='Doctor', required=True)

    start_week = fields.Date(string='Start Week', required=True, default=fields.Date.context_today)
    week_count = fields.Integer(string='Number of Weeks', default=1, required=True)

    schedule_type = fields.Selection([
        ('standard', 'Standard'),
        ('even_week', 'Even Week'),
        ('odd_week', 'Odd Week'),
    ], string='Schedule Type', default='standard', required=True)

    # Дні тижня
    is_monday = fields.Boolean(string='Monday', default=True)
    is_tuesday = fields.Boolean(string='Tuesday', default=True)
    is_wednesday = fields.Boolean(string='Wednesday', default=True)
    is_thursday = fields.Boolean(string='Thursday', default=True)
    is_friday = fields.Boolean(string='Friday', default=True)
    is_saturday = fields.Boolean(string='Saturday', default=False)
    is_sunday = fields.Boolean(string='Sunday', default=False)

    # Робочі години
    start_time = fields.Float(string='Start Time', required=True, default=9.0)
    end_time = fields.Float(string='End Time', required=True, default=18.0)

    # Перерва
    break_start = fields.Float(string='Break Start', default=13.0)
    break_end = fields.Float(string='Break End', default=14.0)

    @api.constrains('week_count')
    def _check_week_count(self):
        for wizard in self:
            if wizard.week_count < 1 or wizard.week_count > 52:
                raise ValidationError("Кількість тижнів має бути від 1 до 52!")

    @api.constrains('start_time', 'end_time', 'break_start', 'break_end')
    def _check_times(self):
        for wizard in self:
            if wizard.start_time >= wizard.end_time:
                raise ValidationError("Час початку має бути раніше часу закінчення!")

            if wizard.break_start and wizard.break_end:
                if wizard.break_start >= wizard.break_end:
                    raise ValidationError("Час початку перерви має бути раніше часу закінчення перерви!")

                if wizard.break_start < wizard.start_time or wizard.break_end > wizard.end_time:
                    raise ValidationError("Перерва має бути в межах робочого часу!")

    def action_generate_schedule(self):
        """Генерація розкладу"""
        self.ensure_one()

        # Перевірка що обрано хоч один день
        if not any([self.is_monday, self.is_tuesday, self.is_wednesday, self.is_thursday,
                    self.is_friday, self.is_saturday, self.is_sunday]):
            raise ValidationError("Оберіть хоча б один день тижня!")

        # Мапа днів
        weekday_map = {
            0: ('monday', self.is_monday),
            1: ('tuesday', self.is_tuesday),
            2: ('wednesday', self.is_wednesday),
            3: ('thursday', self.is_thursday),
            4: ('friday', self.is_friday),
            5: ('saturday', self.is_saturday),
            6: ('sunday', self.is_sunday),
        }

        schedule_records = []
        current_date = self.start_week

        # Генеруємо розклад для кожного тижня
        for week_num in range(self.week_count):
            # Визначаємо чи парний/непарний тиждень
            week_number = current_date.isocalendar()[1]
            is_even_week = week_number % 2 == 0

            # Пропускаємо тиждень якщо не підходить за типом
            if self.schedule_type == 'even_week' and not is_even_week:
                current_date += timedelta(days=7)
                continue
            elif self.schedule_type == 'odd_week' and is_even_week:
                current_date += timedelta(days=7)
                continue

            # Генеруємо для кожного дня тижня
            for day_offset in range(7):
                date = current_date + timedelta(days=day_offset)
                weekday = date.weekday()
                day_name, is_selected = weekday_map[weekday]

                if is_selected:
                    # Ранкова зміна (до перерви)
                    if self.break_start and self.break_end:
                        schedule_records.append({
                            'name': '{} - {} (Morning)'.format(
                                self.doctor_id.name, # type: ignore
                                date.strftime('%d.%m.%Y')
                            ),
                            'doctor_id': self.doctor_id.id,
                            'date': date,
                            'start_time': self.start_time,
                            'end_time': self.break_start,
                            'week_day': day_name,
                        })

                        # Вечірня зміна (після перерви)
                        schedule_records.append({
                            'name': '{} - {} (Afternoon)'.format(
                                self.doctor_id.name, # type: ignore
                                date.strftime('%d.%m.%Y')
                            ),
                            'doctor_id': self.doctor_id.id,
                            'date': date,
                            'start_time': self.break_end,
                            'end_time': self.end_time,
                            'week_day': day_name,
                        })
                    else:
                        # Повний день без перерви
                        schedule_records.append({
                            'name': '{} - {}'.format(
                                self.doctor_id.name, # type: ignore
                                date.strftime('%d.%m.%Y')
                            ),
                            'doctor_id': self.doctor_id.id,
                            'date': date,
                            'start_time': self.start_time,
                            'end_time': self.end_time,
                            'week_day': day_name,
                        })

            current_date += timedelta(days=7)

        # Створюємо записи розкладу
        if schedule_records:
            self.env['hr.hospital.doctor.schedule'].create(schedule_records)

        # Повідомлення про успіх
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success!',
                'message': 'Created {} schedule records for {}'.format(
                    len(schedule_records),
                    self.doctor_id.name # type: ignore
                ),
                'type': 'success',
                'sticky': False,
            }
        }