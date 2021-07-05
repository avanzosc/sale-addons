# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models
from psycopg2.extensions import AsIs


class EducationGroupReport(models.Model):
    _name = "res.partner.addproduct.report"
    _description = "Additional Products Report"
    _auto = False
    _rec_name = "student_id"
    _order = "center_id,level_id,course_id,student_id,product_id"

    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Additional Product")
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center")
    level_id = fields.Many2one(
        comodel_name="education.level", string="Education Level")
    course_id = fields.Many2one(
        comodel_name="education.course", string="Course")
    company_id = fields.Many2one(
        comodel_name="res.company", string="Product Company")
    categ_id = fields.Many2one(
        comodel_name="product.category", string="Product Category")

    _depends = {
        "res.partner": [
            "additional_product_ids",
        ],
    }

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER () as id,
                stu.id AS student_id,
                stu.current_center_id AS center_id,
                stu.current_level_id AS level_id,
                stu.current_course_id AS course_id,
                p.id AS product_id,
                tmp.company_id AS company_id,
                tmp.categ_id AS categ_id
        """
        return select_str

    def _from(self):
        from_str = """
                FROM rel_partner_addproduct addproduct
                JOIN res_partner stu ON addproduct.partner_id = stu.id
                JOIN product_product p ON addproduct.product_id = p.id
                JOIN product_template tmp ON p.product_tmpl_id = tmp.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
                GROUP BY stu.id, p.id, tmp.id, stu.current_center_id,
                stu.current_level_id, stu.current_course_id, tmp.company_id,
                tmp.categ_id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = education_group_teacher_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()), AsIs(self._from()),
                AsIs(self._group_by()),))
