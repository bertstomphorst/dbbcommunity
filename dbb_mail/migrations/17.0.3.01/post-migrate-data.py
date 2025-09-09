# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    # Drop columns for removed fields
    cr.execute("UPDATE mail_message SET fetchmail_server_id = 1 WHERE original_to_email LIKE '%info@dbbtexel.nl%'")
    cr.execute("UPDATE mail_message SET fetchmail_server_id = 2 WHERE original_to_email LIKE '%info@winkelhartvantexel.nl%'")

