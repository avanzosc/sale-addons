.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====================
Sale Product Catalog
====================

This module allows you to create and manage product catalogs for sales.
Each catalog groups a set of pricelist items with configuration such as logo,
description, inventory availability policy, and warehouse.

The catalog–product relationship is defined at the **pricelist item** level:
a catalog contains the specific price rules (pricelist items) that apply to
it, rather than a flat list of products. This makes it possible to have the
same product appear in multiple catalogs at different prices or through
different pricelists.

Key features
============

* Create named catalogs with logo, description, warehouse, and inventory
  availability policy (Never / Always / On Threshold / Custom).
* **Multi-company** — each catalog belongs to a company; a record rule
  ensures users only see catalogs from their own company.
* **Archiving** — catalogs support the standard ``active`` flag so they can
  be archived without being deleted.
* Assign **pricelist items** to one or more catalogs via a many-to-many
  relation (``pricelist_item_catalog_rel``).
* Stat button on each catalog form showing the number of linked pricelist
  items, with a click-through to the filtered list.
* **Catalog** field on sale orders with automatic warehouse propagation: when
  a catalog is selected the order's warehouse updates to match the catalog's
  warehouse.
* **Catalog** field on sale order lines, automatically inherited from the
  parent order (stored computed field).
* **Catalogs** field on each pricelist item, visible in both list and form
  views.
* **Pivot view** for pricelist items grouped by catalog → pricelist, with
  products as rows and fixed price as measure. Defaults to fixed-price items
  only (filter can be removed by the user).
* Extension of the **Pricelist Items** menu provided by
  ``product_pricelist_item_menu`` with a pivot view for catalog-based price
  analysis.

Migration from v12
==================

When installing on a database previously migrated from v12
(``acysos_hlc`` / ``product_catalog_web``), the module runs two hooks:

``pre_init_hook``
    Creates the ``product_catalog`` table as a copy of ``product_catalog_web``
    (same IDs, same columns). No original data is modified or deleted.

``post_init_hook``
    Populates ``pricelist_item_catalog_rel`` by crossing the v12 relations:

    * ``catalog_web_product_pricelist_rel`` (catalog ↔ pricelist)
    * ``catalog_web_product_template_rel`` (catalog ↔ product template)

    A pricelist item is linked to a catalog when its pricelist belongs to
    that catalog **and** its product is listed in that catalog.
    Both product-template items (``applied_on = 1_product``) and
    product-variant items (``applied_on = 0_product_variant``) are handled.
    Category-level and global items are not migrated (they had no catalog
    link in v12 either, as the field was a ``related`` on ``product_id``).

    All v12 tables are treated as read-only during migration; no original
    rows are deleted.

Usage / How to test
===================

1. Go to **Sales → Products → Catalogs**.
2. Create a new catalog, fill in the name, warehouse, and inventory
   availability, and save.
3. Open the catalog form. In the **Pricelist Items** tab, add pricelist items
   manually. Use the stat button to open the filtered list view.
4. Go to **Sales → Products → Pricelist Items** to see all items with their
   catalog assignments. Use the **Pivot** view to compare prices across
   catalogs and pricelists.
5. On a sale order, select a catalog and confirm the warehouse is updated.

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
