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
        'You are tying to install hlpl_character on Python version {}.\n'
        'Please install hlpl_character in Python 3 instead.'.format(
            platform.python_version()
        )
    )
    
config = configparser.ConfigParser()
current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'hlpl_character/setup.cfg')
config.read(config_file_path)

VERSION = config['hlpl_character']['version']
AUTHOR = config['hlpl_character']['author']
AUTHOR_EMAIL = config['hlpl_character']['email']
URL = config['hlpl_character']['url']


projects_urls={}
for i in range(4,len(list(config['hlpl_character'].keys()))):
    x=list(config['hlpl_character'].keys())[i]
    y=x
    if i>3:
       y=y[0:len(y)-4]
    projects_urls[y]=config['hlpl_character'][x]
    

setup (name='hlpl_character', version=VERSION,
      description='hlpl_character simulates human life',
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
      keywords=['hlpl_character', 'hlpl character', 'hlpl-character', 'human life simulator', 'NLP', 'hlpl'],
      package_dir={'hlpl_character': 'hlpl_character',},
      packages=['hlpl_character',],
      install_requires=[],         
      include_package_data=True,
      entry_points ={
        'console_scripts': [
                'hlpl_character = hlpl_character.__main__:main',
            ]},   
      classifiers=[
          'Framework :: Robot Framework',
          'Framework :: Robot Framework :: Library',
          'Framework :: Robot Framework :: Tool',
          'Natural Language :: Arabic',
          'Natural Language :: English',
          ],
                  
    );
