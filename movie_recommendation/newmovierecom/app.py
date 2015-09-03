#/usr/bin/env python3
#-*- coding:utf-8 -*-
complete_dataset_url = 'http://files.grouplens.org/datasets/movielens/ml-latest.zip'
small_dataset_url = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'

# We also need to define download locations.
import os

# datasets_path = os.path.join('..', 'datasets')
datasets_path = os.path.join('file:///Users/hanxirui/Documents/workspace/github/python/movie_recommendation', 'datasets')

# complete_dataset_path = os.path.join(datasets_path, 'ml-latest.zip')
# small_dataset_path = os.path.join(datasets_path, 'ml-latest-small.zip')

# Now we can proceed with both downloads.
import urllib
import urllib.request

# small_f = urllib.request.urlretrieve(small_dataset_url, small_dataset_path)
# complete_f = urllib.request.urlretrieve(complete_dataset_url, complete_dataset_path)

# Both of them are zip files containing a folder with ratings, movies, etc. We need to extract them into its individual folders so we can use each file later on.
import zipfile

# with zipfile.ZipFile(small_dataset_path, "r") as z:
#     z.extractall(datasets_path)

# with zipfile.ZipFile(complete_dataset_path, "r") as z:
#     z.extractall(datasets_path)

# -------------------------------finished download and extract all data files-------------------------------
# ----------------------------------用小数据测试一下程序----------------------------------
# ./bin/spark-submit /Users/hanxirui/Documents/workspace/github/python/movie_recommendation/newmovierecom/app.py
from pyspark import SparkContext
sc = SparkContext(appName="movierecommen")
# So let's load the raw ratings data. We need to filter out the header, included in each file.
small_ratings_file = os.path.join(datasets_path, 'ml-latest-small', 'ratings.csv')

small_ratings_raw_data = sc.textFile(small_ratings_file)
small_ratings_raw_data_header = small_ratings_raw_data.take(1)[0]
# Now we can parse the raw data into a new RDD.

small_ratings_data = small_ratings_raw_data.filter(lambda line: line!=small_ratings_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1],tokens[2])).cache()
# For illustrative purposes, we can take the first few lines of our RDD to see the result. In the final script we don't call any Spark action (e.g. take) until needed, since they trigger actual computations in the cluster.

print(small_ratings_data.take(3))
# Out[5]:
# [(u'1', u'6', u'2.0'), (u'1', u'22', u'3.0'), (u'1', u'32', u'2.0')]
# We proceed in a similar way with the movies.csv file.

small_movies_file = os.path.join(datasets_path, 'ml-latest-small', 'movies.csv')

small_movies_raw_data = sc.textFile(small_movies_file)
small_movies_raw_data_header = small_movies_raw_data.take(1)[0]

small_movies_data = small_movies_raw_data.filter(lambda line: line!=small_movies_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1])).cache()
    
print(small_movies_data.take(3))
# Out[6]:
# [(u'1', u'Toy Story (1995)'),
#  (u'2', u'Jumanji (1995)'),
#  (u'3', u'Grumpier Old Men (1995)')]
# The following sections introduce Collaborative Filtering and explain how to use Spark MLlib to build a recommender model. We will close the tutorial by explaining how a model such this is used to make recommendations, and how to persist it for later use (e.g. in our Python/flask web-service).

# Collaborative Filtering
# In Collaborative filtering we make predictions (filtering) about the interests of a user by collecting preferences or taste information from many users (collaborating). The underlying assumption is that if a user A has the same opinion as a user B on an issue, A is more likely to have B's opinion on a different issue x than to have the opinion on x of a user chosen randomly.
# The image below (from Wikipedia) shows an example of collaborative filtering. At first, people rate different items (like videos, images, games). Then, the system makes predictions about a user's rating for an item not rated yet. The new predictions are built upon the existing ratings of other users with similar ratings with the active user. In the image, the system predicts that the user will not like the video.

