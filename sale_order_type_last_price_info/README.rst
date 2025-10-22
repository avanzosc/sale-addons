.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Sale order type last price info
===============================

Sale order type defines how unit price of products should be determined. 

Key Features
============

- Adds new field **Sale Price Type** on `sale.order.type` with the following options:
  - **Last Sale Price** → Uses the last sale price of the product for the customer.
  - **Last Invoice Price** → Uses the last invoiced price of the product for the customer.
  - **Sale Pricelist** → Uses the standard pricelist logic (default behavior).

- Extends `sale.order.line` to:
  - Automatically update the `price_unit` when the product, quantity, or UoM changes, based on the selected sale price type.
  - React to changes in the fields `sale_last_price_unit` and `invoice_last_price_unit`.
  - Ensure that when these last price fields are updated, the `price_unit` is synchronized accordingly.

- Provides a view extension to display the **Sale Price Type** field in the Sale Order Type form.

Usage
=====

1. Go to **Sales → Configuration → Sale Order Types**.
2. Select or create a Sale Order Type.
3. Choose the **Sale Price Type**:
   - *Last Sale Price*
   - *Last Invoice Price*
   - *Sale Pricelist*
4. When creating a Sale Order with this type:
   - The unit price of order lines will be automatically set according to the chosen type.

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
~~~~~~~~~~~~

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
