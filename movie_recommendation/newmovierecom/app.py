
# Building a web API around our engine using Flask
# Flask is a web microframework for Python. It is very easy to start up a web API, by just importing in 
# in our script and using some annotations to associate our service end-points with Python functions. 
# In our case we will wrap our RecommendationEngine methods around some of these end-points and interchange JSON formatted data 
# with the web client.
# In fact is so simple that we will show the whole app.py here, instead of going piece by piece.
from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    return json.dumps(top_ratings)
 
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    return json.dumps(ratings)
 
 
@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
 
    return json.dumps(ratings)
 
 
def create_app(spark_context, dataset_path):
    global recommendation_engine 
 
    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

# Basically we use the app as follows:
# We init the thing when calling create_app. Here the RecommendationEngine object is created and then 
# we associate the @main.route annotations defined above. Each annotation is defined by (see Flask docs):
# A route, that is its URL and may contain parameters between <>. They are mapped to the function arguments.
# A list of HTTP available methods.
# There are three of these annotations defined, that correspond with the three RecommendationEngine methods:
# GET /<user_id>/ratings/top get top recommendations from the engine.
# GET /<user_id>/ratings get predicted rating for a individual movie.
# POST /<user_id>/ratings add new ratings. The format is a series of lines (ending with the newline separator) 
# with movie_id and rating separated by commas. For example, the following file corresponds to the ten new user ratings 
# used as a example in the tutorial about building the model:
# `260,9
# 1,8
# 16,7
# 25,8
# 32,9
# 335,4
# 379,3
# 296,7
# 858,10
# 50,8`



























