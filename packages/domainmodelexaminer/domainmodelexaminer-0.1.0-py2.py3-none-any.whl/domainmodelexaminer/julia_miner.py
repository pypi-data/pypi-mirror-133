"""Miner for Julia repos."""

import os
from domainmodelexaminer import utilities as util
from domainmodelexaminer import docker_miner as dminer

class JuliaRepoMiner:
  """Julia-specific repo miner."""

  def __init__(self, repo_path, repo_name, about_desc, owner_info, return_comments: bool = True):
    self.repo_path = repo_path
    self.repo_name = repo_name

    if os.name == str('nt'):
      self.sep = '\\'
    else:
      self.sep = '/'

    self.yaml_dict = dict()
    self.yaml_dict['language'] = 'Julia'
    self.yaml_dict['owner'] = owner_info
    self.yaml_dict['about'] = about_desc
    self.return_comments = return_comments
    
    self.mine_files()

  def get_imports(self, filename, root_dirs=()):
    """
    Return unique set of libraries.

    1. using NiceStuff
    2. import NiceStuff
    3. using NiceStuff, NaughtyStuff
    4. import NiceStuff, NaughtyStuff
    5. using NiceStuff: nice, DOG, NiceStuff
    6. import NiceStuff: nice
    7. ignore: using .AgentsModule, .ModelModule, .RunModule

    """
    imports = set()
    with open(filename, 'r', encoding="utf8") as f:
      for line in f:
        line = line.split('#')[0].strip().strip('!')  # remove inline comments and !
        if line.startswith('using') or line.startswith('import'):
          # strip import, using statements
          line = line.replace('using', '').replace('import', '').strip()
          if ':' in line:
            sa = [x.strip() for x in line.split(':')]
            module = sa[0]
            if not module.startswith('.'):  # ignore rep libraries
              # splite line into array with each item prefixed by "{module}.".
              sa = [".".join([module, x.strip()]) for x in sa[1].split(',')]
              imports.update(sa)
            else:
              pass
          else:
            # parse csv modules, ignore those starting with ".".
            sa = [x.strip() for x in line.split(',') if not x.strip().startswith('.')]
            imports.update(sa)
    return imports


  def mine_files(self):
    comments = []
    data_files = set()
    docker = None
    imports = set()
    mainfiles = []
    output_files = set()  # organize by source, output_file path
    readmes = []
    urls = set()

    root_dirs = ()
    for root, dirs, files in os.walk(self.repo_path):
      if root == self.repo_path:
        # Mechanism in get_imports to ignore local libraries based on
        # directories in path root folder. Also add "." to the list and
        # converted to a tuple to be used with str.startswith.
        root_dirs = dirs
        root_dirs.append('.')
        root_dirs = tuple(root_dirs)

      for file in files:
        filename, file_ext = os.path.splitext(file)
        full_filename = root + self.sep + file

        if file_ext == '.jl':
          # Collate all imports
          imports.update(self.get_imports(full_filename, root_dirs))

          # output files
          temp_list = util.get_output1(full_filename)
          if temp_list:
            output_files.update(temp_list)

          # urls
          temp_list = util.get_urls(full_filename)
          if temp_list:
            urls.update(temp_list)

          # file_names
          data_files.update(util.get_filenames(full_filename))

          # comments
          if self.return_comments:
            comments.append({file: util.get_comments(full_filename) })

        elif file == 'Dockerfile':
          docker = dict(docker_entrypoint=dminer.report_dockerfile(full_filename))

        elif file.lower().startswith('readme'):
          # load entire readme until a better desription is generated
          with open(full_filename, 'rt', encoding='utf8') as readme_file:
            readmes.append({full_filename: readme_file.read()})

          # add urls, then further processing
          temp_list = util.get_urls(full_filename)
          if temp_list:
            urls.update(temp_list)

          # file_names
          data_files.update(util.get_filenames(full_filename))

    # Report imports and model types.
    model_types = sorted(util.get_model_types_from_libraries(imports, self.sep, 'Julia'))
    imports = sorted(imports)

    # Report output files, a set of tuples.
    # Remove common path from source files in output_files
    cp = util.commonprefix(mainfiles)
    output_files = util.replace_cp_in_tuple_set(output_files, cp)
    # Reorganize output_files items in tuple as dict.
    output_files = util.reorg_output_files(output_files)

    # Remove common path from readme filenames.
    readmes = util.replace_cp_in_dict_list(readmes, cp)

    # Add the collected data to the dictionary.
    self.yaml_dict['docker_entrypoint'] = docker
    self.yaml_dict['model_types'] = model_types
    self.yaml_dict['imports'] = imports
    self.yaml_dict['main_files'] = mainfiles
    self.yaml_dict['data_files'] = sorted(data_files)
    self.yaml_dict['output_files'] = util.group_tuple_pairs(output_files)
    self.yaml_dict['urls'] = util.group_tuple_pairs(urls)
    self.yaml_dict['readmes'] = readmes
    self.yaml_dict['comments'] = comments
