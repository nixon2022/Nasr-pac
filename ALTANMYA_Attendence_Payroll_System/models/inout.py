from odoo import api,models, fields
from datetime import datetime, timedelta

class Inout(models.Model):
      _name = 'od.inout'
      _description = 'Attendance table'

      emp_deviceno = fields.Integer(string='employee id device')
      emp_name=fields.Char(string='Employee name',compute='_getname',depends=['emp_deviceno'],store=False)
      date_in = fields.Datetime(string='time in')
      date_out = fields.Datetime(string='time out')
      shift_id = fields.Many2one('resource.calendar.attendance',string='shift')
      date_inflag =fields.Selection([('internal','Internal'),('setting','Setting'),('manuel','Manuel')],string='date in source', default='manuel')
      date_outflag = fields.Selection([('internal','Internal'),('setting','Setting'),('manuel','Manuel')],string='date out source', default='manuel')
      att_date=fields.Date(string='Attendance date')
      att_leave = fields.Integer(string="leaving type")
      os_in = fields.Datetime(string='standard time in')
      os_out = fields.Datetime(string='standard time out')

      def _getname(self):
            for inout_rec in self:
                  rec=self.env['hr.employee'].search([('studio_employee_number','=',inout_rec.emp_deviceno)])
                  if rec:
                   if len(rec)==1:
                     inout_rec.emp_name=rec.display_name
                   else:
                     inout_rec.emp_name = 'TOO MANY EMP!!'
                  else:
                   inout_rec.emp_name = 'NOT DEFINED!!'


      def write(self, vals):
          if 'date_in' in vals:
              updval =datetime.strptime(vals['date_in'], "%Y-%m-%d %H:%M:%S")
              newval=updval- timedelta(seconds=updval.second)
              vals['date_in']=newval
              vals['date_inflag'] ='manuel'
          if 'date_out' in vals:
              updval =datetime.strptime(vals['date_out'], "%Y-%m-%d %H:%M:%S")
              newval=updval- timedelta(seconds=updval.second)
              vals['date_out']=newval
              vals['date_outflag'] = 'manuel'

          if 'os_in' in vals:
              updval =datetime.strptime(vals['os_in'], "%Y-%m-%d %H:%M:%S")
              newval=updval- timedelta(seconds=updval.second)
              vals['os_in']=newval

          if 'os_out' in vals:
              updval =datetime.strptime(vals['os_out'], "%Y-%m-%d %H:%M:%S")
              newval=updval- timedelta(seconds=updval.second)
              vals['os_out']=newval



          res = super(Inout, self).write(vals)
          return res

      @api.model
      def create(self, vals_list):

          # if vals_list['att_date']:
          #     updval = datetime.strptime(vals_list['date_in'], "%Y-%m-%d %H:%M:%S")
          #     newval = updval - timedelta(seconds=updval.second)
          #     vals_list['att_date'] = newval

          if vals_list['date_in']:
              updval = datetime.strptime(vals_list['date_in'], "%Y-%m-%d %H:%M:%S")
              newval = updval - timedelta(seconds=updval.second)
              vals_list['date_in'] = newval
          # vals_list['date_inflag'] = 'manuel'
          if vals_list['date_out']:
              updval = datetime.strptime(vals_list['date_out'], "%Y-%m-%d %H:%M:%S")
              newval = updval - timedelta(seconds=updval.second)
              vals_list['date_out'] = newval

          if vals_list['os_in']:
              updval = datetime.strptime(vals_list['os_in'], "%Y-%m-%d %H:%M:%S")
              newval = updval - timedelta(seconds=updval.second)
              vals_list['os_in'] = newval

          if vals_list['os_out']:
              updval = datetime.strptime(vals_list['os_out'], "%Y-%m-%d %H:%M:%S")
              newval = updval - timedelta(seconds=updval.second)
              vals_list['os_out'] = newval

          res = super(Inout, self).create(vals_list)
          return res


