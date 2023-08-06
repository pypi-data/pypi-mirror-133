"""
Miner for repos without a specific miner.

"""

import os
from domainmodelexaminer import utilities as util
from domainmodelexaminer import docker_miner as dminer
from domainmodelexaminer import language as language

IGNORE_FILE_EXT = ['.txt','.html','.css','.json','xml','.csv','.pdf','.yml',
       '.yaml','.ini', '.png', '.store', '.mp3', '.jar', '.webp',
       '.so', '.pack', '','.db', '.idx', '.jks', '.cert', '.der',
       '.ogg', '.ttf']

class ArbitraryRepoMiner:
  """
  Non-specific repo miner.
  """
  def __init__(self, repo_path, repo_name, lang, about_desc, owner_info, return_comments: bool = True):
    self.repo_path = repo_path
    self.repo_name = repo_name
    self.lang = language.languages[lang] if lang != None else 'unknown'

    if os.name == str('nt'):
      self.sep = '\\'
    else:
      self.sep = '/'

    self.yaml_dict = dict()
    self.yaml_dict['language'] = self.lang
    self.yaml_dict['owner'] = owner_info
    self.yaml_dict['about'] = about_desc
    self.return_comments = return_comments

    self.mine_files()


  def mine_files(self):
    data_files = set()
    docker = None
    output_files = set() # organize by source, output_file path
    readmes = []
    urls = set()

    for root, dirs, files in os.walk(self.repo_path):
       for file in files:
         filename, file_ext = os.path.splitext(file)
         full_filename = root + self.sep + file

         if file == 'Dockerfile':
           docker = dict(docker_entrypoint=dminer.report_dockerfile(
              full_filename))
         elif file.lower().startswith('readme'):
           # load entire readme until a better desription is generated
           with open(full_filename, 'r', encoding='utf8') as readme_file:
             readmes.append({ full_filename: readme_file.read()})
           # add urls, then further processing
           temp_list = util.get_urls(full_filename)
           if temp_list:
             urls.update(temp_list)
           # file_names
           data_files.update(util.get_filenames(full_filename))

         elif file_ext not in IGNORE_FILE_EXT:
           # urls
           temp_list = util.get_urls(full_filename)
           if temp_list:
             urls.update(temp_list)

           # file_names
           data_files.update(util.get_filenames(full_filename))

    ## Remove rep path from readme filenames.
    readmes = util.replace_cp_in_dict_list(readmes, self.repo_path)

    # Add the collected data to the dictionary.
    self.yaml_dict['docker_entrypoint'] = docker
    self.yaml_dict['data_files'] = sorted(data_files)
    self.yaml_dict['output_files'] = util.group_tuple_pairs(output_files)
    self.yaml_dict['urls'] = util.group_tuple_pairs(urls)
    self.yaml_dict['readmes'] = readmes
