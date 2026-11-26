/* Copyright 2026 Lucía Echeverría - AvanzOSC
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html). */

import {
  Many2ManyTagsField,
  many2ManyTagsField,
} from "@web/views/fields/many2many_tags/many2many_tags_field";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

/**
 * Tags that open their record when clicked, also from a list cell.
 */
export class EndesaMany2ManyTagsOpenField extends Many2ManyTagsField {
  setup() {
    super.setup();
    this.action = useService("action");
  }

  getTagProps(record) {
    const props = super.getTagProps(record);
    props.onClick = (ev) => {
      ev.stopPropagation();
      this.action.doAction({
        type: "ir.actions.act_window",
        res_model: this.relation,
        res_id: record.resId,
        views: [[false, "form"]],
      });
    };
    return props;
  }
}

export const endesaMany2ManyTagsOpenField = {
  ...many2ManyTagsField,
  component: EndesaMany2ManyTagsOpenField,
  supportedTypes: ["many2many", "one2many"],
};

registry
  .category("fields")
  .add("endesa_many2many_tags_open", endesaMany2ManyTagsOpenField);
