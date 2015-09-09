
# multiprocessing.dummy 模块与 multiprocessing 模块的区别： dummy 模块是多线程，而 multiprocessing 是多进程， api 都是通用的。 
# 所有可以很方便将代码在多线程和多进程之间切换。

# import urllib2
import time
from urllib.request import urlopen
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

start = time.time()
results = map(urlopen, urls)
# python3中map都改为延迟运算了，不取值不进行实际操作
for content in results:
   print(content)

print ('Normal:', time.time() - start)

start2 = time.time()

# 开8个 worker，没有参数时默认是 cpu 的核心数
# Make the Pool of workers
pool = ThreadPool(processes=4) 
# Open the urls in their own threads
# and return the results
results2 = pool.map(urlopen, urls)
for content in results2:
   print(content)
#close the pool and wait for the work to finish 
pool.close() 
pool.join() 
print ('Thread Pool:', time.time() - start2)