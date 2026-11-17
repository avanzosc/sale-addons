.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==============================
Sale Commission Discount Rules
==============================

## Features

- Adds a new **Filter** commission type to the `sale.commission` model.
- Allows configuring commission rules based on the discount percentage applied to sales lines.
- Each rule defines a **Product Category**, a comparison **Operator**, a **Discount** threshold, and a **Commission** percentage.
- Supports the comparison operators `==`, `>`, `<`, `>=`, and `<=`.
- Allows assigning multiple discount-based rules to the same commission.
- Calculates the commission amount by applying the percentage defined in the first matching rule to the sales line subtotal.
- Extends the existing `sale.commission.line.mixin` calculation method while preserving the standard behavior for other commission types.

## Dependencies

- `sale_commission` from OCA/commission.

Use the Odoo `18.0` branch of this module.

## Commission Calculation

When the commission type is set to **Filter**, the module evaluates the configured rules against the discount percentage of the sales line.

Each rule contains:

- **Category** (`category`): Product category associated with the rule.
- **Operation** (`operation`): Comparison operator used to evaluate the discount.
- **Discount** (`discount`): Discount percentage used as the comparison threshold.
- **Commission** (`commission`): Commission percentage applied when the condition matches.

The rules are evaluated sequentially, and the first matching rule determines the commission percentage.

The commission amount is calculated as:

`Commission Amount = Sales Line Subtotal × Commission Percentage / 100`

For example, if a sales line has a subtotal of 1,000, a discount of 10%, and a matching rule specifies a commission of 5%, the resulting commission amount is 50.

If no rules are configured, the commission amount is zero.

Products marked as commission-free are excluded from the custom filter calculation.

## Configuration

1. Open the commission configuration in Odoo.
2. Create or edit a sales commission.
3. Select **Filter** as the commission type.
4. Add the desired discount rules in the **Formula Data** section.
5. Define the product category, comparison operator, discount threshold, and commission percentage for each rule.
6. Save the commission configuration.

## Installation

1. Install the `sale_commission` dependency from the OCA `18.0` branch.
2. Copy `sale_commission_discount_rules` into your Odoo `addons_path`.
3. Update the Apps list and install **Sale Commission Discount Rules**.
4. Configure a commission using the new **Filter** commission type.

## Limitations / Points to Validate

- Rules are evaluated sequentially, and only the first matching rule is applied.
- The product category field is available in the rule configuration but is not currently used to filter the sales lines during commission calculation.
- If no configured rule matches the discount, the calculation falls back to the standard commission calculation method.
- The commission percentage is applied to the sales line subtotal, which already reflects the discount.
- The module relies on the discount field of the sales line being available through `object_id`.
- The module has not been validated against a running Odoo 18 database; installation testing and functional QA are recommended before production use.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Berezi Amubieta Eceiza <bereziamubieta@avanzosc.es>
