"""
Miner for R repos.

What is a Pirate's favorite programming language?
You'd think it is Rrrrr, but it would be the C.

"""

import os
from domainmodelexaminer import utilities as util
from domainmodelexaminer import docker_miner as dminer
import re

class RRepoMiner:
  """
  R-specific repo miner.
  """

  def __init__(self, repo_path, repo_name, about_desc, owner_info, return_comments: bool = True):
    self.repo_path = repo_path
    self.repo_name = repo_name

    if os.name == str('nt'):
      self.sep = '\\'
    else:
      self.sep = '/'

    self.yaml_dict = dict()
    self.yaml_dict['language'] = 'R'
    self.yaml_dict['owner'] = owner_info
    self.yaml_dict['about'] = about_desc
    self.return_comments = return_comments

    self.mine_files()

  def get_libraries(self, filename):
    """
    Return set of libraries.

    Examples:

    * install.packages("tidyr", repos = repo)

    * library(tidyr)

    * x<-c("plyr", "psych", "tm")
    * lapply(x, require, character.only = TRUE)

    * lapply(c("gganimate", "tidyverse", "gapminder"), require, character.only = TRUE)

    * if easypackages is installed:
    ** packages("dplyr", "ggplot2", "RMySQL", "data.table")
    ** my_packages <- c("dplyr", "ggplot2", "RMySQL", "data.table")
    ** libraries(my_packages)
    ** libraries("dplyr", "ggplot2", "RMySQL", "data.table")

    """
    libraries = set()
    last_c_line = ''
    with open(filename, 'r', encoding="utf8") as f:
      for line in f:
        line = line.strip(' ') # strip spaces in case of wierd formatting
        if line.startswith(tuple(['library','install.packages','require'])):
          # standard example e.g. library(tidyr)
          library = line.strip().split('(')[1].split(',')[0].split(')')[0]
          libraries.add(library.strip('"').strip('\''))
        elif line.startswith('lapply(c(') and ('library' in line or 'require' in line):
          # using lapply to pass array of libraries to function
          # e.g.: lapply(c("gganimate", "tidyverse", "gapminder"), require, character.only = TRUE)
          # add everything between single and double quotes
          libraries = libraries | set(re.findall(r"['\"](.*?)['\"]", line))
        elif line.startswith('lapply(') and ('library' in line or 'require' in line):
          # same as above but the libraries have been assigned to a var
          # tricky - try to use last_c_line to identify library names

          # id var name in line and last_c_line; load libs if a match
          #'x<-c("plyr", "psych", "tm")'
          last_c_var_name = last_c_line.split('=')[0] if '=' in last_c_line else last_c_line.split('<-')[0] if '<-' in last_c_line else None

          #'lapply(x, require, character.only = TRUE)'
          line_var_name = line.split('(')[1].split(',')[0]

          if last_c_var_name.strip() == line_var_name.strip() and not line_var_name == None:

            # id'd a lapply(var_name, requires or library; add the parsed library names
            libraries = libraries | set(re.findall(r"['\"](.*?)['\"]", last_c_line))

        elif 'c(' in line and ('=' in line or '<-' in line):
          # record last line with a variable assigned to a vector creator (c)
          last_c_line = line


    return libraries

  def mine_files(self):
    ## Probably move to another unit/class.
    ## Try to id the entry point file based on the identified language.
    ## Requires Iterating again, which makes this slow.
    comments = []
    data_files = set()
    docker = None
    libraries = set()
    mainfiles = []
    output_files = set() # organize by source, output_file path
    readmes = []
    urls = set()
    for root, dirs, files in os.walk(self.repo_path):
      for file in files:
        filename, file_ext = os.path.splitext(file)
        full_filename = root + self.sep + file

        if file_ext == '.R':
          if util.textfile_contains(full_filename, "commandArgs"):
            mainfiles.append(full_filename)

          # Collate all libraries
          libraries.update(self.get_libraries(full_filename))

          # output files
          temp_list = util.get_output2(full_filename)
          if temp_list:
            output_files.update(temp_list)

          # urls
          temp_list = util.get_urls(full_filename)
          if temp_list:
            urls.update(temp_list)

          # comments
          if self.return_comments:
            comments.append({file: util.get_comments(full_filename) })

          # file_names
          data_files.update(util.get_filenames(full_filename))

        elif file == 'Dockerfile':
          docker = dict(docker_entrypoint=dminer.report_dockerfile(full_filename))

        elif file.lower().startswith('readme'):

          # load entire readme until a better desription is generated
          with open(full_filename, 'rt', encoding='utf8') as readme_file:
            readmes.append({ full_filename: readme_file.read()})

          # add urls, then further processing
          temp_list = util.get_urls(full_filename)
          if temp_list:
            urls.update(temp_list)
          util.get_filenames(full_filename)

          # file_names
          data_files.update(util.get_filenames(full_filename))

    # Remove common path from filenames and output.
    cp = util.commonprefix(mainfiles)
    mainfiles = list(map(lambda s: s.replace(cp,''), mainfiles ))

    ## Report imports and model types.
    model_types = sorted(util.get_model_types_from_libraries(libraries, self.sep, 'R'))

    ## Sort libraries.
    libraries = sorted(libraries)

    # Remove common path from source files in output_files
    output_files = util.replace_cp_in_tuple_set(output_files, cp)

    # Reorganize output_files items in tuple as dict.
    output_files = util.reorg_output_files(output_files)

    # Remove common path from readme and about (same as readme) filenames.
    readmes = util.replace_cp_in_dict_list(readmes, cp)

    # Add the collected data to the dictionary.
    self.yaml_dict['docker_entrypoint'] = docker
    self.yaml_dict['model_types'] = model_types
    self.yaml_dict['libraries'] = libraries
    self.yaml_dict['main_files'] = mainfiles
    self.yaml_dict['data_files'] = sorted(data_files)
    self.yaml_dict['output_files'] = util.group_tuple_pairs(output_files)
    self.yaml_dict['urls'] = util.group_tuple_pairs(urls)
    self.yaml_dict['readmes'] = readmes
    self.yaml_dict['comments'] = comments
