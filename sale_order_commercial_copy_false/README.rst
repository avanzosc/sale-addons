.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Sale Order Commercial Copy False
================================

Overview
========

The **Sale Order Commercial Copy False** module modifies the behavior of duplicate sale orders by ensuring that certain fields related to the commercial partner are not copied to the new order. This helps maintain data integrity and avoids unnecessary duplication of sensitive information.

Features
========

- **Sale Order**:
  
  - The `user_id` field is not copied when duplicating a sale order.

- **Sale Order Line**:
  
  - The `salesman_id` field is not copied when duplicating a sale order line.

Usage
=====

After installing the module, the following changes will be applied:

- **Sale Orders**:

  - When duplicating a sale order, the `user_id` field will not be copied to the new order.

- **Sale Order Lines**:

  - When duplicating a sale order line, the `salesman_id` field will not be copied to the new line.

Configuration
=============

No additional configuration is required. The module works out of the box once installed.

Testing
=======

The module has been designed with the following functionalities in mind:

- **Duplication of Sale Orders**:

  - Test the duplication of sale orders to ensure that the `user_id` field is not copied to the new order.

- **Duplication of Sale Order Lines**:

  - Test the duplication of sale order lines to ensure that the `salesman_id` field is not copied to the new line.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/sale-addons/issues>`_. Please check there for existing issues or to report new ones.

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
