.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=============================
Sale Order Report Opportunity
=============================

This module adds the name of the linked opportunity to the printed quotation /
sale order.

Features
========

* The opportunity is shown in the information block of the sale order report,
  next to the salesperson and just before the order lines.
* It is only printed when the order comes from an opportunity, so orders
  created directly from the sales menu are not affected.
* It applies to quotations, sale orders and pro-forma invoices, since all of
  them share the same document template.

Usage
=====

#. Create a quotation from an opportunity (*CRM > Pipeline > New Quotation*),
   or set the *Opportunity* field on an existing order.
#. Print the quotation (*Print > Quotation / Order*).
#. The opportunity name appears in the header block of the document.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.