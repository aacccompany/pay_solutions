# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route
import requests
from odoo.addons.payment.models.payment_acquirer import ValidationError
import random


class PaySolutions(http.Controller):

    @http.route('/aacc_x_odoo/pay_solutions_request', type='http', auth="public", csrf=False, cors="*")
    def pay_solutions_request(self, path=None):

        token = request.params.get('token')
        headers = {
            'Authorization': 'Basic {token}'.format(token=token),
            'Content-Type': 'application/json'
        }

        random_number = random.randint(100000, 999999)

        odoo_tx = request.env['payment.transaction'].sudo().search(
            [('reference', '=', request.params.get('reference'))])

        odoo_tx.write({'paysolutions_no': random_number})

        url = "https://apis.paysolutions.asia/tep/api/v2/promptpay?merchantID={merchant}&productDetail={refNo}&customerEmail={customeremail}&customerName={customername}&total={amount}&referenceNo={refNoTransactionCode}".format(
            amount=request.params.get('amount'),
            merchant=request.params.get('merchant'),
            refNo=str(request.params.get('reference')),
            refNoTransactionCode=random_number,
            customeremail=request.params.get('partner_email'),
            customername=str(request.params.get(
                'partner_name')),
        )

        response = requests.post(
            url, data={}, headers=headers).json()

        base_url = request.params.get('base_url')

        return request.render('pay_solutions.pay_solutions_view_qr', {
            'image':  response['data']['image'],
            'reference':  response['data']['referenceNo'],
            'base_url': base_url,
        })

    @http.route('/aacc_x_odoo/pay_solutions_validate', type='http', auth="public", csrf=False, cors="*")
    def pay_solutions_validate(self, path=None):

        try:
            result = request.env['pos.solution'].sudo(
            ).toggle_from_webhook_solution_order(request.params)

            if result == 'success':
                return result
        except ValidationError as e:
            #_logger.info('Received notification for tx %s. Skipped it because of %s', tx_reference, e)
            print(e)

        try:
            ref_key = request.params.get("refno")
            odoo_tx = request.env['payment.transaction'].sudo().search(
                [('paysolutions_no', '=', ref_key)])
            odoo_tx.write({'acquirer_reference': ref_key})
            odoo_tx._set_transaction_done()
        except ValidationError as e:
            #_logger.info('Received notification for tx %s. Skipped it because of %s', tx_reference, e)
            return False
        
        return '1'

    @http.route('/aacc_x_odoo/pay_solutions_status', type='http', auth="public", csrf=False, cors="*")
    def pay_solutions_status(self, path=None):
        try:
            ref_key = request.params.get("reference")
            odoo_tx = request.env['payment.transaction'].sudo().search(
                [('paysolutions_no', '=', ref_key)])
        except ValidationError as e:
            #_logger.info('Received notification for tx %s. Skipped it because of %s', tx_reference, e)
            return '0'

        if odoo_tx.state == 'done':
            return '1'
        return '0'
