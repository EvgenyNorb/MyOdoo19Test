from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from datetime import date, timedelta

@tagged('post_install', '-at_install','patient')
class TestHrHospitalPatient(TransactionCase):

    def setUp(self):
        super(TestHrHospitalPatient, self).setUp()

        self.speciality = self.env['hr.hospital.doctor.speciality'].create({
            'name': 'General Practice',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Doctor',
            'last_name': 'Test',
            'speciality_id': self.speciality.id,
            'date_of_birth': date.today() - timedelta(days=365 * 45),
        })


    # Тест підрахунку кількості візитів пацієнта
    def test_01_compute_visit_count(self):

        patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'One',
            'date_of_birth': date.today() - timedelta(days=365 * 30),
            'doctor_id': self.doctor.id,
        })

        # Створюємо 3 візити
        for i in range(3):
            self.env['hr.hospital.visit'].create({
                'patient_id': patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_datatime': date.today() + timedelta(days=i),
            })

        # Перевіряємо підрахунок
        self.assertEqual(patient.visit_count, 3, "Patient should have 3 visits")
