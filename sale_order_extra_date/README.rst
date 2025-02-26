.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

============================
Sale Order Extra Date Fields
============================

Overview
========

The **Sale Order Extra Date Fields** module adds two additional datetime fields to the Sale Order form:

1. **Customer Order Creation Date**.

2. **Reconfirmed Date**.

These fields allow users to store important date information related to the sale order, improving tracking and reporting capabilities.

Features
========

- **Additional Date Fields**:

  - Adds two new fields to the `sale.order` model:

    - **Customer Order Creation Date**: The date the order was created by the customer.

    - **Reconfirmed Date**: The date the order was reconfirmed.
  
- **In the Sale Order View**:

  - These fields are displayed in the Sale Order form for easier access.
  
- **In the Sale Order Line View**:

  - The fields are added to the sale order line tree view but are set as invisible.

Usage
=====

1. **Install the Module**:

   - Install the **Sale Order Extra Date Fields** module from the Apps menu.

2. **View the Sale Order Form**:

   - Navigate to *Sales* → *Orders* → *Sales Orders*.

   - In the Sales Order form, you will see two new fields:

     - **Customer Order Creation Date**.

     - **Reconfirmed Date**.

3. **Invisible Fields in Sale Order Line View**:

   - In the Sale Order line tree view, the new fields will be present but invisible.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/sale-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
