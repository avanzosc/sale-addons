.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Sale Final Customer Address
===========================

* Adds a boolean field "Final customer" on delivery addresses (contacts with
  type "Delivery Address").
* Adds a boolean field "Ship to final customer" on Sales Orders.
* When enabled, the shipping address field only shows delivery addresses with
  "Final customer" enabled.
* When disabled, it only shows delivery addresses with "Final customer"
  disabled.
* When creating a new delivery address from the Sales Order, the default value
  for "Final customer" follows the Sales Order checkbox.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Eñaut Alberdi <enautavanzosc@gmail.com>
