# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class HrEmpDoc(models.Model):
    _name = 'hr.emp.doc'
    _description = "Employee Document"
    _rec_name = "type"

    hrdoc = fields.Many2one('hr.employee', string="Insurance Ref", required=1)
    # name = fields.Char("Document Name")
    type = fields.Many2one('hr.emp.doc.type',string="Document Type")
    start_date = fields.Date("Document Start date")
    end_date = fields.Date("Document End date")
    upload_file = fields.Many2many('ir.attachment')
    file_name = fields.Char(string="File Name")


class HrDocType(models.Model):
    _name = 'hr.emp.doc.type'
    _description = "Employee Document"

    name = fields.Char("Name", required=1)