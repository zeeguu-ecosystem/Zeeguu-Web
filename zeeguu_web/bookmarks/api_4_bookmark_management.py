# These following endpoints are invoked via ajax calls from the bookmarks page

from zeeguu_web.account.api.bookmarks import \
    star_bookmark, \
    report_learned_bookmark, \
    unstar_bookmark, \
    delete_bookmark

from zeeguu_web.bookmarks import bookmarks_blueprint, login_first


@bookmarks_blueprint.route("/report_learned_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def post_report_learned_bookmark(bookmark_id):
    return report_learned_bookmark(bookmark_id)


@bookmarks_blueprint.route("/delete_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def delete(bookmark_id):
    return delete_bookmark(bookmark_id)


@bookmarks_blueprint.route("/starred_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def starred_word(bookmark_id):
    return star_bookmark(bookmark_id)


@bookmarks_blueprint.route("/unstarred_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def unstarred_word(bookmark_id):
    return unstar_bookmark(bookmark_id)
