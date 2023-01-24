# -*- coding: utf-8 -*-
{
    'name': "Arab states HR",

    'summary': """
        Hr Module For Arab states """,

    'description': """
        This modules contains all features such as iqama, nationality etc features
    """,

    'author': "SolutionFounder",
    'website': "http://www.kyan_it.com",
    'version': '14.0.1.11',
    'category': 'hr',
    'depends': ['base', 'hr','account','hr_contract', 'notify_inbox','hr_employee_updation','hr_holidays'],
    'data': [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/schedule.xml',
        'views/hr_contract_ext_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_iqama_view.xml',
        'views/hr_passport_view.xml',
        'views/hr_doc_type.xml',
        'views/hr_insurance_view.xml',
        'views/hr_employee_access.xml',
        'views/hr_education_type.xml',
        'views/hr_access_type.xml',
        'views/hr_nationality_detail.xml',
        'views/hr_id_type.xml',
        'views/hr_employee_banks.xml',
        'views/reference_letter_bank.xml',
        'views/hr_sponsor.xml',
        'views/hr_config.xml',
        'mail_format/probation_contract.xml',
        'mail_format/iqama_expire.xml',
        'mail_format/insurance_expire.xml',
        'mail_format/passport_expire.xml',
        'views/hr_policies.xml',
        'views/hr_leaves.xml',
        'views/hr_grading.xml',
        'views/hr_job_view.xml',
    ],
}
