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
        'security/ir.model.access.csv',
        'views/hr_hospital_menu.xml',
        'data/disease_data.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
    ],
    'demo': [
        'demo/hr.hospital.doctor.csv',  # 1. Сначала докторов
        'demo/hr.hospital.patient.csv',  # 2. Потом пациентов (они ссылаются на докторов)
        'demo/hr.hospital.disease.csv',  # 3. В конце болезни (они ссылаются на пациентов)
    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.jpg'
    ],
}