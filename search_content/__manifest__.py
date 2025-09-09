# -*- coding: utf-8 -*-

{
    'name': 'Search content',
    'category': 'Productivity/Discuss',
    'version': '17.0.1.09',
    'author': 'Advisto, Bert Stomphorst',
    'website': 'https://www.advisto.nl',
    'summary': """ Makes all notes, e-mails and documents in your Odoo-database searchable (by content) and clickable to navigate to corresponding object. """,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'views/menu.xml',
        'views/mail_message.xml',
        'views/attachment.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': True,
}
