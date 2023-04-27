from odoo import models, fields


class MailingList(models.Model):
    _inherit = "mailing.list"

    double_opt_in = fields.Boolean(
        string="Double Opt-In",
        help=(
            "If set, contacts will be added to the list only after they have"
            " confirmed their subscription"
        ),
        default=True,
    )
