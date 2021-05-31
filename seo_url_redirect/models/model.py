from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_log = logging.getLogger(__name__)


class Models(models.Model):

    _register = False

    @api.model
    def _add_magic_fields(self):
        super(Models, self)._add_magic_fields()
        self._add_field("url_key", fields.Char(
                            string='SEO Url Key',
                            default='',
                            translate=True,
                            help="SEO Url Key for Product Category",
                            copy=False
                            )
                        )

    @api.constrains('url_key')
    def __check_url_key_uniq(self):
        for obj in self:
            if obj.url_key:
                urlKey = "/" + obj.url_key
                res = self.env['website.rewrite'].sudo().search([('url_to', '=', urlKey), ('rewrite_val', '!=', 'custom')], 0, 2, 'id desc')
                if res:
                    for resObj in res:
                        if resObj.record_id == obj.id:
                            if resObj.rewrite_val != obj._name:
                                raise ValidationError(_('SEO URL Key must be unique!'))
                        else:
                            raise ValidationError(_('SEO URL Key must be unique!'))
        return True
