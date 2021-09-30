# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged
from odoo import fields


@tagged("post_install", "-at_install")
class TestSaleExpenseFromAnalytic(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleExpenseFromAnalytic, cls).setUpClass()
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product = cls.env['product.product'].create({
            'name': 'Product Sale Expense From Analytic',
            'default_code': 'PSEFA',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service',
            'can_be_expensed': True})
        vals = {'name': 'User Sale Expense From Analytic',
                'login': 'usersaleexpensefromanalytic@avanzosc.es'}
        cls.user = cls.env['res.users'].create(vals)
        vals = {'name': 'Employee Sale Expense From Analytic',
                'user_id': cls.user.id}
        cls.employee = cls.env['hr.employee'].create(vals)
        cls.analytic_account = cls.env['account.analytic.account'].create({
            'name': 'Analytic Account For Event With Expense',
            'partner_id': cls.user.partner_id.id})
        cls.sale = cls.env['sale.order'].search([], limit=1)

    def test_sale_expense_from_analytic(self):
        vals = {
            'account_id': self.analytic_account.id,
            'name': 'Analytic Line Sale Expense From Analytic',
            'date': fields.Date.today(),
            'amount': 222,
            'partner_id': self.user.partner_id.id,
            'product_id': self.product.id}
        analytic_line = self.env['account.analytic.line'].with_context(
            default_sale_order_id=self.sale).create(vals)
        cond = [('name', '=', analytic_line.name),
                ('date', '=', analytic_line.date),
                ('quantity', '=', 1),
                ('product_id', '=', self.product.id),
                ('employee_id', '=', self.employee.id),
                ('sale_order_id', '=', self.sale.id)]
        hr_expense = self.env['hr.expense'].search(cond, limit=1)
        self.assertEqual(len(hr_expense), 1)
