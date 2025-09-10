from . import models
from odoo.addons.sale_expense.models.account_move_line import AccountMoveLine

# Bewaar de originele methode
original_method = AccountMoveLine._sale_create_reinvoice_sale_line


def new_sale_create_reinvoice_sale_line(self):
    expensed_lines = self.filtered('expense_id')
    res = super(AccountMoveLine, self - expensed_lines)._sale_create_reinvoice_sale_line()
    # Change ten opzichte van sale_expense\models\account_move_line.py#_sale_create_reinvoice_sale_line:
    # force_split_lines naar False ipv True
    res.update(super(AccountMoveLine, expensed_lines.with_context({'force_split_lines': False}))._sale_create_reinvoice_sale_line())
    return res


# Vervang de methode
AccountMoveLine._sale_create_reinvoice_sale_line = new_sale_create_reinvoice_sale_line
