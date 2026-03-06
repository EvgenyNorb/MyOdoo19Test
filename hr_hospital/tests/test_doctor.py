from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from datetime import date, timedelta

@tagged('post_install', '-at_install','doctor')
class TestHrHospitalDoctor(TransactionCase):

    def setUp(self):
        super(TestHrHospitalDoctor, self).setUp()

        # Створюємо спеціальність
        self.speciality = self.env['hr.hospital.doctor.speciality'].create({
            'name': 'Cardiology',
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

        doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Jane',
            'last_name': 'Doe',
            'speciality_id': self.speciality.id,
            'date_of_birth': date.today() - timedelta(days=365 * 30),  # 30 років
        })

        # Перевіряємо, що вік розрахувався правильно
        self.assertEqual(doctor.age, 30, "Age should be calculated as 30")
