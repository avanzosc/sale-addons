.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==================================
Website Sale Checkout Vat Required
==================================

Overview
========

The **Website Sale Checkout Vat Required** module enhances the address form in the Odoo website sales process. It modifies the VAT field to ensure that any alphabetic characters are properly formatted when submitted, providing a cleaner input for VAT registration.

Features
========

- **VAT Field Processing**: Automatically formats the VAT field to separate alphabetic characters from numeric values for improved data consistency.

- **Customization of Address Form**: Customizes the address form to ensure specific fields are treated as required.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Modify VAT Input**:

   - When customers enter their VAT numbers during checkout, the module will ensure the input is formatted correctly.

3. **Address Form Customization**:

   - The module customizes the address form to adjust which fields are required for submission.

Configuration
=============

No additional configuration is required. The module is ready to use once installed.

Testing
=======

Test the following scenarios:

- **VAT Formatting**:

  - Enter various VAT formats in the checkout process and confirm that they are correctly formatted after submission.

- **Address Form Validation**:

  - Check that the address form behaves as expected and that required fields are correctly enforced.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/yourusername/yourrepository/issues>`_.

Credits
=======

Contributors
------------

* Leire Martinez de Santos
* AvanzOSC

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
