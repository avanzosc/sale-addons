# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def _catch_top_bottom_graphic_info(sale_line):
    top_graphic = "ZZZZZ"
    bottom_graphic = "ZZZZZ"
    for description_line in sale_line.name.split('\n'):
        if description_line.startswith(f"Top Graphic"):
            top_graphic = description_line.split(":", 1)[1].strip()
        if description_line.startswith(f"Bottom Graphic"):
            bottom_graphic = description_line.split(":", 1)[1].strip()
    return top_graphic, bottom_graphic
