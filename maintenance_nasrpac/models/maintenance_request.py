# -*- coding: utf-8 -*-
import math
from turtle import pd

from odoo import api, fields, models
from datetime import datetime, date, time, timezone
from datetime import timedelta


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    request_date1 = fields.Datetime(string='Request Date',
                                    help="Date requested for the maintenance to happen",
                                    default=fields.Date.context_today)

    close_date1 = fields.Datetime(string='Close Date', help="Date the maintenance was finished." )

    schedule_date1 = fields.Datetime(string='Scheduled Date', default=fields.Date.context_today)

    done_time = fields.Float(string='Done Time', help="the date has been spent to finish the maintenance ",
                             compute="_compute_done_time")

    job_donetime = fields.Float(string='Technician job done time', help ="the date has been spent to Technician job done time",
                                compute="_compute_job_donetime")

    etft = fields.Datetime(string= 'Expected time to finish maintenance' , compute='_compute_etft')


    expected_mtbf = fields.Integer(string='Expected MTBF',
                                   help='Expected Mean Time Between Failure')

    mtbf1 = fields.Integer(string='MTBF',
                           help='Mean Time Between Failure, computed based on done corrective maintenances.', related='equipment_id.mtbf')

    mttr1 = fields.Integer(string='MTTR',
                         help='Mean Time To Repair',related='equipment_id.mttr')

    estimated_next_failure1 = fields.Date(string='Estimated time before next failure (in days)' ,
                                          help='Computed as Latest Failure Date + MTBF',related='equipment_id.estimated_next_failure')

    latest_failure_date1 = fields.Date(string='Latest Failure Date',related='equipment_id.latest_failure_date')





    @api.onchange('close_date1')
    def _compute_close_date1(self):
        for rec in self:
            if not rec.close_date1:
               rec.close_date1 = datetime.now()








    def _compute_done_time(self):
        for rec in self:
            rec.done_time = None
            if rec.close_date1:
                diff = rec.close_date1 - rec.request_date1
                sec = diff.total_seconds()
                print('different in sec ',sec)
                min = sec / 60
                print('different in minutes ', min)
                hors = sec / (60 * 60)
                print('-----own hours----', hors)
                rec.done_time = hors




    def _compute_job_donetime(self):
        for rec in self:
            rec.job_donetime = None
            if rec.close_date1:
                diff1 = rec.close_date1 - rec.schedule_date1
                sec1 = diff1.total_seconds()
                print('different in sec ',sec1)
                min1 = sec1 / 60
                print('different in sec ', min1)
                hors1 = sec1 / (60 * 60)
                print('-----own hours----', hors1)
                rec.job_donetime = hors1



    @api.depends('schedule_date1','mttr1')
    def _compute_etft(self):
        for rec in self:
            rec.etft = None
            if rec.mttr1 != 0 and rec.schedule_date1 :
                rec.etft =rec.schedule_date1 + timedelta(hours=rec.mttr1)
            else:
                if rec.schedule_date1:
                     rec.etft =rec.schedule_date1 + timedelta(hours=rec.equipment_id.maintenance_duration)
            
























