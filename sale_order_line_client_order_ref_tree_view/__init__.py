from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_client_ref_in_lines(cr, registry):
    api.Environment(cr, SUPERUSER_ID, {})
    cr.execute(
        """
        UPDATE sale_order_line
        SET client_order_ref = (select sale_order.client_order_ref
                               from sale_order
                               where sale_order.id = order_id)
        """
    )
