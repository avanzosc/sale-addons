.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Sale Order Line Endesa
======================

Track the deliveries of the sale orders of Endesa customers on the sale order
lines themselves: Endesa code, status, ID, serial number and need date of each
line, together with its manufacturing orders.

Key features
============

* **Endesa** checkbox on customers (*Sales & Purchase* tab). It is set on the
  company: its contacts follow it.
* On sale orders of Endesa customers:

  * **Endesa** tab with the contract (*Source Document*) and the Endesa order
    (*Customer Reference*).
  * Endesa columns in the order lines: Endesa code, need date, review,
    S/N, Endesa status (PDP / PDI / CSV / QA) and Endesa ID.

* **Endesa Deliveries** menu: the lines (quotations and sale orders) of
  Endesa customers, except those of cancelled orders and of services, with
  the same columns as the former Endesa deliveries table:

  * From the order and its lines: sales order, description, quantity,
    delivered quantity, destination (delivery address), product, internal
    reference, contract, Endesa order and planned date (*Delivery Date* of the
    order).
  * From the manufacturing orders of the line: all of them, and the
    manufacturing date (latest end date). They are the manufacturing orders
    its stock moves come from (make to order), and the ones with the line as
    *Origin sale order line*.
  * The need date is red if it is due, orange if it is due in 7 days or less
    and yellow in 15 days or less (not for QA lines). Only in this list.

  Only the Endesa fields can be edited there; the rest follow the sale order,
  the line and the manufacturing orders. The sales order, destination, product
  and each manufacturing order open their form, and each row opens its line.
* Changing the need date marks the line to review.

Configuration
=============

* **Endesa Deliveries / User**: sees the Endesa deliveries and fields.
* **Endesa Deliveries / Manager**: also edits the Endesa fields.

These groups only give read access to sale orders, sale order lines and
manufacturing orders. To open the forms of sale orders and manufacturing
orders, users also need access to Sales and Manufacturing.

Usage / How to test
===================

1. Mark a customer as **Endesa** in its form.
2. Create a sale order for it: the **Endesa** tab and the Endesa columns of
   the lines appear.
3. Go to **Endesa Deliveries**, edit the Endesa fields of a line and open its
   sales order or manufacturing orders from the list.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical
issues.

Credits
=======

Contributors
------------

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
