.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Compute Planned Hours on Tasks Module
=====================================

Summary
=======

The **Compute Planned Hours on Tasks** module automates the calculation of planned hours on project tasks in Odoo. 
It extends the `sale.order.line` model to compute `planned_hours` 
based on product quantity, sales order state, and project hourly rate defined in `project.project`.

Installation
============

This module requires Odoo dependencies:
- Base
- Project
- Sales

Install the module via the Odoo Apps interface.

Bug Tracker
===========

Report bugs or provide feedback on `GitHub Issues <https://github.com/avanzosc/compute-planned-hours/issues>`_.

Credits
=======

Author
------
- Unai Beristain <unaiberistain@avanzosc.es>
