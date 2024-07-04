.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Sale Order Basket Type Depending on Number
==========================================

This module enhances Odoo's sales order functionality by introducing computed fields and categorization based on basket types (closed, expanded, open).

Features
--------

- **Basket Field**: Adds a boolean field `is_basket` to product templates to mark items as baskets.
  
- **Basket Line Calculation**: Computes the number of basket and non-basket lines in each sales order.
  
- **Basket Type Classification**: Automatically categorizes sales orders into three types based on their line composition:

  - **Closed**: Orders that exclusively contain basket items.
  - **Expanded**: Orders that include both basket and non-basket items.
  - **Open**: Orders without any basket items.

Bug Tracker
===========

Issues and bugs can be reported on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`. Please check if your issue has already been reported before creating a new one. Your feedback and suggestions are valuable for improving this module.

Contributors
============

Contributions to this module have been made by:

- Unai Beristain <unaiberistain@avanzosc.es>
