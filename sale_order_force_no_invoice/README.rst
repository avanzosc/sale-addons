.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===========================
Sale Order Force No Invoice
===========================

This module allows forcing the invoice status of a sale order to
"Nothing to Invoice", even if there are order lines or quantities still
pending invoicing.

The standard ``invoice_status`` field on ``sale.order`` is computed and
stored, so it cannot be set directly. This module adds a boolean field,
``Force Nothing to Invoice``, and extends the computation so that, when
checked, the order's invoice status is always set to "Nothing to Invoice"
regardless of the state of its lines.

**Usage**

#. Open a sale order.
#. Go to the *Other Info* tab, *Invoicing* section.
#. Check the *Force Nothing to Invoice* field.
#. The order's *Invoice Status* is recomputed to "Nothing to Invoice" and
   the order stops appearing in the "To Invoice" / "Orders to Invoice"
   filters and views.
#. Unchecking the field restores the standard computation.

Note: this only affects the order's invoice status. It does not prevent
invoicing the pending quantity if a user manually creates an invoice from
the order.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
