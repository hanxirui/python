from multiprocessing import Pool 
from PIL import Image
import os

'''生成缩略图，使用的是Pillow，这个支持Python3，原生的PIL目前不支持python3
pip install Pillow
https://github.com/python-pillow/Pillow
http://pillow.readthedocs.org/handbook/tutorial.html'''

SIZE = (75,75)
SAVE_DIRECTORY = 'thumbs'

def get_image_paths(folder):
  return (os.path.join(folder, f) 
      for f in os.listdir(folder) 
      if 'jpg' in f)

def create_thumbnail(filename): 
  im = Image.open(filename)
  im.thumbnail(SIZE, Image.ANTIALIAS)
  base, fname = os.path.split(filename) 
  save_path = os.path.join(base, SAVE_DIRECTORY, fname)
  im.save(save_path)

if __name__ == '__main__':
  folder = os.path.abspath(
    '/Users/hanxirui/Documents/workspace/github/python/stone/jpg')
  os.mkdir(os.path.join(folder, SAVE_DIRECTORY))

  images = get_image_paths(folder)

  pool = Pool()
  pool.map(create_thumbnail, images)
  pool.close() 
  pool.join()