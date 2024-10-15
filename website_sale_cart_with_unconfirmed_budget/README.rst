.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

========================================================
Website Sale Cart with Unconfirmed Budget
========================================================

Overview
========

The **Website Sale Cart with Unconfirmed Budget** module enhances the shopping cart functionality by linking unconfirmed budgets with the cart. When a product is added to the cart, it checks for existing unconfirmed budgets for the same customer and utilizes them instead of creating a new order. This ensures that the cart remains consistent and avoids unnecessary order duplication.

Features
========

- **Utilizes Unconfirmed Budgets**: When adding a product to the cart, the module checks for any existing unconfirmed budgets for the customer. If one exists, it will add the product to that budget instead of creating a new order.

- **Cart Management**: The module maintains the integrity of the cart during the conversion to a confirmed budget, ensuring that products remain in the cart when transitioning between states.

- **Redirect Handling**: Proper redirection after cart updates, maintaining the user experience during checkout.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Adding Products**:

   - When products are added to the cart, the module will automatically check for unconfirmed budgets and add the product to the appropriate budget if available.

3. **Budget Confirmation**:

   - Upon confirming the cart, the existing unconfirmed budget will be transformed into a confirmed order, maintaining the added products.

Configuration
=============

- **No additional configuration is required** for this module. It integrates seamlessly with the existing website sale module.

Testing
=======

Test the following scenarios:

- **Adding Products to Cart**:

  - Ensure that when a product is added to the cart, it checks for an existing unconfirmed budget and adds the product there.

- **Confirming the Cart**:

  - Verify that when the cart is confirmed, it correctly transforms the unconfirmed budget into a confirmed sale order, preserving all products.

- **Cart State After Confirmation**:

  - Check that the cart remains intact when transitioning from the cart to the budget and vice versa.

Bug Tracker
===========

For bugs and issues, please visit `GitHub Issues <https://github.com/avanzosc/l10n-addons/issues>`_ to report or track issues.

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
