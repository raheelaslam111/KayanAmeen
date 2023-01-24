# -*- coding: utf-8 -*-

from datetime import datetime, date
from odoo import models, fields, api


class NotifyInbox(models.Model):
    _name = 'notify.inbox'
    _description = "Notify Messages"

    def send_inbox_message(self, subject, body, partner_ids, res_model, res_id):
        login_partner = self.env.user.partner_id
        vals = {
            'record_name': subject,
            'subject': subject,
            'email_from': login_partner.name + ' <%s>' % login_partner.email,
            'author_id': login_partner.id,
            'body': body,
            'message_type': 'notification',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'partner_ids': partner_ids,
            'needaction_partner_ids': partner_ids,
            'starred_partner_ids': partner_ids,
            'no_auto_thread': True,
            'model': res_model,
            'res_id': res_id,
            'date': datetime.now(),
        }
        self.sudo().env['mail.message'].create(vals)._notify(self.env[res_model].search([('id', '=', res_id)]), vals)

    def get_partner_from_email_group(self, partner_ids):
        return [(6, 0, [p.id for p in partner_ids if p])]

    def get_subject_body_from_email(self, template, red_id):
        print(red_id,'red_id')
        body = self.env['mail.template'].browse(template.id).generate_email(red_id)['body_html']
        subject = self.env['mail.template'].browse(template.id).generate_email(red_id)['subject']
        return subject, body

    def send_inbox_msg(self, partner_ids, template, model, res_id):
        if partner_ids:
            partner_ids = self.get_partner_from_email_group(partner_ids)
            print(res_id,'res_id')
            subject, body = self.get_subject_body_from_email(template, res_id)
            self.send_inbox_message(subject, body, partner_ids, model, res_id)



