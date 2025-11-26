.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Sale Order Usability
====================

This module extends the sale order and sale order line models to allow tracking and filtering lines by the order date.

Key Features
============
- Adds `date_order` field to **Sale Order Lines**, reflecting the parent order's date.
- Shows the order date in **Sale Orders** and **Sale Order Lines** tree views.
- Adds filtering and grouping by order date in the search view of sale order lines.
- Improves search by product or line description, including the `origin` of the order.

Configuration
=============
1. Install the module.
2. Go to **Sales → Orders** and open a quotation or confirmed order.
3. The **Order Date** column will be visible in the list of orders and optionally in lines.
4. Use the search or group by filters in sale order lines to analyze orders by their dates.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <ajuaristio@gmail.com>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Berezi Amubieta <bereziamubieta@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
