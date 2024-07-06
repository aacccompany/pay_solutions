# -*- coding: utf-8 -*-

from odoo import api, fields, models

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('paysolutions', 'Pay solutions')], ondelete={'paysolutions': 'set default'})
    pay_solutions_api_key = fields.Char(
        'Pay solution API Key', required_if_provider='paysolutions',     groups='base.group_user')
    pay_solutions_secret_key = fields.Char(
        'Pay solution Secret Key', required_if_provider='paysolutions', groups='base.group_user')
    pay_solutions_auth_key = fields.Char(
        'Pay solution Auth Key', required_if_provider='paysolutions', groups='base.group_user')
    pay_solutions_merchant = fields.Char(
        'Pay solution merchant', required_if_provider='paysolutions', groups='base.group_user')

    def paysolutions_form_generate_values(self, values):
        base_url = self.get_base_url()
        values = dict(values)
        values.update({
            'amount': values['amount'],
            'currency': values['currency'] and values['currency'].name or '',
            'base_url': base_url,
            'reference': values['reference'],
            'token': self.pay_solutions_auth_key,
            'merchant': self.pay_solutions_merchant,
            'solutions': 'solutions'
        })
        return values

    def paysolutions_get_form_action_url(self):
        base_url = self.get_base_url() + "aacc_x_odoo/pay_solutions_request"
        base_url = base_url.replace("http://", "https://")
        return base_url


class PaymentTransactionPaysolutions(models.Model):
    _inherit = 'payment.transaction'
    
    paysolutions_no = fields.Char(
        'Pay solution no code', groups='base.group_user')
