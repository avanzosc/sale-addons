.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Sale Order Country Pivot
========================

This module extends the sales order and sales order line models to include fields for the customer's country and state, and the fiscal position on sales order lines. It also modifies the tree and pivot views to show these fields.

Features
--------

- Adds `Country` and `State` fields to the Sales Order model.
- Adds `Country`, `State`, and `Fiscal Position` fields to the Sales Order Line model.
- Updates the Sales Order tree view to display the `Country` and `State` fields.
- Updates the Sales Order pivot view to include `Country` and `State` fields.
- Updates the Sales Order Line tree view to include `Country`, `State`, and `Fiscal Position` fields.

Usage
-----

- Go to Sales -> Orders -> Orders in the backend.
- You will see `Country` and `State` columns in the sales order tree view.
- In the pivot view, you can group and aggregate by `Country` and `State`.
- In the sales order line tree view, you will see the `Country`, `State`, and `Fiscal Position` fields.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
