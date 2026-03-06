from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

@tagged('post_install', '-at_install','visit')
class TestHrHospitalVisit(TransactionCase):

    def setUp(self):
        super(TestHrHospitalVisit, self).setUp()

        self.speciality = self.env['hr.hospital.doctor.speciality'].create({
            'name': 'Pediatrics',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Doctor',
            'last_name': 'Visit',
            'speciality_id': self.speciality.id,
            'date_of_birth': datetime.today() - timedelta(days=365 * 40),
        })

        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'Visit',
            'date_of_birth': datetime.today() - timedelta(days=365 * 20),
            'doctor_id': self.doctor.id,
        })


    # Тест валідації: дата візиту не може бути в минулому
    def test_01_validate_scheduled_datetime_in_past(self):
        past_date = datetime.now() - timedelta(days=1)

        with self.assertRaises(ValidationError, msg="Should not allow past scheduled datetime"):
            self.env['hr.hospital.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_datatime': past_date,
            })
