
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


====================
Sale Kit Description
====================

Update sale order line description with BOM components.

Description
-----------

This module updates the description of sale order lines based on the components of the first active Bill of Materials (BOM) associated with the product.

It also adds two fields on Bill of Materials lines (``mrp.bom.line``):

- **Producer**: many2one to ``res.partner``. On product change it is preloaded with the first vendor of the product (lowest sequence of ``product.supplierinfo``). The user can override it manually.
- **Product Link**: related to ``producer.website``, editable. It follows the website of the selected producer.

Both fields are appended to the auto-generated sale order line description, so the producer and link are visible wherever that description is rendered (reports, emails, screen).

Usage
-----

- When a product is selected in a sale order line, the description is automatically updated with the components of the first active BOM linked to the product.
- For each BOM component the description shows: ``- <component> <qty> <uom>, <producer>, <product link>`` (producer and link are omitted if empty).
- Producer and Product Link can be edited on the BOM line tree to override the autofilled values.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
