import urllib2 
from multiprocessing.dummy import Pool as ThreadPool 

urls = [
  'http://www.python.org', 
  'http://www.python.org/about/',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.jd.com',
  'http://www.taobao.com',
  'http://www.jobbole.com/',
  'http://www.csdn.net',
  'https://www.infoq.com',
  'http://www.sina.com.cn',
  'http://www.163.com',
  'http://www.baidu.com'
  # etc.. 
  ]

# Make the Pool of workers
pool = ThreadPool(10) 
# Open the urls in their own threads
# and return the results
results = pool.map(urllib2.urlopen, urls)
#close the pool and wait for the work to finish 
pool.close() 
pool.join() 