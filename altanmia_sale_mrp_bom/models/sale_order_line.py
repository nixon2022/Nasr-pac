# Copyright 2020 Akretion Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bom_summary = fields.Html("Order Bom Summary")

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get("bom_summary", False):
            return res

        html_content = ""
        for line in self.order_line:
            if not line.bom_id:
                continue
            html_content += f"""<div>
                                    <h3> {line.product_id.name}/ {line.bom_id.code}:</h3>
                                    <div class="summary ml-5">{line.bom_summary}</div>
                                </div>"""

        self.write({"bom_summary": html_content})
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        html_content = ""
        for line in self.order_line:
            if not line.bom_id:
                continue
            html_content += f"""<div>
                                    <h3> {line.product_id.name}/ {line.bom_id.code}:</h3>
                                    <div class="summary ml-5">{line.bom_summary}</div>
                                </div>"""
        res.write({"bom_summary": html_content})
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="BoM",
        domain="[('product_tmpl_id.product_variant_ids', '=', product_id),"
               "'|', ('product_id', '=', product_id), "
               "('product_id', '=', False)]",
    )

    bom_summary = fields.Html("Line Bom Summary")

    @api.constrains("bom_id", "product_id")
    def _check_match_product_variant_ids(self):
        for line in self:
            if line.bom_id:
                bom_product_tmpl = line.bom_id.product_tmpl_id
                bom_product = bom_product_tmpl.product_variant_ids
            else:
                bom_product_tmpl, bom_product = None, None
            line_product = line.product_id
            if not bom_product or line_product == bom_product:
                continue
            raise ValidationError(
                _(
                    "Please select BoM that has matched product with the line `{}`"
                ).format(line_product.name)
            )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            bom = self.env['mrp.bom']._bom_find(rec.product_id, bom_type='normal').get(rec.product_id)
            rec.bom_id = bom or None

    @api.onchange('bom_id')
    def onchange_bom(self):
        for record in self:
            record.product_uom_qty = record.bom_id.sale_qty or record.product_uom_qty
            record.price_unit = record.bom_id.unit_cost or record.price_unit

    def write(self, vals):
        bom = vals.get('bom_id', self.bom_id.id)
        if bom:
            messages = self.env['mail.message']._message_fetch(domain=[
                ('res_id', '=', bom),
                ('model', '=', 'mrp.bom'),
                ('message_type', '!=', 'user_notification'),
            ], limit=30)
            html_content = "<u class='text-decoration-none'>"
            for msg in messages:
                html_content += f"""<li>
                                        <b>{msg.get('author_id')[1]}: </b>
                                        <i class='text-mute pull-right'>{msg.get("date")}</i>
                                        <span class="msg-body">{msg.get('body', '')}</span>
                                    </li>"""
            html_content += "</u>"
            vals['bom_summary'] = html_content
        return super(SaleOrderLine, self).write(vals)

    @api.model
    def create(self, vals):
        bom = vals.get('bom_id', False)
        if bom:
            messages = self.env['mail.message']._message_fetch(domain=[
                ('res_id', '=', bom),
                ('model', '=', 'mrp.bom'),
                ('message_type', '!=', 'user_notification'),
            ], limit=30)
            html_content = ""

            html_content = "<u class='text-decoration-none'>"
            for msg in messages:
                html_content += f"""<li>
                                                    <b>{msg.get('author_id')[1]}: </b>
                                                    <i class='text-mute pull-right'>{msg.get("date")}</i>
                                                    <span class="msg-body">{msg.get('body', '')}</span>
                                                </li>"""
            html_content += "</u>"
            vals['bom_summary'] = html_content
        return super(SaleOrderLine, self).create(vals)
