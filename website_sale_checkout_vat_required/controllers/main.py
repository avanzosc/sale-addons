from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):
    def checkout_form_validate(self, mode, all_form_values, data):
        field_list = (
            all_form_values["field_required"].split(",")
            if isinstance(all_form_values["field_required"], str)
            else all_form_values["field_required"]
        )

        if "vat" not in field_list:
            field_list.append("vat")

        all_form_values["field_required"] = ",".join(field_list)

        return super().checkout_form_validate(mode, all_form_values, data)
