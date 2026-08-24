from . import models
from odoo import api, SUPERUSER_ID


def _post_install_calculate_customized_sequence(env):
    env.cr.execute("""
        SELECT COALESCE(MAX(split_part(name, '-', 3)::integer), 0)
        FROM sale_order
        WHERE name LIKE 'AR-%'
          AND length(name) - length(replace(name, '-', '')) = 2
    """)
    last_sequence = env.cr.fetchone()[0]

    sequence = env.ref(
        "sale_order_custom_sequence.seq_sale_order_customized",
        raise_if_not_found=False,
    )
    if sequence:
        sequence.number_next = last_sequence + 1
