import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# Each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.

# Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

	# __unicode__ on Python 2
    def __str__(self):
	    return self.question_text

    def was_published_recently(self):
	    return self.pub_date >= timezone.now()-datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # __unicode__ on Python 2
    def __str__(self):
	    return self.choice_text
