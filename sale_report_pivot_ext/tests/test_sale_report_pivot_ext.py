# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleReportPivotExt(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleReportPivotExt, cls).setUpClass()
        cls.report_model = cls.env['sale.report']

    def test_sale_line_pending_info(self):
        res = self.report_model._query(
            with_clause='', fields=None, groupby='', from_clause='')
        self.assertIn(
            ', s.commitment_date_without_hour as commitment_date', res)
        self.assertIn('s.id , s.commitment_date_without_hour', res)
