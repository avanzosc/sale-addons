# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    fnames = [
        "qty_pending_delivery",
        "qty_pending_invoicing",
        "amount_pending_delivery",
        "amount_pending_invoicing",
        "qty_shipped_pending_invoicing",
        "amount_shipped_pending_invoicing",
    ]
    records = env["sale.order.line"].search([])
    if records:
        for fname in fnames:
            env.add_to_compute(records._fields[fname], records)
        records.modified(fnames)
