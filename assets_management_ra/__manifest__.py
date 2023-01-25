# -*- coding: utf-8 -*-

{
    'name': "Assets Management Ext",
    'author': 'raheel',
    'category': 'assets',
    'summary': """customization in manintenance and equipments""",
    'website': 'http://www.raheel aslam.com',
    'description': """
""",
    'version': '15.0.1.0',
    'depends': ['base','web','hr','maintenance'],
    'data': ['security/ir.model.access.csv',
             'views/maintenance_equipment.xml',
             'views/branch_name.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
