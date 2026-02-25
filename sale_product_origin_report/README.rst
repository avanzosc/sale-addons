.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==========================
Sale Product Origin Report
==========================

This module extends sale quotation/order reports and adds product extra information
to each regular sale order line:

* Product name as line title (first line only)
* Product origin from sales description (``description_sale``)
* Optional external product URL (if available and valid)

Behavior
========

* The product name is shown in the Description column.
* If a valid product URL exists, product name is shown as a clickable link.
* If product sales description exists, it is shown below as ``Origin: ...``.
* Invalid URL placeholders such as ``0.0`` are ignored.
* If URL/origin do not exist, report remains unchanged for that line.

Compatibility
=============

URL lookup is compatible with these optional modules:

* ``product_variant_url`` (``external_url``)
* ``website_sale_product_external_link`` (``website_link``)

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* AvanzOSC

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
