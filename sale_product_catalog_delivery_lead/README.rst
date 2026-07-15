.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==================================
Sale Product Catalog Delivery Lead
==================================

This module extends ``sale_product_catalog`` so the delivery lead time of a
sale order line can be driven by the catalog instead of the product.

In HLC's scenario the number of delivery days does not depend on the product
but on the catalog: an online catalog is assumed to have stock and ships almost
immediately, while a prebook catalog may take months.

Features
========

* Adds a **Delivery Lead Time** field (in days) to the product catalog.
* When a sale order has a catalog assigned and its delivery lead time is
  greater than 0, every order line takes that value as its lead time.
* When the catalog is empty or its delivery lead time is 0, the line keeps the
  standard value coming from the product's customer lead time.
* Assigning or changing the catalog on the order header updates all the lines,
  and it also works for orders created from the website or through the API
  (the logic runs in the ``customer_lead`` computation, not in an onchange).

Configuration
=============

Go to the catalog form (*Sales > Catalogs*) and set the **Delivery Lead Time**.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.com>

License
=======

AGPL-3
