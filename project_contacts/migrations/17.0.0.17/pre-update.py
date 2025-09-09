# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    cr.execute('ALTER TABLE project_project DROP COLUMN IF EXISTS lang')
