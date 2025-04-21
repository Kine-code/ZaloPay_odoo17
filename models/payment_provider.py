from odoo import models, fields


class ProviderZaloPay(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('zalopay', "ZaloPay")],
        ondelete={'zalopay': 'set default'}
    )

    zalopay_app_id = fields.Char("ZaloPay App ID")
    zalopay_key1 = fields.Char("ZaloPay Key1")
    zalopay_key2 = fields.Char("ZaloPay Key2")
    zalopay_endpoint = fields.Char("ZaloPay API Endpoint", default="https://sb-openapi.zalopay.vn/v2/create")
    
def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.code == 'zalopay':
            return self.env.ref('payment.payment_method_electronic').id
        return super()._get_default_payment_method_id()
