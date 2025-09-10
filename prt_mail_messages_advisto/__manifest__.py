# -*- coding: utf-8 -*-

{
    'name': 'Mail Messages Easy - Advisto aanpassingen',
    'category': 'Discuss',
    'version': '17.0.0.1.01',
    'author': 'Advisto, Bert Stomphorst',
    'website': 'https://www.advisto.nl',
    'summary': """ Aanpassingen op Mail Messages Easy """,
    'depends': [
        'prt_mail_messages_pro',
    ],
    'data': [
        'views/mail_message_views.xml',

        'wizard/mail_message_composer.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'auto_install': True,
}
