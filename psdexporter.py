#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
import time
import logging
from psd_tools import PSDImage
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog as watchdog
import re

class PSDExportEventHandler(watchdog.events.FileSystemEventHandler):
  """docstring for PSDExportEventHandler"""
  def __init__(self):
    super(PSDExportEventHandler, self).__init__()
    # self.arg = arg

  # def on_any_event(self, event):
  #   print('event:', event)

  def check_psd(self, path):
    # print(path)
    matchObj = re.match( r'\./(.*)\.(.*)', path, re.M|re.I)
    file_name = ''
    ext_name = ''
    if matchObj:
      file_name = matchObj.group(1)
      ext_name = matchObj.group(2)
      # print(file_name, ext_name)
      if ext_name.lower() == 'psd':
        self.export_png(path)
    # else:
    #   print('no match')
      # print()

  def export_png(self, path):
    
    psd = PSDImage.load(path)
    # print(psd.layers)
    for layer in psd.layers:
      
      matchObj = re.match( r'(.*):(.*)', layer.name, re.M|re.I)
      if matchObj:
        export_name = matchObj.group(1)
        map_type = matchObj.group(2)
        if map_type.lower() in ['normal', 'diffuse', 'specular', 'roughness']:
          print(export_name, map_type)
          layer_image = layer.as_PIL()
          layer_image.save('{0}_{1}.png'.format(export_name, map_type))
      else:
        print('No layers found.')

  def on_created(self, event):
    self.check_psd(event.src_path)
    # print('created event:', event)
  
  def on_modified(self, event):
    self.check_psd(event.src_path)
    

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
  path = sys.argv[1] if len(sys.argv) > 1 else '.'
  # event_handler = LoggingEventHandler()
  event_handler = PSDExportEventHandler()
  
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:

      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()
  observer.join()