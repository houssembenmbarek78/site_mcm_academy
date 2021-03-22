from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    document_ids = fields.One2many(
        comodel_name="partner.documents",
        inverse_name="partner_id",
        string="Related documents",
    )

    document_count = fields.Integer(
        compute="_compute_partner_documents_count", string="compteur documents"
    )

    documentst_count_string = fields.Char(
        compute="_compute_partner_documents_count", string="Documents"
    )

    def _compute_partner_documents_count(self):
        for record in self:
            document_ids = self.env["partner.documents"].search(
                [("partner_id", "child_of", record.id)]
            )
            record.document_count = len(document_ids)
            record.documentst_count_string = (
                "{}/5".format(len(document_ids))
            )


    def action_view_partner_documents(self):
        return {
            "name": self.name,
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "partner.documents",
            "type": "ir.actions.act_window",
            "domain": [("partner_id", "child_of", self.id)],
            "context": self.env.context,
        }