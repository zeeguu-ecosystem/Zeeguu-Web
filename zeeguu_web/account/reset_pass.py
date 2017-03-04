# -*- coding: utf8 -*-

"""
    reset_pass.py: Helping the forgetful reset their password
"""

import flask
from flask import flash

import zeeguu
from zeeguu import db

from zeeguu.model.unique_code import UniqueCode

# the account blueprint is defined in the __init__ of the module
from . import account

from smtplib import SMTP
import traceback
import sys
from zeeguu.model.user import User


@account.route("/reset_pass", methods=("POST", "GET",))
def reset_password():

    """
    Three main states of this controller
          1. by default just show the email field
          2. in a second step, also show the field for the code and new password
          3. in a third step, if code is correct, redirect to login
    :return: template to be rendered
    """

    form = flask.request.form
    email = form.get("email", "")
    code = form.get("code", "")
    password = form.get("password", "")

    if email and not code:
        generate_code_and_send_email(email)
        flash("Now check your inbox for a one-time code")
        return flask.render_template("reset_pass.html", code_active=True, email=email)

    if email and code and password:
        try:
            return change_password_if_code_is_correct(code, email, password)
        except Exception as e:
            flash("Something went wrong")
            traceback.print_exc(file=sys.stdout)
            return flask.render_template("reset_pass.html",message=True)

    flash("This will be fast. We promise.")
    return flask.render_template("reset_pass.html")


def content_of_email_with_code(team_email, email, code):
    """
    :param team_email: string
    :param email: string
    :param code: string
    :return:
    """
    return "\r\n".join([
          "From: " + team_email,
          "To: " + email,
          "Subject: Password Reset Code",
          "Hi there,",
          " ",
          "Please use this code to reset your password: " + str(code) + ".",
          " ",
          "Cheers,",
          "The Zeeguu Team"
          ])


def change_password_if_code_is_correct(code, email, password):
    """
    The params are the user input values
    :param code:string
    :param email: string
    :param password: string
    :return:
    """
    last_code = UniqueCode.last_code(email)
    if code == last_code:
        if len(password) < 4:
            flash("Password must be at least 4 characters long")
            return flask.render_template("reset_pass.html",
                                         code_active=True,
                                         email=email,
                                         code=code)
        user = User.find(email)
        user.update_password(password)
        db.session.commit()

        # Delete all the codes for this user
        for x in UniqueCode.all_codes_for(email):
            db.session.delete(x)
        db.session.commit()

        flash("Password was reset successfully!")
        return flask.redirect('login')
    else:
        flask.flash("Code seems wrong. Did you check your email?")
        return flask.render_template("reset_pass.html",
                                     code_active=True,
                                     message=True,
                                     email=email)


def generate_code_and_send_email(user_email):
    """
    Hardcoded for Gmail
    Assumes TEAM_EMAIL and TEAM_PASS are present in config.cfg

    :param user_email: string
    :return:
    """

    # Generate one-time code
    code = UniqueCode(user_email)
    db.session.add(code)
    db.session.commit()

    # Send email
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    team_email = zeeguu.app.config.get("TEAM_EMAIL")
    team_pass = zeeguu.app.config.get("TEAM_PASS")
    server.login(team_email, team_pass)
    server.sendmail(team_email, user_email, content_of_email_with_code(team_email, user_email, code))
    server.quit()
