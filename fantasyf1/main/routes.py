from flask import render_template, request, Blueprint, url_for
from fantasyf1.models import Post
from fantasyf1.main.utils import get_driver_standings, get_last_race_results, get_constructor_standings, get_next_race_data
from fantasyf1 import cache

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    drivers = get_last_race_results()
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4, page=page)
    return render_template("home.html", posts=posts, drivers=drivers)


@main.route("/about")
def about():
    return render_template("about.html", title="About")

@main.route("/scoreboard")
def scoreboard():
    pass

@main.route("/standings")
def standings():
    drivers = get_driver_standings()
    constructors = get_constructor_standings()
    return render_template("standings.html", title="Standings", drivers=drivers, constructors=constructors)

@main.route("/next_race")
@cache.cached(timeout=50)
def next_race():
    data = get_next_race_data()
    return render_template("next_race.html", title="Next race", data=data)