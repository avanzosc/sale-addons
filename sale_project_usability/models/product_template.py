# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    project_template_group_by_id = fields.Many2one(
        comodel_name="project.project",
        store=True,
        copy=False,
        compute="_compute_project_template_group_by_id",
        string="Project Template",
    )

    @api.depends("project_template_id")
    def _compute_project_template_group_by_id(self):
        for template in self:
            project = self.env["project.project"]
            if template.project_template_id:
                project = template.project_template_id.id
            template.project_template_group_by_id = project
