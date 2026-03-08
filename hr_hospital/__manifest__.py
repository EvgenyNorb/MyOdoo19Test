{
    'name': 'HR Hospital',
    'version': '19.0.1.0.0',
    'author': 'Evgeny Lyalin',
    'website': 'https://odoo.school',
    'category': 'Customizations',
    'license': 'OPL-1',
    'depends': [
        'base'
    ],
    'external_dependencies': {
        'python': []
    },
    'data': [
        'security/hr_hospital_security.xml',
        'security/ir.model.access.csv',
        'views/hr_hospital_menu.xml',
        'data/disease_data.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/medical_diagnosis_views.xml',
        'views/doctor_speciality_views.xml',
        'views/doctor_schedule_views.xml',
        'views/patient_doctor_history_views.xml',
        'wizard/hr_hospital_mass_reassign_doctor_wizard.view.xml',
        'wizard/hr_hospital_disease_report_wizard.view.xml',
        'wizard/hr_hospital_reschedule_visit_wizard.view.xml',
        'wizard/hr_hospital_doctor_schedule_wizard.view.xml',
        'wizard/hr_hospital_patient_card_export_wizard.view.xml',
        'reports/doctor_report_template.xml',
    ],
    'demo': [
        'demo/hr.hospital.doctor.speciality.csv',  # 1. Базова довідкова (немає залежностей)
        'demo/hr.hospital.doctor.csv',  # 2. Лікарі (залежать від speciality)
        'demo/hr.hospital.patient.csv',  # 3. Пацієнти (залежать від doctor)
        'demo/hr.hospital.contact.person.csv',  # 4. Контакти (залежать від patient)
        'demo/hr.hospital.disease.csv',  # 5. Хвороби (залежать від patient)
        'demo/hr.hospital.doctor.schedule.csv',  # 6. Розклад (залежить від doctor)
        'demo/hr.hospital.visit.csv',  # 7. Візити (залежать від patient + doctor)
        'demo/hr.hospital.medical.diagnosis.csv',  # 8. Діагнози (залежать від visit + disease)
        'demo/hr.hospital.patient.doctor.history.csv',  # 9. Історія (залежить від patient + doctor)
    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.jpg'
    ],
}