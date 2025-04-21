from odoo import http
from odoo.http import request
from ..services.zalopay_api import ZaloPayAPI
import logging

_logger = logging.getLogger(__name__)

class ZaloPayController(http.Controller):

    @http.route('/payment/zalopay/redirect', type='http', auth='public', methods=['GET'], csrf=False)
    def zalopay_redirect(self, **kwargs):
        tx_id = kwargs.get('tx_id')
        tx = request.env['payment.transaction'].sudo().browse(int(tx_id))

        provider = tx.provider_id
        zalopay = ZaloPayAPI(
            app_id=provider.zalopay_app_id,
            key1=provider.zalopay_key1,
            key2=provider.zalopay_key2,
            endpoint=provider.zalopay_endpoint,
        )

        result = zalopay.create_order(
            amount=int(tx.amount),
            app_trans_id=tx.reference,
            app_user=tx.partner_id.name,
            embed_data={"return_url": "/payment/zalopay/return"},
            items=[]
        )

        if result.get("return_code") == 1:
            return http.redirect_with_hash(result["order_url"])
        else:
            return "Failed to create ZaloPay order"

    @http.route('/payment/zalopay/callback', type='http', auth='public', methods=['POST'], csrf=False)
    def zalopay_callback(self, **post):
        parsed = http.request.jsonrequest
        _logger.info("ZaloPay Callback: %s", parsed)

        tx = request.env['payment.transaction'].sudo().search([
            ('reference', '=', parsed.get("app_trans_id"))
        ], limit=1)

        if tx:
            tx._handle_notification_data('zalopay', parsed)

        return "OK"
