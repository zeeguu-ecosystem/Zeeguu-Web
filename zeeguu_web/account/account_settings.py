from zeeguu_web.account.account_settings_form import AccountSettingsForm
from zeeguu_web.account.api.account_management import get_current_user_settings

from . import account, login_first
import flask


@account.route("/settings", methods=["GET", "POSt"])
@login_first
def stats_s():

    user_info = get_current_user_settings()
    print(user_info.json())

    form = AccountSettingsForm(flask.request.form, **user_info.json())

    if flask.request.method == 'POST':
        print(f"going to call the api with: {form.data}")
        return flask.redirect('whatnext')


    return flask.render_template("my_account.html", form=form)
