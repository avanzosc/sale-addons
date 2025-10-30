.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================
Sale Order Return
=================

Return quantities management directly from the sale order lines.  
Allows users to register and control product returns while preventing inconsistencies between pending deliveries and returns.

Key Features
============

- Add new field **“Return Qty”** (`return_qty`) in the Sale Order Lines.
- Prevents returns if:
  - The order is not confirmed or done.
  - There are pending delivery pickings.
  - The order type or return type is not configured.
- Prevents deliveries if:
  - There are pending return pickings.
- Automatically creates or updates a **return picking** when a valid return quantity is entered.
- Blocks decreasing the return quantity once some quantities have already been returned.
- Adds computed flags at order level:
  - `pending_returns`: Indicates if there are pending return pickings.
  - `pending_deliveries`: Indicates if there are pending delivery pickings.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
