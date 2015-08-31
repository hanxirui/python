'''
celery第二个例子，展示如何的应用中使用celery
celery -A proj worker -l info
'''

#--------------------------以下是test----------------------------

from proj.tasks import add

print(add(3,4))
res = add.delay(2, 2)
print(res.get(timeout=1))

s1 = add.subtask((2, 2), countdown=10)
res = s1.delay()
res.get()

# add options
s3 = add.s(2, 2, debug=True)
s3.delay(debug=False)   # debug is now False.


# Groups
group(add.s(i, i) for i in xrange(10))().get()

# Partial group
g = group(add.s(i) for i in xrange(10))
g(10).get()

# Chains  (4 + 4) * 8
chain(add.s(4, 4) | mul.s(8))().get()

# Chords
# A chord is a group with a callback:
chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()

# Routing
# Celery supports all of the routing facilities provided by AMQP, but it also supports simple routing where messages are sent to named queues.

# The CELERY_ROUTES setting enables you to route tasks by name and keep everything centralized in one location:

# app.conf.update(
#     CELERY_ROUTES = {
#         'proj.tasks.add': {'queue': 'hipri'},
#     },
# )
# You can also specify the queue at runtime with the queue argument to apply_async:

# >>> from proj.tasks import add
# >>> add.apply_async((2, 2), queue='hipri')
# You can then make a worker consume from this queue by specifying the -Q option:

# $ celery -A proj worker -Q hipri
# You may specify multiple queues by using a comma separated list, for example you can make the worker consume from both the default queue, and the hipri queue, where the default queue is named celery for historical reasons:

# $ celery -A proj worker -Q hipri,celery
# The order of the queues doesn’t matter as the worker will give equal weight to the queues.

# To learn more about routing, including taking use of the full power of AMQP routing, see the Routing Guide.