# -*- coding: utf-8 -*-

{
    'name': 'DBB Texel - Mail',
    'category': 'Marketing',
    'version': '17.0.4.09',
    'author': 'Advisto, Bert Stomphorst',
    'website': 'https://www.advisto.nl',
    'summary': """ Aanpassingen t.b.v. mailen met huisstijl namens verschillende bedrijven """,
    'depends': [
        'base',
        "mass_mailing",
        "prt_mail_messages_advisto",
    ],
    'data': [
        'data/bulkmail_templates.xml',

        'views/mail.xml',
        'views/mail_message_views.xml',
        'views/mailing_mailing.xml',
        'views/res_company.xml',

        'wizard/mail_message_composer.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dbb_mail/static/src/*',
        ]
    },
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'auto_install': True,
}
