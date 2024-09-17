.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

====================================================
Sale Order Line Commitment Date and Delivery Address
====================================================

Overview
========

The **Sale Order Line Commitment Date and Delivery Address** module extends the Sale Order functionality in Odoo by adding two new fields to the sale order lines. This module allows you to track the commitment date and delivery address directly from the sale order lines, enhancing the detail and visibility of sales orders.

Features
========

- **Commitment Date**:
  
  - Adds a *Commitment Date* field to sale order lines, which is linked to the commitment date of the sale order.

- **Delivery Address**:
  
  - Adds a *Delivery Address* field to sale order lines, which displays the contact address of the partner associated with the sale order.

Usage
=====

After installing the module:

- Navigate to the **Sales** module in Odoo.
  
- Go to the **Sales Orders** menu and open any sales order.

- In the sale order lines, you will see the new fields *Commitment Date* and *Delivery Address*.

- These fields will show the commitment date of the sale order and the delivery address of the customer, respectively.

Configuration
=============

1. **Install the Module**:

   - Ensure that the `sale_management` module is installed as it is a dependency for this module.

2. **Verify Fields in Views**:

   - The module automatically adds the new fields to the tree view and search view of sale order lines.

Testing
=======

Test the following scenarios:

- **View Sales Order Lines**:
  
  - Open a sales order and check the sale order lines to verify that the *Commitment Date* and *Delivery Address* fields are displayed.

- **Filter Sales Orders**:

  - Use the search view to filter sales orders by *Commitment Date* and *Delivery Address*.

Bug Tracker
===========

For bugs and issues, please visit `GitHub Issues <https://github.com/avanzosc/sale-order-addons/issues>`_ to report or track issues.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>

* Ana Juaristi <anajuaristi@avanzosc.es>

Please contact contributors for module-specific questions, but direct support requests should be made through the official channels.

License
=======
This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