# Spark MLlib library for Machine Learning provides a Collaborative Filtering implementation by using Alternating Least Squares. The implementation in MLlib has the following parameters:
# numBlocks is the number of blocks used to parallelize computation (set to -1 to auto-configure).
# rank is the number of latent factors in the model.
# iterations is the number of iterations to run.
# lambda specifies the regularization parameter in ALS.
# implicitPrefs specifies whether to use the explicit feedback ALS variant or one adapted for implicit feedback data.
# alpha is a parameter applicable to the implicit feedback variant of ALS that governs the baseline confidence in preference observations.
# Selecting ALS parameters using the small dataset
# In order to determine the best ALS parameters, we will use the small dataset. We need first to split it into train, validation, and test datasets.
# In [7]:
training_RDD, validation_RDD, test_RDD = small_ratings_data.randomSplit([6, 2, 2], seed=0)
validation_for_predict_RDD = validation_RDD.map(lambda x: (x[0], x[1]))
test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))

#---------------------------------- Now we can proceed with the training phase. ----------------------------------
from pyspark.mllib.recommendation import ALS
import math

seed = 5
iterations = 10
regularization_parameter = 0.1
ranks = [4, 8, 12]
errors = [0, 0, 0]
err = 0
tolerance = 0.02

min_error = float('inf')
best_rank = -1
best_iteration = -1
for rank in ranks:
    model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                      lambda_=regularization_parameter)
    predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
    rates_and_preds = validation_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
    error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
    errors[err] = error
    err += 1
    print('For rank %s the RMSE is %s' % (rank, error))
    if error < min_error:
        min_error = error
        best_rank = rank

print('The best model was trained with rank %s' % best_rank)

# For rank 4 the RMSE is 0.963681878574
# For rank 8 the RMSE is 0.96250475933
# For rank 12 the RMSE is 0.971647563632
# The best model was trained with rank 8
# But let's explain this a little bit. First, let's have a look at how our predictions look.
# In [9]:
# predictions.take(3)
# Out[9]:
# [((32, 4018), 3.280114696166238),
#  ((375, 4018), 2.7365714977314086),
#  ((674, 4018), 2.510684514310653)]
# Basically we have the UserID, the MovieID, and the Rating, as we have in our ratings dataset. In this case the predictions third element, the rating for that movie and user, is the predicted by our ALS model.
# Then we join these with our validation data (the one that includes ratings) and the result looks as follows:
# In [10]:
# rates_and_preds.take(3)
# Out[10]:
# [((558, 788), (3.0, 3.0419325487471403)),
#  ((176, 3550), (4.5, 3.3214065001580986)),
#  ((302, 3908), (1.0, 2.4728711204440765))]
# To that, we apply a squared difference and the we use the mean() action to get the MSE and apply sqrt.
# Finally we test the selected model.


# For testing data the RMSE is 0.972342381898
# Using the complete dataset to build the final model
# In order to build our recommender model, we will use the complete dataset. Therefore, we need to process it the same way we did with the small dataset.

#---------------------------------- 下面开始玩儿真的了 ----------------------------------
# Load the complete dataset file
complete_ratings_file = os.path.join(datasets_path, 'ml-latest', 'ratings.csv')
complete_ratings_raw_data = sc.textFile(complete_ratings_file)
complete_ratings_raw_data_header = complete_ratings_raw_data.take(1)[0]

# Parse
# complete_ratings_data = complete_ratings_raw_data.filter(lambda line: line!=complete_ratings_raw_data_header)\
#     .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),int(tokens[1]),float(tokens[2]))).cache()
    
# print("There are %s recommendations in the complete dataset" % (complete_ratings_data.count()))
# There are 21063128 recommendations in the complete dataset
# Now we are ready to train the recommender model.
training_RDD, test_RDD = complete_ratings_data.randomSplit([7, 3], seed=0)

complete_model = ALS.train(training_RDD, best_rank, seed=seed, 
                           iterations=iterations, lambda_=regularization_parameter)

