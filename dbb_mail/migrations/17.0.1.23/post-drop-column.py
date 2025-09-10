# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    # Drop columns for removed fields
    cr.execute('ALTER TABLE res_company DROP COLUMN IF EXISTS x_dbb_mail_bulk_template_id')
