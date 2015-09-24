# Deploying a WSGI server using CherryPy
# Among other things, the CherryPy framework features a reliable, HTTP/1.1-compliant, WSGI thread-pooled webserver. 
# It is also easy to run multiple HTTP servers (e.g. on multiple ports) at once. All this makes it a perfect candidate 
# for an easy to deploy production web server for our on-line recommendation service.
# The use that we will make of the CherryPy server is relatively simple. Again we will show here the complete server.py 
# script and then explain it a bit.
import time, sys, cherrypy, os
from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf
 
def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("movie_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
    sc = SparkContext(conf=conf, pyFiles=['engine.py', 'app.py'])
 
    return sc
 
 
def run_server(app):
 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
 
 
if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    dataset_path = os.path.join('datasets', 'ml-latest')
    app = create_app(sc, dataset_path)
 
    # start web server
    run_server(app)

# This is pretty standard use of CherryPy. If we have a look at the __main__ entry point, we do three things:
# Create a spark context as defined in the function init_spark_context, passing aditional Python modules there.
# Create the Flask app calling the create_app we defined in app.py.
# Run the server itself.
# See the following section about starting the server.

# Running the server with Spark
# In order to have the server running while being able to access a Spark context and cluster, we need to submit the server.py 
# file to pySpark by using spark-submit. The different parameters when using this command are better explained in the Spark 
# docummentaion. In our case, we will use something like the following.
# ~/spark-1.3.1-bin-hadoop2.6/bin/spark-submit --master spark://169.254.206.2:7077 --total-executor-cores 14 --executor-memory
# 6g server.py
# The important bits are:
# Use spark-submit and not pyspark directly.
# The --master parameters must point to your Spark cluster setup (can be local).
# You can pass additional configuration parameters such as --total-executor-cores and --executor-memory
# You will see an output like the following:
# INFO:engine:Starting up the Recommendation Engine: INFO:engine:Loading Ratings data... INFO:engine:Loading Movies data... 
# INFO:engine:Counting movie ratings... INFO:engine:Training the ALS model... ... More Spark and CherryPy logging INFO:engine:
# ALS model built! [05/Jul/2015:14:06:29] ENGINE Bus STARTING [05/Jul/2015:14:06:29] ENGINE Started monitor 
# thread 'Autoreloader'. [05/Jul/2015:14:06:29] ENGINE Started monitor thread '_TimeoutMonitor'. [05/Jul/2015:14:06:29] 
# ENGINE Serving on http://0.0.0.0:5432 [05/Jul/2015:14:06:29] ENGINE Bus STARTED
# Some considerations when using multiple Scripts and Spark-submit
# There are two issues we need to work around when using Spark in a deployment like this. The first one is that a Spark 
# cluster is a distrubuted environment of Workers orchestrated from the Spark Master where the Python script is launched. 
# This means that the master is the only one with access to the submitted script and local additional files. If we want the 
# workers to be able to access additional imported Python moules, they either have to be part of our Python distributuon or 
# we need to pass them implicitly. We do this by using the pyFiles=['engine.py', 'app.py'] parameter when creating the 
# SparkContext object.
# The second issue is related with the previous one but is a bit more tricky. In Spark, when using transformations (e.g. 
# 	map on an RDD), we cannot make reference to other RDDs or objects that are not globally available in the execution 
# context. For example, we cannot make reference to a class instance variables. Because of this, we have defined all 
# the functions that are passed to RDD transformations outside the RecommendationEgine class.
# Trying the service
# Let's now give the service a try, using the same data we used on the tutorial about building the model. That is, 
# first we are going to add ratings, and then we are going to get top ratings and individual ratings.
# POSTing new ratings
# So first things first, we need to have our service runing as explained in the previous section. Once is running, 
# we will use curl to post new ratings from the shell. If we have the file user_ratings.file (see Getting the source 
# 	code below) in the current folder, just execute the following command.
# curl --data-binary @user_ratings.file http://









