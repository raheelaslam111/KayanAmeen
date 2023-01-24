# -*- coding: utf-8 -*-
import pdb
from odoo import models, fields, exceptions, api, _
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



class endorsement_request(models.Model):
    _name = 'endorsement.request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mail.render.mixin']
    _description = 'endorsement_request'

    document_no = fields.Char(string='Document No')
    policy_type = fields.Selection([('endors', 'Endorsement')], default='endors',
                                   string="Transaction Type", tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    insurance_company_id = fields.Many2one('insurance.company',string='Insurance Company')
    policy_no = fields.Char("Policy No")
    insurance_type_id = fields.Many2one('insurance.type', string='Insurance Type')
    insurance_sub_type_id = fields.Many2one('insurance.sub.type', string='Insurance Sub Type',
                                            domain="[('insurance_type_id','=',insurance_type_id)]")
    prev_policy = fields.Many2one('insurance.policy', string="Policy", required='1')
    state = fields.Selection([('draft', 'Draft'),
                              ('review', 'Review'),
                              ('sent_to_insurance', 'Sent to Vendor'),
                              ('sent_to_customer', 'Sent to Customer'),
                              ('validate', 'Validate'),
                              ('cancel', 'Cancel')], string='state', default='draft', tracking=True)
    medical_visibility_check = fields.Boolean(string='Medical Visibility Check',
                                              compute='get_insurance_pages_visibility')
    vehicle_visibility_check = fields.Boolean(string='Vehicle Visibility Check',
                                              compute='get_insurance_pages_visibility')


    health_endors_ids = fields.Many2many('insurance.employee.data', string='Health Detail')
    endors_vehicle_ids = fields.Many2many('insurance.vehicle', string="Endorsement Vehicle Detail")
    endorsement_policy_id = fields.Many2one('insurance.policy',string='Related Endorsement Policy',compute='get_endorsement_policy')

    def action_open_endorsement_policy(self):
        return {
            'name': 'Endorsement Policy',
            'views': [
                (self.env.ref('policy_entry_insurance.view_policy_form').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'res_model': 'insurance.policy',
            'view_mode': 'form',
            'res_id': self.endorsement_policy_id.id,
        }

    def get_endorsement_policy(self):
        for rec in self:
            endorsement_policy = self.env['insurance.policy'].search([('endorsement_request_id','=',rec.id)],limit=1)
            if endorsement_policy:
                rec.endorsement_policy_id = endorsement_policy.id
            else:
                rec.endorsement_policy_id = False

    @api.model
    def create(self, vals):
        vals['document_no'] = self.env['ir.sequence'].next_by_code('endorsement.req.seq')
        res = super(endorsement_request, self).create(vals)
        return res

    def action_create_endorsement_policy(self):
        return {
            'name': 'Endorsement Policy',
            'views': [
                (self.env.ref('policy_entry_insurance.view_policy_form').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'res_model': 'insurance.policy',
            'context': {
                'default_policy_type': self.policy_type,
                'default_partner_id': self.partner_id.id,
                'default_insurance_company_id': self.insurance_company_id.id,
                'default_policy_no': self.policy_no,
                'default_insurance_type_id': self.insurance_type_id.id,
                'default_insurance_sub_type_id': self.insurance_sub_type_id.id,
                'default_prev_policy': self.prev_policy.id,
                'default_health_endors_ids': self.health_endors_ids.ids,
                'default_endors_vehicle_ids': self.endors_vehicle_ids.ids,
                'default_endorsement_request_id': self.id,
            },
            'view_mode': 'form',
        }

    @api.onchange('prev_policy')
    def _onchange_prev(self):
        line = [(5, 0, 0)]
        self.partner_id = self.prev_policy.partner_id.id
        self.insurance_company_id = self.prev_policy.insurance_company_id.id
        self.insurance_sub_type_id = self.prev_policy.insurance_sub_type_id.id
        self.insurance_type_id = self.prev_policy.insurance_type_id.id
        self.policy_no = self.prev_policy.policy_no
        # for benefits in self.prev_policy.benefits_custome_ids:
        #     vals = {
        #         # 'policy_id': policy.id,
        #         'name': benefits.name,
        #         'benefit_name': benefits.benefit_name,
        #         'category_type': benefits.category_type,
        #         'benefit_id': benefits.benefit_id.id,
        #         'benefit_value': benefits.benefit_value,
        #         'display_type': benefits.display_type,
        #         'sequence': benefits.sequence,
        #         'included': benefits.included,
        #         'vary': benefits.vary,
        #         'from_value': benefits.from_value,
        #         'to_value': benefits.to_value,
        #     }
        #     line.append((0, 0, vals))
        # self.benefits_custome_ids = line

    @api.depends('insurance_type_id')
    def get_insurance_pages_visibility(self):
        for rec in self:
            if rec.insurance_type_id.ins_type_select == 'is_medical':
                rec.medical_visibility_check = True
            else:
                rec.medical_visibility_check = False
            if rec.insurance_type_id.ins_type_select == 'is_vehicle':
                rec.vehicle_visibility_check = True
            else:
                rec.vehicle_visibility_check = False