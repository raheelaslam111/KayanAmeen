# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import except_orm
from odoo.exceptions import UserError, ValidationError


class ContractDeduction(models.Model):
    _name = 'contract.deduction'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Contract Deduction"

    name = fields.Char(string="Deduction Name", default="/", readonly=True)
    date = fields.Date(string="Date", default=fields.Date.today())
    requseter_id = fields.Many2one('res.users', string="Requester", default=lambda self: self.env.user, readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True,track_visibility='onchange')
    department_id = fields.Many2one(related='employee_id.department_id',track_visibility='onchange', string="Department", readonly=True)
    deduction_lines = fields.One2many('contract.deduction.line', 'deduction_id', string="Deductions Line", index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
    ], string="State", default='draft', copy=False)
    deduction_amount = fields.Float(string="Deduction Amount", required=True, track_visibility='onchange')
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_deduction_amount')
    balance_amount = fields.Float(string="Balance Amount", compute='_compute_deduction_amount')
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_deduction_amount')
    installment_type = fields.Selection([
        ('installment_amount', 'Installment Amount'),
        ('installment_no', 'Installment No.',),
    ], string="Payment Type", default='installment_amount',track_visibility='onchange', copy=False)
    installment = fields.Integer(string="No Of Installments", default=1)
    installment_amount = fields.Float(string="Installment Amount",track_visibility='onchange')
    payment_date = fields.Date(string="Installment Date",track_visibility='onchange', required=True, default=fields.Date.today())
    employee_no = fields.Char('Employee No')
    salary = fields.Float()
    description = fields.Text(string="Description", required=True, copy=False)
    prevoius_total = fields.Float("Prev Balance",compute='_prev_balance')

    @api.depends('employee_id')
    def _prev_balance(self):
        for rec in self:
            op_bal_date = " '" + str('2021-09-01') + "'"
            op_date = " and ml.date<'" + str('2021-09-01') + "'"
            op_date_payslip = " and mv.date<'" + str('2021-09-01') + "'"
            period = " and ml.date>='" + str('2021-09-01') + "' and ml.date<='" + str(fields.date.today()) + "'"

            sbqry = ''
            if rec.employee_id:
                sbqry = ' and e.id = ' + str(rec.employee_id.id)

            query = '''
                                   select e.id,e.employee_number, e.name as employee, ''' + op_bal_date + ''' as date, '' as type_of_deduction, '' as payment_ref, 'Opening Balance' as description
                            ,sum(Debit-Credit)
                         -coalesce((select sum(amount) from account_move mv, hr_payslip_line pl, hr_payslip pay
                                   where pl.employee_id=e.id and pay.id=pl.slip_id and pay.move_id=mv.id
                         and pl.code in ('CD','LO') and pl.amount !=0
                            and mv.state='posted' ''' + op_date_payslip + '''
                                   ),0)
                         as addition,0 as deduction, 1 as op_bal
                            from hr_employee e,account_account coa, account_move_line ml
                            Where ml.employee_id=e.id and ml.account_id=coa.id
                            and coa.code='11150002' 
                            and ml.parent_state='posted' ''' + op_date + sbqry + '''
                            group by e.id,e.employee_number, e.name, coa.id
    
                         union all
                            select e.id,e.employee_number, e.name as employee, ml.date, ml.name as type_of_deduction ,ml.move_name as payment_ref, ml.ref as description
                            ,ml.debit as addition,ml.credit as deduction, 0 as op_bal
                            from hr_employee e,account_account coa, account_move_line ml
                            Where ml.employee_id=e.id and ml.account_id=coa.id
                            and coa.code='11150002'
                            and ml.parent_state='posted' ''' + period + sbqry + '''
    
                         union all
                            select e.id,e.employee_number,e.name as employee, ml.date, pl.name as type_of_deduction,'' as payment_ref, CONCAT(pay.name,' ',coalesce((select name from hr_payslip_run pr where pr.id=pay.payslip_run_id),'')) as description
                            ,0 as addition,pl.amount as deduction, 0 as op_bal
                            from hr_employee e, account_move ml, hr_payslip_line pl, hr_payslip pay
                            Where pl.employee_id=e.id and pay.id=pl.slip_id and pay.move_id=ml.id
                         and pl.code in ('CD','LO') and pl.amount !=0
                            and ml.state='posted' ''' + period + sbqry + '''
                            order by employee,date
                           '''
            print("Q", query)
            #
            self._cr.execute(query)
            balance=0
            query_res = self._cr.dictfetchall()
            for res in query_res:
                addition = res['addition']
                deduction = res['deduction']
                balance = balance + addition - deduction
            rec.prevoius_total=balance
    def approve_deduction(self):
        self.state="approve"


    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """it get the department of employee it have"""
        for emp in self:
            emp.department_id = emp.employee_id.department_id.id if emp.employee_id.department_id else False
            emp.employee_no = emp.employee_id.employee_number
            if emp.sudo().employee_id.contract_id:
                emp.salary = emp.sudo().employee_id.contract_id.wage

    def _compute_deduction_amount(self):
        """
        it computes total amount and total paid amount ,balance amount fields
        """
        total_paid = 0.0
        for deduction in self:
            for line in deduction.deduction_lines:
                if line.status == 'done':
                    total_paid += line.amount
            balance_amount = deduction.deduction_amount - total_paid
            self.total_amount = deduction.deduction_amount
            self.balance_amount = balance_amount
            self.total_paid_amount = total_paid



    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('contract.deduction.seq')
        res = super(ContractDeduction, self).create(values)
        return res

    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        if any(ded.status=='done' for ded in self.deduction_lines):
            raise ValidationError("There is some entries in done state")
        for deduction in self:
            deduction.deduction_lines.unlink()
            amount = 0.0
            installment = 1
            TotalLastAmount = 0.0
            date_start = datetime.strptime(str(deduction.payment_date), '%Y-%m-%d')
            if deduction.installment_type == 'installment_no':
                amount = deduction.deduction_amount / deduction.installment
                installment = deduction.installment
            else:
                amount = deduction.installment_amount
                installment = deduction.deduction_amount / deduction.installment_amount
            if installment == len(self.deduction_lines):
                raise except_orm('Error!', 'Line Already Filled')
            else:
                for i in range(1, int(installment) + 1):
                    self.env['contract.deduction.line'].create({
                        'date': date_start,
                        'amount': amount,
                        'employee_id': deduction.employee_id.id,
                        'deduction_id': deduction.id,
                        'installment_type': deduction.installment_type,
                        'description': str(deduction.description) + '-' + str(date_start)})
                    date_start = date_start + relativedelta(months=1)
            # Last Payment Amonuts CA
            for line in deduction.deduction_lines:
                TotalLastAmount += line.amount
            if (deduction.deduction_amount - TotalLastAmount) > 0:
                self.env['contract.deduction.line'].create({
                    'date': date_start,
                    'amount': deduction.deduction_amount - TotalLastAmount,
                    'employee_id': deduction.employee_id.id,
                    'deduction_id': deduction.id,
                    'installment_type': deduction.installment_type,
                    'description': str(deduction.description) + '-' + str(date_start)})
        return True


class ContractDeductionLine(models.Model):
    _name = 'contract.deduction.line'
    _description = "Installment Line"
    _rec_name = 'description'

    date = fields.Date(string="Payment Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    amount = fields.Float(string="Amount", required=True)
    deduction_id = fields.Many2one('contract.deduction', string="Deduction Ref.")
    status = fields.Selection([('pending', 'Pending'), ('done', 'Done'), ('hold', 'Hold')], string="Status",
                              default="pending")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    description = fields.Text(string="Description")
    installment_type = fields.Selection([
        ('installment_amount', 'Installment Amount'),
        ('installment_no', 'Installment No.'),
    ], string="Payment Type", copy=False)


