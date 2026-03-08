from odoo.tests.common import TransactionCase
from datetime import date, timedelta
# from odoo.tests import tagged

# @tagged('post_install', '-at_install','doctor')
class TestHrHospitalDoctor(TransactionCase):

    def setUp(self):
        super(TestHrHospitalDoctor, self).setUp()

        # Створюємо спеціальність
        self.speciality = self.env['hr.hospital.doctor.speciality'].create({
            'name': 'Cardiology',
            'specialty_code': 'CARD',
        })

        # Створюємо ментора
        self.mentor = self.env['hr.hospital.doctor'].create({
            'first_name': 'John',
            'last_name': 'Smith',
            'speciality_id': self.speciality.id,
            'date_of_birth': date.today() - timedelta(days=365 * 50),
            'is_intern': False,
        })


    # Тест розрахунку віку лікаря
    def test_01_compute_age(self):
        """Тест розрахунку віку лікаря"""
        # Використовуємо точну дату
        birth_date = date(1996, 3, 8)

        doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Jane',
            'last_name': 'Doe',
            'speciality_id': self.speciality.id,
            'date_of_birth': birth_date,
        })

        # Перевіряємо, що вік розрахувався правильно
        self.assertEqual(doctor.age, 30, "Age should be calculated as 30")
