# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    # Drop columns for removed fields
    cr.execute("UPDATE res_country SET active=false, sequence=99 WHERE code NOT IN ('NL', 'DE', 'ES', 'FR', 'US', 'GB', 'IT', 'LU', 'PT', 'BE', 'AT', 'SE', 'CH', 'FI', 'NO', 'DK')")
    cr.execute("UPDATE res_country SET active=false, sequence=10 WHERE code IN ('NL', 'DE', 'ES', 'FR', 'US', 'GB', 'IT', 'LU', 'PT', 'BE', 'AT', 'SE', 'CH', 'FI', 'NO', 'DK')")
    cr.execute("UPDATE res_country SET sequence=1 WHERE code = 'NL'")
    cr.execute("UPDATE res_country SET sequence=2 WHERE code = 'DE'")
    cr.execute("UPDATE res_country SET sequence=3 WHERE code = 'BE'")
    cr.execute("UPDATE res_country SET sequence=4 WHERE code = 'FR'")
    cr.execute("UPDATE res_country SET sequence=5 WHERE code = 'ES'")

    cr.execute('ALTER TABLE res_country DROP COLUMN IF EXISTS active')

    cr.execute('ALTER TABLE res_partner DROP COLUMN IF EXISTS x_dbb_bungalownummer')
