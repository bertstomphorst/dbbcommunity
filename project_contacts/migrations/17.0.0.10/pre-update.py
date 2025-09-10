# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    cr.execute('DROP TABLE project_project_res_partner_category_rel')
