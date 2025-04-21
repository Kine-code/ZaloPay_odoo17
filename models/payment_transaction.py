from odoo import models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _handle_notification_data(self, provider_code, notification_data):
        if provider_code != 'zalopay':
            return super()._handle_notification_data(provider_code, notification_data)

        _logger.info('Received ZaloPay notification: %s', notification_data)

        transaction_reference = notification_data.get('app_trans_id')
        transaction = self._get_tx_from_notification_data('zalopay', notification_data)

        if not transaction:
            _logger.warning("ZaloPay: No transaction found for reference %s", transaction_reference)
            raise ValidationError("Transaction not found")

        status = notification_data.get('status')
        if status == '1':
            transaction._set_transaction_done()
        elif status == '0':
            transaction._set_transaction_pending()
        else:
            transaction._set_transaction_cancel()

        return transaction

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        if provider_code != 'zalopay':
            return super()._get_tx_from_notification_data(provider_code, notification_data)
        return self.search([('reference', '=', notification_data.get('app_trans_id'))], limit=1)
