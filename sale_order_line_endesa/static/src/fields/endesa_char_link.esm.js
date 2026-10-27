/* Copyright 2026 Lucía Echeverría - AvanzOSC
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html). */

import {Component} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useService} from "@web/core/utils/hooks";

/**
 * Char shown as a link that opens the record of another many2one field of
 * the row (option "link_field"), also from a list cell.
 */
export class EndesaCharLinkField extends Component {
  static template = "sale_order_line_endesa.EndesaCharLinkField";
  static props = {
    ...standardFieldProps,
    linkField: {type: String},
  };

  setup() {
    this.action = useService("action");
  }

  get value() {
    return this.props.record.data[this.props.name] || "";
  }

  get linkId() {
    const link = this.props.record.data[this.props.linkField];
    return link ? link[0] : false;
  }

  get relation() {
    return this.props.record.fields[this.props.linkField].relation;
  }

  onClick(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    this.action.doAction({
      type: "ir.actions.act_window",
      res_model: this.relation,
      res_id: this.linkId,
      views: [[false, "form"]],
    });
  }
}

export const endesaCharLinkField = {
  component: EndesaCharLinkField,
  displayName: _t("Link to another field"),
  supportedTypes: ["char"],
  supportedOptions: [
    {
      label: _t("Many2one field to open"),
      name: "link_field",
      type: "string",
    },
  ],
  extractProps: ({options}) => ({linkField: options.link_field}),
};

registry.category("fields").add("endesa_char_link", endesaCharLinkField);
