from odoo.addons.mass_mailing.controllers.main import MassMailController
from odoo.http import request, route


class OptinController(MassMailController):
    @route(
        ["/mail/subscription-opt-in/<int:subscription_id>/<string:token>"],
        type="http",
        website=True,
        auth="public",
    )
    def mailing_opt_in(self, subscription_id, token="", **post):
        """
        This controller method handles subscription opt-ins through a unique token.
        It checks if the token matches the one associated with the subscription,
        and updates the subscription's opt-out and token fields accordingly.

        :param subscription_id: int - the ID of the subscription being opted in
        :param token: str - the unique token associated with the subscription
        :return: http.Response - the rendered opt-in page template
        """
        # Retrieve the subscription from the database
        subscription = (
            request.env["mailing.contact.subscription"]
            .sudo()
            .browse(subscription_id)
        )

        # Check if the token matches the one associated with the subscription
        if subscription.opt_in_token == token:
            # If the token matches, update the subscription's opt-out and
            # token fields
            subscription.opt_out = False
            subscription.opt_in_token = False

            return request.redirect("/mailing-subscribe-thank-you")
        else:
            return request.redirect("/mailing-subscribe-error")
