from flask import flash, make_response

from zeeguu_web.account.account_settings_form import AccountSettingsForm
from zeeguu_web.account.api.account_management import get_current_user_settings, set_user_settings
from zeeguu_web.constants import KEY__USER_NAME, KEY__NATIVE_LANG

from . import account

from zeeguu_web.crosscutting_concerns import login_first

import flask


@account.route("/my_settings", methods=["GET", "POSt"])
@login_first
def my_settings():
    user_info = get_current_user_settings()

    form = AccountSettingsForm(flask.request.form, **user_info.json())

    if flask.request.method == 'POST':
        set_user_settings(form.name.data,
                          form.email.data,
                          form.native_language.data,
                          form.learned_language.data)

        flask.session[KEY__USER_NAME] = form.name.data

        flash("Successfully changed settings")
        response = make_response(flask.redirect(flask.url_for("account.whatnext")))
        response.set_cookie(KEY__NATIVE_LANG, form.native_language.data, max_age=31536000)

        return response

    return flask.render_template("account/account_settings.html", form=form)
