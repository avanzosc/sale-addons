# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class ProcurementException(Exception):
    """An exception raised by ProcurementGroup `run` containing all the faulty
    procurements.
    """

    def __init__(self, procurement_exceptions):
        """:param procurement_exceptions: a list of tuples containing the faulty
        procurement and their error messages
        :type procurement_exceptions: list
        """
        self.procurement_exceptions = procurement_exceptions


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def run(self, procurements, raise_user_error=True):
        result = super(ProcurementGroup, self).run(procurements, raise_user_error)

        def raise_exception(procurement_errors):
            if raise_user_error:
                dummy, errors = zip(*procurement_errors)
                raise UserError("\n".join(errors))
            else:
                raise ProcurementException(procurement_errors)

        actions_to_run = defaultdict(list)
        procurement_errors = []
        for procurement in procurements:
            procurement.values.setdefault(
                "company_id", procurement.location_id.company_id
            )
            procurement.values.setdefault("priority", "0")
            procurement.values.setdefault("date_planned", fields.Datetime.now())
            if float_is_zero(
                procurement.product_qty,
                precision_rounding=procurement.product_uom.rounding,
            ):
                rule = self._get_rule(
                    procurement.product_id, procurement.location_id, procurement.values
                )
                if not rule:
                    error = _(
                        'No rule has been found to replenish "%s" in "%s".\n'
                        "Verify the routes configuration on the product."
                    ) % (
                        procurement.product_id.display_name,
                        procurement.location_id.display_name,
                    )
                    procurement_errors.append((procurement, error))
                else:
                    action = "pull" if rule.action == "pull_push" else rule.action
                    actions_to_run[action].append((procurement, rule))
                if procurement_errors:
                    raise_exception(procurement_errors)
                for action, procurements in actions_to_run.items():
                    if hasattr(self.env["stock.rule"], "_run_%s" % action):
                        try:
                            getattr(self.env["stock.rule"], "_run_%s" % action)(
                                procurements
                            )
                        except ProcurementException as e:
                            procurement_errors += e.procurement_exceptions
                    else:
                        _logger.error(
                            "The method _run_%s doesn't exist on the procurement rules"
                            % action
                        )
                if procurement_errors:
                    raise_exception(procurement_errors)
        return result
