# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Islamic Date Picker',
    'version': '15.0.1.2',
    'category': 'General',
    'description': """Islamic Date Picker""",
    'summary': 'As its name suggest and we all know that Islamic date picker follows Hijri Calendar which is achieved by this module | Islamic Date | Date Picker | Islamic Calendar | islamic date | date picker | islamic calendar',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['web'],
    'data': [
        'view/islamic_calendar_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'islamic_calendar/static/src/scss/web_hijri_date.scss',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.picker.css',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.plugin.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.plus.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.picker.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.islamic.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.islamic-ar.js',
            'islamic_calendar/static/src/lib/jQuery_calendars/jquery.calendars.islamic-fa.js',
            'islamic_calendar/static/src/js/islamic_calendar.js',
        ],
        'web.assets_qweb': [
            'islamic_calendar/static/src/xml/*.xml',
        ]
    },
    'images': ['static/description/main_screenshot.jpg'],
    'installable': True,
    'price': 50,
    'currency': 'EUR',
}
