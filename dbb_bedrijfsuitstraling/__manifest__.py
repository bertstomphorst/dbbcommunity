# -*- coding: utf-8 -*-

{
    'name': 'DBB Texel - Bedrijfsuitstraling',
    'category': 'Marketing',
    'version': '17.0.2.08',
    'author': 'Advisto, Bert Stomphorst',
    'website': 'https://www.advisto.nl',
    'summary': """ Layouts van documenten en mails voor DBB Texel """,
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'reports/external_layout.xml',
        'reports/invoice_document.xml',

        'views/res_company.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'auto_install': True,
}
