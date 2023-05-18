{
    "name": "Newsletter Double Opt-In",
    "version": "16.0.1.0.1",
    "author": "Labiso GmbH",
    "category": "Marketing",
    "summary": (
        "Implements a double opt in workflow for newsletter registrations"
    ),
    "depends": ["mass_mailing", "website"],
    "data": [
        "data/opt_in_template.xml",
        "views/mailing_list.xml",
        "data/opt_in_page.xml",
    ],
    "application": False,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
