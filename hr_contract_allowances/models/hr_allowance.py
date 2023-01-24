# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)

from odoo import models, fields, api, exceptions
from odoo import tools, _
from odoo.tools import UserError

DEFAULT_RULE_PYTHON_CODE = """
total = 0
for line in contract.allowances_ids:
    if line.allowance_id.name == '%s':
        total = line.amount
    result = total
"""


class Allowance(models.Model):
    _name = 'hr.allowance'
    _rec_name = 'name'
    _description = 'Allowance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Allowance Name", required=True)
    python_code = fields.Text(string="Python Code", compute="_compute_python_code")
    active = fields.Boolean(string="Active", default=True)

    @api.depends('name')
    def _compute_python_code(self):
        """
        it generates python code for allowance
        """
        for rec in self:
            rec.python_code = DEFAULT_RULE_PYTHON_CODE % rec.name

    def unlink(self):
        """restrict on delete
                """
        for record in self:
            contract_lines = self.env['hr.contract.allowance.line'].search_count([('allowance_id', '=', record.id)])
            if contract_lines != 0:
                raise exceptions.ValidationError(
                    _('You can not delete the allowance which is used in employee contracts'))
        res = super(Allowance, self).unlink()
        return res

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Allowance Rule with name already created !')
    ]


class ContractAllowanceLine(models.Model):
    _name = 'hr.contract.allowance.line'
    _rec_name = 'allowance_id'
    _description = 'Contract Allowance Line'

    allowance_id = fields.Many2one(comodel_name="hr.allowance", string="Allowance")
    contract_id = fields.Many2one(comodel_name="hr.contract", string="Contract")
    rate = fields.Float('Rate/Amount')
    type = fields.Selection([('Amount', 'Amount'),
                             ('Percentage', 'Percentage')], string='Type', default='Amount')

    category = fields.Selection([('basic', 'Basic'),
                             ('allowance1', 'Allowance 1'),('allowance2', 'Other Allowance 2')], string='Category', default='basic')
    amount = fields.Float(string="Amount", compute='_get_amount', store=True)
    index_value = fields.Char(string="Index")
    
    def create(self, values):
        record = super(ContractAllowanceLine, self).create(values)
        return record

    @api.depends('type', 'rate', 'contract_id.basic_salary')
    def _get_amount(self):
        """
        it calc total amount according to formula
        """
        for record in self:
            if record.type == 'Amount':
                record.amount = record.rate
            else:
                if record.contract_id:
                    record.amount = record.contract_id.basic_salary * record.rate / 100
                else:
                    record.amount = record.rate / 100

    @api.constrains('allowance_id', 'contract_id')
    def check_unique_contract(self):
        for record in self:
            Records = self.search([('allowance_id', '=', record.allowance_id.id), ('contract_id', '=', record.contract_id.id)])
            if len(Records) > 1:
                raise UserError(str(self.allowance_id.name) + " has already been used for this contract !\nCan't add it twice")
