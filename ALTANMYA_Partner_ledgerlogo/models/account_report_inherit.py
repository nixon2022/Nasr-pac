# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import markupsafe
from odoo import api, fields, models, tools, _

class AccountReportInherit(models.AbstractModel):
    _inherit = 'account.report'



    def _get_html_render_values(self, options, report_manager):
        return {

            'report': {
                'name': self._get_report_name(),
                'summary': report_manager.summary,
                'company_name': self.env.company.name,
                'company_logo': self.env.company.logo,
                'vat_number': self.env.company.vat,
                'company_partner_id': self.env.company.partner_id.name,
                'company_address': self.env.company.street,
                'company_address_street': self.env.company.street2,
                'company_address_city': self.env.company.city,
                'company_address_state_id': self.env.company.state_id.name,
                'company_address_zip': self.env.company.zip,
                'company_address_country_id': self.env.company.country_id.name,
                'company_registry': self.env.company.company_registry,
            },

            'options': options,
            'context': self.env.context,
            'model': self,
        }

    # TO BE OVERWRITTEN
    def _get_templates(self):
        # res= super(AccountReportInherit, self)._get_templates()
        print("ssecond")
        return {
                'main_template': 'ALTANMYA_Partner_ledgerlogo.main_template_with_filter_input_partner_with_edit',
                'main_table_header_template': 'account_reports.main_table_header',
                'line_template': 'account_reports.line_template',
                'footnotes_template': 'account_reports.footnotes_template',
                'search_template': 'account_reports.search_template',
                'line_caret_options': 'account_reports.line_caret_options',
        }

    def get_html(self, options, line_id=None, additional_context=None):
        '''
               return the html value of report, or html value of unfolded line
               * if line_id is set, the template used will be the line_template
               otherwise it uses the main_template. Reason is for efficiency, when unfolding a line in the report
               we don't want to reload all lines, just get the one we unfolded.
        '''
        # Prevent inconsistency between options and context.
        self = self.with_context(self._set_context(options))

        templates = self._get_templates()
        print("templates ", templates)
        print("options   ", options)
        report_manager = self._get_report_manager(options)


        render_values = self._get_html_render_values(options, report_manager)
        if additional_context:
            render_values.update(additional_context)

        # Create lines/headers.
        if line_id:
            headers = options['headers']
            lines = self._get_lines(options, line_id=line_id)
            template = templates['line_template']

        else:
            headers, lines = self._get_table(options)
            options['headers'] = headers
            template = templates['main_template']

        if options.get('hierarchy'):
            lines = self._create_hierarchy(lines, options)
        if options.get('selected_column'):
            lines = self._sort_lines(lines, options)

        lines = self._format_lines_for_display(lines, options)

        render_values['lines'] = {'columns_header': headers, 'lines': lines}

        # Manage footnotes.
        footnotes_to_render = []
        if self.env.context.get('print_mode', False):
            # we are in print mode, so compute footnote number and include them in lines values, otherwise, let the js compute the number correctly as
            # we don't know all the visible lines.
            footnotes = dict([(str(f.line), f) for f in report_manager.footnotes_ids])
            number = 0
            for line in lines:
                f = footnotes.get(str(line.get('id')))
                if f:
                    number += 1
                    line['footnote'] = str(number)
                    footnotes_to_render.append({'id': f.id, 'number': number, 'text': f.text})

        # Render.

        if render_values['report']['name'] == 'Partner Ledger':
            template='ALTANMYA_Partner_ledgerlogo.main_template_with_filter_input_partner_with_edit'
        html = self.env.ref(template)._render(render_values)
        if self.env.context.get('print_mode', False):
            for k, v in self._replace_class().items():
                html = html.replace(k, v)
            html = html.replace(markupsafe.Markup('<div class="js_account_report_footnotes"></div>'),
                                self.get_html_footnotes(footnotes_to_render))
        return html