# Now we test on our testing set.
# In [14]:
test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))

predictions = complete_model.predictAll(test_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
rates_and_preds = test_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
    
print('For testing data the RMSE is %s' % (error))
# For testing data the RMSE is 0.82183583368
# We can see how we got a more accurate recommender when using a much larger dataset.


# How to make recommendations
# Although we aim at building an on-line movie recommender, now that we know how to have our recommender model ready, we can give it a try providing some movie recommendations. This will help us coiding the recommending engine later on when building the web service, and will explain how to use the model in any other circumstances.
# When using collaborative filtering, getting recommendations is not as simple as predicting for the new entries using a previously generated model. Instead, we need to train again the model but including the new user preferences in order to compare them with other users in the dataset. That is, the recommender needs to be trained every time we have new user ratings (although a single model can be used by multiple users of course!). This makes the process expensive, and it is one of the reasons why scalability is a problem (and Spark a solution!). Once we have our model trained, we can reuse it to obtain top recomendations for a given user or an individual rating for a particular movie. These are less costly operations than training the model itself.
# So let's first load the movies complete file for later use.

complete_movies_file = os.path.join(datasets_path, 'ml-latest', 'movies.csv')
complete_movies_raw_data = sc.textFile(complete_movies_file)
complete_movies_raw_data_header = complete_movies_raw_data.take(1)[0]

# Parse
complete_movies_data = complete_movies_raw_data.filter(lambda line: line!=complete_movies_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),tokens[1],tokens[2])).cache()

complete_movies_titles = complete_movies_data.map(lambda x: (int(x[0]),x[1]))
    
print("There are %s movies in the complete dataset" % (complete_movies_titles.count()))


# There are 27303 movies in the complete dataset
# Another thing we want to do, is give recommendations of movies with a certain minimum number of ratings. For that, we need to count the number of ratings per movie.

def get_counts_and_averages(ID_and_ratings_tuple):
    nratings = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1]))/nratings)

movie_ID_with_ratings_RDD = (complete_ratings_data.map(lambda x: (x[1], x[2])).groupByKey())
movie_ID_with_avg_ratings_RDD = movie_ID_with_ratings_RDD.map(get_counts_and_averages)
movie_rating_counts_RDD = movie_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))

# Adding new user ratings
# Now we need to rate some movies for the new user. We will put them in a new RDD and we will use the user ID 0, that is not assigned in the MovieLens dataset. Check the dataset movies file for ID to Tittle assignment (so you know what movies are you actually rating).

new_user_ID = 0

# The format of each line is (userID, movieID, rating)
new_user_ratings = [
     (0,260,9), # Star Wars (1977)
     (0,1,8), # Toy Story (1995)
     (0,16,7), # Casino (1995)
     (0,25,8), # Leaving Las Vegas (1995)
     (0,32,9), # Twelve Monkeys (a.k.a. 12 Monkeys) (1995)
     (0,335,4), # Flintstones, The (1994)
     (0,379,3), # Timecop (1994)
     (0,296,7), # Pulp Fiction (1994)
     (0,858,10) , # Godfather, The (1972)
     (0,50,8) # Usual Suspects, The (1995)
    ]
new_user_ratings_RDD = sc.parallelize(new_user_ratings)
print('New user ratings: %s' % new_user_ratings_RDD.take(10))

# New user ratings: [(0, 260, 9), (0, 1, 8), (0, 16, 7), (0, 25, 8), (0, 32, 9), (0, 335, 4), (0, 379, 3), (0, 296, 7), (0, 858, 10), (0, 50, 8)]
# Now we add them to the data we will use to train our recommender model. We use Spark's union() transformation for this.

complete_data_with_new_ratings_RDD = complete_ratings_data.union(new_user_ratings_RDD)
# And finally we train the ALS model using all the parameters we selected before (when using the small dataset).

from time import time

t0 = time()
new_ratings_model = ALS.train(complete_data_with_new_ratings_RDD, best_rank, seed=seed, 
                              iterations=iterations, lambda_=regularization_parameter)
