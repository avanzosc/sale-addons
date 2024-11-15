.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=======================
sale_report_stamp
=======================

Overview
========

The **sale_report_stamp** module extends the **sale** module to display the company’s digital signature and stamp images on the sale order report. It enhances the sale order PDF by including these company-specific details.

Features
========

- Adds a digital signature image to the sale order report if configured in the **Company** settings.
- Adds a digital stamp image to the sale order report if configured in the **Company** settings.

Usage
=====

1. **Install the Module**:
   - Install the **sale_report_stamp** module via the Apps menu.

2. **Configure Signature and Stamp**:
   - Ensure the **res_company_signature_fields** module is installed and the **Signature Image** and **Stamp Image** fields in the **Company** settings are populated.

3. **View Sale Order Report**:
   - Generate or print a sale order. The report will display the company's digital signature and stamp if they are configured.

Configuration
=============

This module depends on the **res_company_signature_fields** module, which provides the fields for storing the signature and stamp images.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Signature Display**:
  - Generate a sale order report with a configured signature image in the **Company** settings. Verify that the image appears on the report.

- **Test Stamp Display**:
  - Generate a sale order report with a configured stamp image in the **Company** settings. Check that the image is displayed as expected.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
