.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Sale Discount Tax Recompute
===========================

This module extends Odoo Sales (`sale.order`) to correctly recompute taxes on global discount lines and loyalty reward discount lines when the fiscal position of a sales order is changed.

By default, Odoo may not correctly update taxes on some discount lines when using the "Update Taxes" action. Global discount lines can lose their taxes because the technical discount product has no taxes configured, while loyalty reward lines may keep taxes from the previous fiscal position.

This module ensures that both types of discount lines remain consistent with the taxes applied to the sales order after a fiscal position change.

Features
--------

- Correctly recomputes taxes on global discount lines created from the Sales Order Discount wizard.

- Correctly refreshes loyalty reward discount lines after a fiscal position change.

- Preserves the standard Odoo tax recomputation flow.

- Reuses the taxes of the corresponding sales order lines to determine the correct tax configuration for global discounts.

- Recomputes loyalty rewards only after normal lines and global discount lines have been updated.

- Supports sales orders with multiple tax groups.

- Prevents incorrect tax assignment when a previous tax group is split into multiple tax groups after applying a new fiscal position.

- Raises a validation error when the tax mapping of a global discount cannot be determined safely.

- No modification of the standard discount products or loyalty reward products is required.

Data Model
----------

**sale.order**

- Extends the standard tax recomputation process (`_recompute_taxes`).

- Detects global discount lines using:

  `company_id.sale_discount_product_id`

- Detects loyalty reward lines using:

  `sale.order.line.is_reward_line`

- Stores the relationship between each global discount line and the sales order lines that originally shared the same tax configuration before taxes are recomputed.

- Reassigns the appropriate taxes to global discount lines after the standard Odoo tax recomputation.

- Refreshes loyalty rewards through the standard loyalty engine after all other tax calculations have been completed.

Logic Overview
--------------

When the user changes the Fiscal Position of a sales order and uses the standard "Update Taxes" action:

1. The module identifies:

   - Normal sales order lines

   - Global discount lines

   - Loyalty reward discount lines

2. Before Odoo recomputes taxes, the module stores the relationship between each global discount line and the normal sales order lines that share the same tax group.

3. The standard Odoo tax recomputation is executed:

   `_recompute_taxes()`

4. Normal product lines are recalculated using the new Fiscal Position.

5. Global discount lines are recalculated using the new tax configuration of their related sales order lines.

6. Loyalty reward lines are refreshed using:

   `_update_programs_and_rewards()`

7. The final tax configuration remains consistent across product lines, global discounts and loyalty rewards.

Global Discount Tax Mapping
---------------------------

Global discount products created by Odoo do not necessarily have taxes configured directly on the product.

Because of this, their taxes cannot be safely recomputed using only:

`product_id.taxes_id`

Instead, this module determines the correct tax configuration from the sales order lines that belonged to the same tax group before the Fiscal Position was changed.

For example:

Before changing Fiscal Position:

- Product lines: `21% VAT + 18% Withholding`

- Global Discount: `21% VAT + 18% Withholding`

- Loyalty Reward: `21% VAT + 18% Withholding`

After changing Fiscal Position and updating taxes:

- Product lines: `21% VAT`

- Global Discount: `21% VAT`

- Loyalty Reward: `21% VAT`

Tax Group Safety
----------------

If a tax group that previously corresponded to a single global discount line becomes multiple different tax groups after changing the Fiscal Position, the module does not assign taxes automatically.

Instead, it raises a validation error indicating that the global discount must be removed and applied again.

This prevents the sales order from being left with an incorrect or ambiguous tax configuration.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it
first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <ajuaristio@gmail.com>

Do not contact contributors directly about support or help with technical issues.
