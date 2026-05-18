.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

======================================
Sale Kit Description Producer & Link
======================================

Adds two fields to bill of materials lines:

* **Producer**: the component's sales description (``description_sale``).
* **Product Link**: the external URL of the component (``external_url``).

Both are filled automatically when the product is selected on a BoM line,
and can be edited afterwards.

When a sale order line uses a product whose BoM the ``sale_kit_description``
module expands into the description, every component line is extended with
the producer and link, so the information ends up in any printed report or
email that already renders the line description.

Example output::

    KIWI GRANDE
    - KIWI 5.0 kg, PEDRO MARI, GERNIKA (BIZKAIA), https://urbide.eu/kiwi

Technical notes
===============

The override of ``sale.order.line._set_bom_description`` **does not call**
``super()``; it rebuilds the description in a single pass to keep the
producer/link in the same loop as the base BoM iteration. Any other module
that extends ``_set_bom_description`` via ``super()`` on top of
``sale_kit_description`` will be short-circuited when this module is
installed. If you need to chain additional logic, override
``_set_bom_description`` here (or split the line-formatting into a hook).

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_.

Credits
=======

Contributors
------------

* AvanzOSC

License
=======

This project is licensed under the AGPL-3 License.
