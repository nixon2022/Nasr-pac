from odoo import models, fields, api,_

class AccountPartnerLedgerInherit(models.AbstractModel):
    _inherit = 'account.partner.ledger'

    invoice_date = fields.Date(string='Invoice Date')

    @api.model
    def _get_partner_ledger_lines(self, options, line_id=None):
        lines = super(AccountPartnerLedgerInherit, self)._get_partner_ledger_lines(options, line_id=line_id)
        for line in lines:
            move_id = self.env['account.move'].browse(line.get('move_id'))
            if move_id:
                line['invoice_date'] = move_id.invoice_date or ''  # Add your logic to fetch invoice_date
        return lines

    def _get_columns_name(self, options):
        columns = [
            # {'name': _('Invoice Date'),'class': 'date'},
            {'name': _('JRNL')},
            {'name': _('Account')},
            {'name': _('Ref')},
            {'name': _('Due Date'), 'class': 'date'},
            {'name': _('Matching Number')},
            {'name': _('Initial Balance'), 'class': 'number'},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'}]

        if self.user_has_groups('base.group_multi_currency'):
            columns.append({'name': _('Amount Currency'), 'class': 'number'})

        columns.append({'name': _('Balance'), 'class': 'number'})

        return columns



class ReportPartnerLedgerInherit(models.AbstractModel):
        _inherit = 'account.partner.ledger'

        def _get_columns_name(self, options):
            columns = super(ReportPartnerLedgerInherit, self)._get_columns_name(options)
            # Insert 'Invoice Date' as the first column
            columns.insert(0, {'name': 'Invoice Date', 'style': 'text-align:center; border: 1px solid #e6e6e6;border-collapse: separate;'})
            return columns

        def _get_templates(self):
            templates = super(ReportPartnerLedgerInherit, self)._get_templates()
            templates['main_template'] = 'your_module.report_partnerledger_main_template'
            return templates