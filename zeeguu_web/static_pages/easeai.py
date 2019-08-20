from . import static_pages

import flask


@static_pages.route("/easeai")
def easeai():
    return flask.render_template("static_pages/easeai.html")
