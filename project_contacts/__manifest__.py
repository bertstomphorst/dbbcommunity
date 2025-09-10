# -*- coding: utf-8 -*-

{
    'name': 'Project Contacts',
    'category': 'Services/Project',
    'version': '17.0.1.03',
    'author': 'Advisto, Bert Stomphorst',
    'website': 'https://www.advisto.nl',
    'summary': """ Link projects and contacts together. 
    Multiple contacts linked to a single project, and multiple projects to a single contact.
    Projects are reachable by a smartbutton from contact-form. """,
    'depends': [
        'base',
        "project",
    ],
    'data': [
        'views/project_project.xml',
        'views/res_partner.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': True,
}
