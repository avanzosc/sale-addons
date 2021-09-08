# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute("""
        UPDATE sale_order s
        SET teacher_id = (
            SELECT teacher_id
            FROM hr_employee_supervised_year t
            WHERE t.student_id = s.child_id
            AND t.school_year_id = s.academic_year_id);
    """)
