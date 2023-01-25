# -*- coding: utf-8 -*-
import pdb
from odoo import models, fields, exceptions, api, _
from random import choice
from string import digits
from odoo.exceptions import ValidationError, UserError
from datetime import date
from xlrd import open_workbook
from bs4 import BeautifulSoup
import xlrd
import logging
from datetime import datetime, timedelta
from hijri_converter import Hijri, Gregorian
import requests
from odoo.http import request
from odoo import http



class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    # equipment_assign_to = fields.Selection(selection_add=[('employee', 'Employee'),('branch', 'Branch')])
    equipment_assign_to = fields.Selection(
        [('department', 'Department'), ('employee', 'Employee'),('branch', 'Branch'), ('other', 'Other')],
        string='Used By',
        required=True,
        default='employee', tracking=True)
    branch_id = fields.Many2one('branch.name',string='Branch', tracking=True)

    employee_id = fields.Many2one('hr.employee', compute='_compute_equipment_assign',
                                  store=True, readonly=False, string='Assigned Employee', tracking=True)
    department_id = fields.Many2one('hr.department', compute='_compute_equipment_assign',
                                    store=True, readonly=False, string='Assigned Department', tracking=True)
    owner_user_id = fields.Many2one(compute='_compute_owner', store=True)
    assign_date = fields.Date(compute='_compute_equipment_assign', store=True, readonly=False, copy=True)

    def generate_random_serial_no(self):
        for rec in self:
            rec.serial_no = '041'+"".join(choice(digits) for i in range(9))



    is_parent = fields.Boolean(string='Is Parent?', tracking=True)
    is_subsidiary = fields.Boolean(string='Is subsidiary?', tracking=True)
    parent_id = fields.Many2one('maintenance.equipment',string='Parent', tracking=True)


    assets_value = fields.Float(string='Assets Value', tracking=True)
    acc_dep_value = fields.Float(string='Acc.Dep Value', tracking=True)
    net_amount = fields.Float(string='Net Amount',compute='get_net_amount')

    # def action_open_label_layout(self):
    #     pdb.set_trace()
    #     view = self.env.ref('assets_management_ra.equipment_label_layout_form')
    #     return {
    #         'name': _('Print Equipment Labels'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'equipment.label.layout',
    #         'views': [(view.id, 'form')],
    #         'view_id': view.id,
    #         'target': 'new',
    #         'context': {
    #             # 'default_equipment_ids': self.move_line_ids.product_id.ids,
    #             },
    #     }




    @api.depends('assets_value','acc_dep_value')
    def get_net_amount(self):
        for rec in self:
            rec.net_amount = rec.assets_value - rec.acc_dep_value


    @api.depends('employee_id', 'department_id', 'equipment_assign_to')
    def _compute_owner(self):
        for equipment in self:
            equipment.owner_user_id = self.env.user.id
            if equipment.equipment_assign_to == 'employee':
                equipment.owner_user_id = equipment.employee_id.user_id.id
            elif equipment.equipment_assign_to == 'department':
                equipment.owner_user_id = equipment.department_id.manager_id.user_id.id

    @api.depends('equipment_assign_to')
    def _compute_equipment_assign(self):
        for equipment in self:
            if equipment.equipment_assign_to == 'employee':
                equipment.department_id = False
                equipment.employee_id = equipment.employee_id
            elif equipment.equipment_assign_to == 'department':
                equipment.employee_id = False
                equipment.department_id = equipment.department_id
            else:
                equipment.department_id = equipment.department_id
                equipment.employee_id = equipment.employee_id
            equipment.assign_date = fields.Date.context_today(self)



class branch_name(models.Model):
    _name = 'branch.name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mail.render.mixin']
    _description = 'branch_name'

    name = fields.Char(string='Branch Name')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    partner_id = fields.Many2one('res.partner', string='Vendor Name', check_company=True)
    vendor_reference = fields.Char(string='Vendor Reference')
    invoice_date = fields.Date(string='Invoice Date')
    cost = fields.Float(string='Cost')


class EquipmentLabelLayout(models.TransientModel):
    _name = 'equipment.label.layout'
    _description = 'Choose the sheet layout to print the labels'

    print_format = fields.Selection([
        ('dymo', 'Dymo'),
        ('2x7xprice', '2 x 7 with price'),
        ('4x7xprice', '4 x 7 with price'),
        ('4x12', '4 x 12'),
        ('4x12xprice', '4 x 12 with price')], string="Format", default='2x7xprice', required=True)
    # custom_quantity = fields.Integer('Quantity', default=1, required=True)
    equipment_ids = fields.Many2many('maintenance.equipment')
    # product_tmpl_ids = fields.Many2many('product.template')
    extra_html = fields.Html('Extra Content', default='')
    # rows = fields.Integer(compute='_compute_dimensions')
    # columns = fields.Integer(compute='_compute_dimensions')
    #
    # @api.depends('print_format')
    # def _compute_dimensions(self):
    #     for wizard in self:
    #         if 'x' in wizard.print_format:
    #             columns, rows = wizard.print_format.split('x')[:2]
    #             wizard.columns = int(columns)
    #             wizard.rows = int(rows)
    #         else:
    #             wizard.columns, wizard.rows = 1, 1

    def _prepare_report_data(self):
        xml_id = 'assets_management_ra.report_equipment_label'
        equipment_ids = self.equipment_ids
        print(equipment_ids)
        active_model = 'product.product'
        # else:
        #     raise UserError(_("No product to print, if the product is archived please unarchive it before printing its label."))

        # Build data to pass to the report
        data = {
            'active_model': 'maintenance.equipment',
            'equipment_ids': equipment_ids,
            'layout_wizard': self.id,
            # 'price_included': 'xprice' in self.print_format,
        }
        return xml_id, data


    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))
        report_action = self.env.ref(xml_id).report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action


class ReportEquipmentLabel(models.AbstractModel):
    _name = 'report.assets_management_ra.report_equipmentlabel'
    _description = 'Equipment Label Report'

    def _get_report_values(self, docids, data):
        # return _prepare_data(self.env, data)
        equipment_ids = self.env['maintenance.equipment'].search([('id','in',data.get('context').get('default_equipment_ids'))])

        return {
            'equipment_ids': equipment_ids,
            'docids': docids,
            # 'columns': layout_wizard.columns,
            # 'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
            # 'price_included': data.get('price_included'),
            # 'extra_html': layout_wizard.extra_html,
        }
