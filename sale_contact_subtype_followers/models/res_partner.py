# Copyright 2026 Alfredo de la fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models

from odoo.addons.base.models.res_partner import Partner as BaseResPartner


class ResPartner(models.Model):
    _inherit = "res.partner"

    def address_get_override_no_assign_subtype_contact(self, adr_pref=None):
        """
        Reemplaza el funcionamiento de base del método "address_get" de forma
        que siempre se retorne el mismo contacto original.

        :param adr_pref: Listado de direcciones a buscar, defaults to None
        :type adr_pref: set[str], optional
        :returns dict[int] Diccionario con el conjunto de direcciones y su
               correspondiente dirección (en este caso, siempre `self.id`).
        """
        result = dict()
        adr_pref = set(adr_pref or [])

        if "contact" not in adr_pref:
            adr_pref.add("contact")

        for address_type in adr_pref:
            result[address_type] = self.id

        return result


# XXX: Override del método para respetar herencias.
BaseResPartner.address_get = ResPartner.address_get_override_no_assign_subtype_contact
