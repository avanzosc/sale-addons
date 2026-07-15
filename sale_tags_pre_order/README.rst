.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Sale Tags Pre-Order
===================

This module extends Odoo Sales, CRM Tags, and Shopify Payment Gateway to automate advance invoicing for pre-order sales flows.

It introduces a tagging-based mechanism that allows sales orders to automatically generate advance invoices upon confirmation, with optional posting and automatic payment based on configuration.

Features
--------

- Extends crm.tag with pre-order configuration options.
- Automatic advance invoice creation on Sales Order confirmation.
- Tag-based control of invoice generation logic.
- Flexible invoice posting rules (draft, open, or paid).
- Integration with Shopify payment gateway journals for automatic payment registration.
- Automatic assignment of invoice journal based on CRM tag configuration.

Data Model
----------

**crm.tag**

- Is Pre Order (is_pre_order): Marks the tag as a pre-order trigger.
- Invoice Mode (invoice_mode): Controls invoice lifecycle behavior:
  - none: Invoice is generated in draft.
  - open: Invoice is posted automatically.
  - paid: Invoice is posted and automatically paid.
- Advance Journal (journal_id): Journal used for pre-order invoices.

**sale.order**

- Overrides action_confirm:
  - Triggers pre-order invoice creation after confirmation.
- Pre-order invoice logic:
  - Only applies if at least one CRM tag has is_pre_order = True.
  - Only triggers when:
    - Invoice status is "no", OR
    - Invoice status is "to invoice" and Shopify status is "unfulfilled".
- Automatic advance invoice creation:
  - Creates a 100% advance payment invoice using Odoo wizard.
  - Assigns journal based on CRM tag configuration.

**shopify.payment.gateway.ept**

- Journal (journal_id):
  - Defines the accounting journal used for automatic payment registration.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* AvanzOSC

Contributors
~~~~~~~~~~~~

* `AvanzOsc <http://www.avanzosc.es>`_:

  * Berezi Amubieta <bereziamubieta@avanzosc.es>
  * Ana Juaristi <anajuaristi@avanzosc.es>
