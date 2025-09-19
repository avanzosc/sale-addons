.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Sale Import Wizard
==================

Module to import **Sale Orders** from Excel files, improving usability and automation in sales operations.

* Allows importing sale orders and order lines from structured Excel files.
* Automatically validates customers, products, invoice addresses, and delivery addresses.
* Creates sale orders and order lines from imported data.
* Provides a log of errors and highlights issues in import lines.
* Quick access to imported lines and created sale orders.

Key Features
============

- Wizard to upload Excel files and import sale orders.
- Validation of imported lines, with error reporting in **Log Info**.
- Automatic creation of **Sale Orders** and **Order Lines** from import lines.
- Search, filter, and group by **Product**, **Customer**, **Invoice Address**, **Delivery Address**, and **State**.
- Statusbar and state management for import workflow (`draft`, `2validate`, `pass`, `error`, `done`).
- Tree, form, and search views for **Sale Order Import Lines** with decorations to highlight errors and processed lines.

Configuration
=============

1. Go to **Sales → Configuration → Import Sale Orders**.
2. Upload an Excel file using the column names in the **Help** tab.
3. Click **Validate** to check imported lines.
4. Click **Process** to create sale orders from valid lines.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us improve it by providing detailed feedback.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
