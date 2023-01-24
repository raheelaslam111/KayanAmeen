# -*- coding: utf-8 -*-
{
    'name': "Notify Inbox",
    'summary': """Send Inbox Notification""",
    'description': """Send Inbox Notification Based On Odoo mail.message""",
    'author': 'SolutionFounder',
    'website': "http://www.solutionfounder.com",
    'category': 'Discuss',
    'version': '12.0.0.30',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False
}
