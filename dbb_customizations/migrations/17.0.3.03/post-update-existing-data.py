# documentation from https://odoo-development.readthedocs.io/en/latest/maintenance/data-migration.html


def migrate(cr, version):
    # Drop columns for removed fields
    cr.execute("UPDATE res_country SET active=false WHERE code NOT IN ('NL', 'DE', 'SP', 'FR', 'US', 'GB', 'IT', 'LU', 'PT', 'BE', 'AT', 'SE', 'CH', 'FI', 'NO', 'DK')")
    cr.execute("UPDATE res_country SET sequence=1 WHERE code = 'NL'")
    cr.execute("UPDATE res_country SET sequence=2 WHERE code = 'DE'")
    cr.execute("UPDATE res_country SET sequence=3 WHERE code = 'BE'")
    cr.execute("UPDATE res_country SET sequence=4 WHERE code = 'FR'")
    cr.execute("UPDATE res_country SET sequence=5 WHERE code = 'SP'")
