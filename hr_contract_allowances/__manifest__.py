# -*- coding: utf-8 -*-
{'name': "Employee Contract Allowances/Deductions ",
 'summary': """
       Multiple Allowances/Deductions for employee""",
 'description': """
            Add many allowances/deductions to any employee, include in payroll and END of Service Reward calculation
    """,
 'author': "KyanIt",
 'website': "http://www.Kyanit.com",
 'email': "info@ivalue-s.com",
 'license': "OPL-1",
 'category': 'HR',
 'version': '14.0.1.10',
 'images': ['static/description/Banner.png'],
 'depends': ['base', 'mail', 'hr_contract', 'hr_payroll','hr_work_entry_contract_enterprise'],
 'data': [
    'data/data.xml',
    'data/contract_deduction_seq.xml',
    'data/contract_allowance_seq.xml',
    'security/ir.model.access.csv',
    'views/hr_allowance_views.xml',
    'views/hr_deduction_views.xml',
    'views/hr_contract_views.xml',
    'views/contract_deduction.xml',
    'views/contract_allowance.xml',
    'views/deduction_payslip_view.xml',
    'views/hr_employee.xml',
 ],
 'demo': []
 }
