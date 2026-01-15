=======================================
Sale Subscription Auto Validate Disable
=======================================

Disable the automatic validation and sending of invoices created from
subscriptions. Recurring invoices still get generated, but they remain
unvalidated so users can review and confirm them manually.

Installation
============

- Install this module after ``sale_subscription``.

Behavior
========

- ``validate_and_send_invoice`` is forced to run with ``auto_commit=False``.
- The recurring invoice cron calls ``_create_recurring_invoice`` with
  ``automatic=False`` so invoices stay unvalidated.

Compatibility
=============

Tested for Odoo 18.0.
