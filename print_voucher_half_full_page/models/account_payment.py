# -- coding: utf-8 --

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
#from odoo.tools.misc import formatLang, format_date
# try:
#     from num2words import num2words
# except ImportError:
#     _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
#     num2words = None

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    words_amount = fields.Char(string='In Words', compute='_compute_amount_total_words')
    # 

    @api.depends('amount', 'currency_id')
    def _compute_amount_total_words(self):
        # self.ensure_one()
        for payment in self:
            payment.words_amount = payment.currency_id.amount_to_text(payment.amount) if payment.currency_id else ''
            return payment.words_amount


    # def set_words_amount(self):
    #     for payment in self:
    #         payment.words_amount = payment.currency_id.amount_to_text(payment.amount) if payment.currency_id else ''

        
    # @api.onchange('amount', 'currency_id')
    # def _compute_amount_total_words(self):
    #     res = super(AccountPayment, self)._onchange_amount()
    #     self.words_amount = self.currency_id.amount_to_text(self.amount) if self.currency_id else ''
    #     return res
