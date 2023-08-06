#! /usr/bin/python 
from setuptools  import setup
import os
import sys
import platform
import configparser

from io import open
# to install type:
# python setup.py install --root=/
LONG_DESCRIPTION=open('README.md','r',encoding='utf8').read()        
        
if sys.version_info[0] < 3:
    raise Exception(
        'You are tying to install hlpl_photographer on Python version {}.\n'
        'Please install hlpl_photographer in Python 3 instead.'.format(
            platform.python_version()
        )
    )
    
config = configparser.ConfigParser()
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'hlpl_photographer/setup.cfg')
config.read(config_file_path)

VERSION = config['hlpl_photographer']['version']
AUTHOR = config['hlpl_photographer']['author']
AUTHOR_EMAIL = config['hlpl_photographer']['email']
URL = config['hlpl_photographer']['url']


projects_urls={}
for i in range(4,len(list(config['hlpl_photographer'].keys()))):
    x=list(config['hlpl_photographer'].keys())[i]
    y=x
    if i>3:
       y=y[0:len(y)-4]
    projects_urls[y]=config['hlpl_photographer'][x]
    

setup (name='hlpl_photographer', version=VERSION,
      description='hlpl_photographer simulates nature',
      long_description_content_type='text/markdown',  
      long_description = LONG_DESCRIPTION,       
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=URL+'/download/',
      project_urls=projects_urls,      
      python_requires='>=3, <=3.9',
      license='MIT',
      platform="OS independent",
      keywords=['hlpl_photographer', 'hlpl photographer', 'hlpl-photographer', 'nature simulator', 'NLP', 'hlpl'],
      package_dir={'hlpl_photographer': 'hlpl_photographer',},
      packages=['hlpl_photographer',],
      install_requires=[],         
      include_package_data=True,
      entry_points ={
        'console_scripts': [
                'hlpl_photographer = hlpl_photographer.__main__:main',
            ]},   
      classifiers=[
          'Framework :: Robot Framework',
          'Framework :: Robot Framework :: Library',
          'Framework :: Robot Framework :: Tool',
          'Natural Language :: Arabic',
          'Natural Language :: English',
          ],
                  
    );
