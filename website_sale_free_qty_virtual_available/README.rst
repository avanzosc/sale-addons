.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=======================================================
Website Sale Free Qty Virtual Available
=======================================================

Overview
========

The **Website Sale Free Qty Virtual Available** module replaces the usage of `free_qty` with `virtual_available` to determine if stock is available or not in the context of online sales. This adjustment ensures that only the available quantity (considering reserved stock) is used to check stock availability.

Features
========

- **Stock Availability Based on Virtual Available**:
  - The module uses the `virtual_available` field instead of `free_qty` to determine if a product is available for sale, ensuring a more accurate representation of stock levels.

- **Customization**:
  - Modifies the product availability template to check stock availability using `virtual_available` when determining if the product is out of stock.

- **Updated Variant Controller**:
  - The module extends the variant controller to include the `virtual_available` value for a product, ensuring accurate stock information is provided when querying product combinations.

Usage
=====

1. **Install the Module**:
   - Install the **Website Sale Free Qty Virtual Available** module from the Apps menu.

2. **Product Availability Check**:
   - After installation, the stock availability check on the website will be based on the `virtual_available` field, which accounts for both real stock and reserved quantities.

3. **Combination Info**:
   - When querying product combinations, the updated `virtual_available` value will be included in the response, providing accurate stock information for each variant.

Configuration
=============

No additional configuration is required. The module will automatically replace the use of `free_qty` with `virtual_available` for stock availability checks.

Testing
=======

1. Test by adding a product to the website and verifying that the stock status is based on `virtual_available`.
2. Confirm that when querying product combinations, the `virtual_available` field is correctly included in the response.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

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