tt = time() - t0

print("New model trained in %s seconds" % round(tt,3))
# New model trained in 56.61 seconds
# It took some time. We will need to repeat that every time a user add new ratings. Ideally we will do this in batches, and not for every single rating that comes into the system for every user.

# Getting top recommendations
# Let's now get some recommendations! For that we will get an RDD with all the movies the new user hasn't rated yet. We will them together with the model to pr

# filter
new_user_unrated_movies_RDD = (complete_movies_data.filter(lambda x: x[1]!=new_user_ID)
                      .map(lambda x: (new_user_ID, x[0])))

# Use the input RDD, new_user_unrated_movies_RDD, with new_ratings_model.predictAll() to predict new ratings for the movies
new_user_recommendations_RDD = new_ratings_model.predictAll(new_user_unrated_movies_RDD)
# We have our recommendations ready. Now we can print out the 25 movies with the highest predicted ratings. And join them with the movies RDD to get the titles, and ratings count in order to get movies with a minimum number of counts. First we will do the join and see what does the result looks like.

# Transform new_user_recommendations_RDD into pairs of the form (Movie ID, Predicted Rating)
new_user_recommendations_rating_RDD = new_user_recommendations_RDD.map(lambda x: (x.product, x.rating))
new_user_recommendations_rating_title_and_count_RDD = \
    new_user_recommendations_rating_RDD.join(complete_movies_titles).join(movie_rating_counts_RDD)
new_user_recommendations_rating_title_and_count_RDD.take(3)



# [(87040, ((6.834512984654888, u'"Housemaid'), 14)),
#  (8194, ((5.966704041954459, u'Baby Doll (1956)'), 79)),
#  (130390, ((0.6922328127396398, u'Contract Killers (2009)'), 1))]
# So we need to flat this down a bit in order to have (Title, Rating, Ratings Count).
# In [23]:
new_user_recommendations_rating_title_and_count_RDD = \
    new_user_recommendations_rating_title_and_count_RDD.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))

# Finally, get the highest rated recommendations for the new user, filtering out movies with less than 25 ratings.

top_movies = new_user_recommendations_rating_title_and_count_RDD.filter(lambda r: r[2]>=25).takeOrdered(25, key=lambda x: -x[1])

print ('TOP recommended movies (with more than 25 reviews):\n%s' %
        '\n'.join(map(str, top_movies)))


# Getting individual ratings
# Another useful usecase is getting the predicted rating for a particular movie for a given user. The process is similar to the previous retreival of top recommendations but, instead of using predcitAll with every single movie the user hasn't rated yet, we will just pass the method a single entry with the movie we want to predict the rating for.

my_movie = sc.parallelize([(0, 500)]) # Quiz Show (1994)
individual_movie_rating_RDD = new_ratings_model.predictAll(new_user_unrated_movies_RDD)
individual_movie_rating_RDD.take(1)

# Not very likely that the new user will like that one... Obviously we can include as many movies as we need in that list!
# Persisting the model
# Optionally, we might want to persist the base model for later use in our on-line recommendations. Although a new model is generated everytime we have new user ratings, it might be worth it to store the current one, in order to save time when starting up the server, etc. We might also save time if we persist some of the RDDs we have generated, specially those that took longer to process. For example, the following lines save and load a ALS model.


from pyspark.mllib.recommendation import MatrixFactorizationModel

model_path = os.path.join(datasets_path, 'models', 'movie_lens_als')

# Save and load model
model.save(sc, model_path)
same_model = MatrixFactorizationModel.load(sc, model_path)

# Among other things, you will see in your filesystem that there are folder with product and user data into Parquet format files.
# Genre and other fields
# We havent used the genre and timestamp fields in order to simplify the transformations and the whole tutorial. Incorporating them doesn't reprensent any problem. A good use could be filtering recommendations by any of them (e.g. recommendations by genre, or recent recommendations) like we have done with the minimum number of ratings.




































