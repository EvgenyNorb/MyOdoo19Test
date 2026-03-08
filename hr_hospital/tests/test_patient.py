# from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from datetime import date, timedelta, datetime


# @tagged('post_install', '-at_install','patient')
class TestHrHospitalPatient(TransactionCase):

    def setUp(self):
        super(TestHrHospitalPatient, self).setUp()

        self.speciality = self.env['hr.hospital.doctor.speciality'].create({
            'name': 'General Practice',
            'specialty_code': 'GP',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Doctor',
            'last_name': 'Test',
            'speciality_id': self.speciality.id,
            'date_of_birth': date.today() - timedelta(days=365 * 45),
        })

    def test_01_compute_visit_count(self):
        """Тест підрахунку кількості візитів пацієнта"""
        patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'One',
            'date_of_birth': date.today() - timedelta(days=365 * 30),
            'doctor_id': self.doctor.id,
            'blood_type': '1',
        })

        # Створюємо 3 візити
        for i in range(3):
            self.env['hr.hospital.visit'].create({
                'patient_id': patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_datatime': datetime.now() + timedelta(days=i + 1),
            })

        # Перевіряємо підрахунок
        self.assertEqual(patient.visit_count, 3, "Patient should have 3 visits")

    def test_02_action_view_visits(self):
        """Тест методу відкриття візитів пацієнта"""
        patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'Two',
            'date_of_birth': date.today() - timedelta(days=365 * 25),
            'doctor_id': self.doctor.id,
            'blood_type': '2',
        })
        # ... решта коду

    def test_03_action_create_visit(self):
        """Тест методу швидкого створення візиту"""
        patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'Three',
            'date_of_birth': date.today() - timedelta(days=365 * 35),
            'doctor_id': self.doctor.id,
            'blood_type': '3',
        })
