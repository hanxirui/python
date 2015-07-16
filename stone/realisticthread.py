'''
A more realistic thread pool example
'''

import time
import threading
import Queue
import urllib2

class Consumer(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self._queue = queue

	def run(self):
		while True:
			content = self._queue.get()
			if isinstance(content,str) and content == 'quit':
				break
			print content
			response = urllib2.urlopen(content)
		print "Bye bye!"

def Producer():
	urls = ['http://www.python.org','http://www.yahoo.com',
			'http://www.scala.org','http://www.oracle.com']
	queue = Queue.Queue()
	worker_threads = build_worker_pool(queue,4)
	start_time = time.time()

	for url in urls:
		queue.put(url)

	for worker in worker_threads:
		queue.put('quit')

	for worker in worker_threads:
		worker.join()

	print 'Done! Time taken:{}'.format(time.time()-start_time)

def build_worker_pool(queue,size):
	workers = []
	for _ in range(size):
		worker = Consumer(queue)
		worker.start()
		workers.append(worker)

	return workers

if __name__=='__main__':
	Producer()



















