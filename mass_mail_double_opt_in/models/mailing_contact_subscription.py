from odoo import models, api, fields
from secrets import token_urlsafe


class MailingContactSubscription(models.Model):
    _inherit = "mailing.contact.subscription"

    opt_in_token = fields.Char(
        string="Opt-In Token",
        help="Token used to verify the opt-in of the contact.",
    )

    opt_in_url = fields.Char(
        string="Opt-In URL",
        compute="_compute_opt_in_url",
        help="URL used to verify the opt-in of the contact.",
    )

    def _compute_opt_in_url(self):
        """
        This method computes the opt-in URL for the current contact
        subscription.
        """

        # Iterate over the current contact subscriptions
        for record in self:
            # If the list is not double opt-in, skip the opt-in URL
            if not record.list_id.double_opt_in:
                continue

            # Compute the opt-in full URL with the base URL and the opt-in
            # token
            record.opt_in_url = (
                "{base_url}/mail/subscription-opt-in/{id}/{token}".format(
                    base_url=self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("web.base.url"),
                    id=record.id,
                    token=record.opt_in_token,
                )
            )

    def send_opt_in_mail(self):
        """
        This method sends an opt-in confirmation mail to the current contact
        subscription.
        """

        self.ensure_one()

        # Get the opt-in confirmation mail template
        template = self.env.ref(
            "mass_mail_double_opt_in.mass_mail_confirmation_template"
        )

        # Send the mail using the template and the current contact subscription
        template.with_user(1).send_mail(self.id)

    @api.model_create_multi
    def create(self, vals_list):
        """
        This method overrides the 'create' method of the base model to add a
        double opt-in mechanism.

        If the list is double opt-in, it generates an opt-in token, sets the
        opt-out flag to True, and sends an opt-in confirmation mail.

        :param vals_list: A list of dictionaries containing the field values for
            the new contact subscriptions.
        :return: A list of the created contact subscription records.
        """

        # Create the new contact subscription records using the base method
        records = super().create(vals_list)

        # Iterate over the new records
        for record in records:
            # If the list is not double opt-in, skip the confirmation mail
            if not record.list_id.double_opt_in:
                continue

            # Generate an opt-in token if not already present
            if not record.opt_in_token:
                record.opt_in_token = token_urlsafe(32)

            # Set the opt-out flag to True to require confirmation
            record.opt_out = True

            # Send the opt-in confirmation mail
            record.send_opt_in_mail()

        # Return the created contact subscription records
        return records
