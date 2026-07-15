.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Sale Order Picking Res Partner Fields
=====================================

Overview
========

The **Sale Order Picking Res Partner Fields** module extends the Sale Order and Stock Picking models in Odoo by adding additional fields linked to the `res.partner` model. It provides a way to capture and display detailed information related to sales orders and stock pickings.

Features
========

- **Additional Fields in Sale Order**:

  - Adds fields such as `integrator`, `sale_phone`, `delivery_note`, `install_address`, `install_date`, `install_type`, `technical_contact`, `training`, `installation_by`, `structure_type`, and `initial_order` to the Sale Order model.

- **Enhanced Stock Picking**:

  - Adds corresponding fields in the Stock Picking model that are related to the Sale Order.

- **Extended Res Partner**:

  - Introduces a `delivery_timetable` field in the Res Partner model.

- **New Models**:

  - Includes new models for `InstallType` and `StructureType`.

Usage
=====

After installing the module, the following changes will be visible:

- **Sale Orders**:

  - New fields will be available on the Sale Order form to capture additional information related to sales and installations.

- **Stock Pickings**:

  - Additional fields on the Stock Picking form will reflect the related Sale Order information.

- **Res Partners**:

  - A new field for `delivery_timetable` will be available on the Res Partner form.

Configuration
=============

1. **Field Configuration**:

   - Ensure the new fields are appropriately configured and visible in the Sale Order and Stock Picking forms.

2. **Access Rights**:

   - Verify that the necessary access rights are set up for the new models and fields.

Testing
=======

Test the following functionalities:

- **Sale Order Forms**:

  - Verify that all new fields are correctly displayed and saved on the Sale Order form.

- **Stock Picking Forms**:

  - Ensure that the fields related to the Sale Order are correctly populated and displayed on the Stock Picking form.

- **Res Partner Forms**:

  - Confirm that the `delivery_timetable` field is correctly displayed on the Res Partner form.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/project-addons/issues>`_. Please check there for existing issues or to report new ones.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>

* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.

License
=======
This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <http://www.gnu.org/licenses/agpl-3.0-standalone.html>.
