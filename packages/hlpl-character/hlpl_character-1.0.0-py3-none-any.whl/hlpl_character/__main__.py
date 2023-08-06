
import configparser
import sys
import os

def get_hlpl_character_version(case):
    config = configparser.ConfigParser()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, 'setup.cfg')
    config.read(config_file_path)
    if case=='version':
       return config['hlpl_character']['version']
    if case=='else':
       return config['hlpl_character']['version']+'\n'+config['hlpl_character']['author']+'\n'+config['hlpl_character']['email']+'\n'+config['hlpl_character']['url']+'\n'
       
 
    
def main():
    if 'version' in sys.argv:
        print('\n'+get_hlpl_character_version('version'))
    else:
        print('\n'+get_hlpl_character_version('else')+'\n'+'hlpl_character under developement, it will be released next versions of HLPL')