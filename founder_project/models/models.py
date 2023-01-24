# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FounderProject(models.Model):
    _name = 'founder.project'
    _description = 'founder project'

    name = fields.Char('Project Name', required=1)
    name_ar = fields.Char('Project name Arabic')

    def purchase_requests(self):
        action_vals = {
            'name': _('Purchase request'),
            'domain': [('project_id', '=', self.id)],
            'res_model': 'purchase.req',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'view_mode':'tree,form',
        }
        return action_vals

    def purchase_orders(self):
        action_vals = {
            'name': _('Purchase order'),
            'domain': [('project_id', '=', self.id)],
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'view_mode':'tree,form',
        }
        return action_vals

    def purchase_bills(self):
        action_vals = {
            'name': _('Purchase order'),
            'domain': [('project_id', '=', self.id)],
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'view_mode':'tree,form',
        }
        return action_vals


class PurchaseReq(models.Model):
    _inherit = 'purchase.req'

    project_id = fields.Many2one('founder.project')

    def action_create_purchase_order(self):
        res = super(PurchaseReq, self).action_create_purchase_order()
        self.purchase_request_id.update({
            'project_id': self.project_id.id
        })
        return res


class PurchaseReqRec(models.Model):
    _inherit = 'purchase.req.rec'

    project_id = fields.Many2one('founder.project')

    def action_received(self):
        res = super(PurchaseReqRec, self).action_received()
        self.rfq_ref.update({
            'project_id': self.project_id.id
        })
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one('founder.project')

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        res['project_id'] = self.project_id.id
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('founder.project')



