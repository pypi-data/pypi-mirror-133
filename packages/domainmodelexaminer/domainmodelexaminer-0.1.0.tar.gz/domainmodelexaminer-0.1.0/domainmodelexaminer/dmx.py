
from os.path import abspath, basename, dirname, splitext
import sys

# Add path of the run files to the system path so VS Code can find things. 
sys.path.append(dirname(dirname(abspath(__file__))))

import argparse
import json
import logging
import os
from pathlib import Path
from pkg_resources import resource_stream

from domainmodelexaminer import arbitrary_miner as arbminer
from domainmodelexaminer import julia_miner as julieminer
from domainmodelexaminer import language as language
from domainmodelexaminer import python_miner as pyminer
from domainmodelexaminer import r_miner as rminer
from domainmodelexaminer import repo_miner as repo_miner
from domainmodelexaminer import utilities as util


def examine(url: str, return_json: bool = True, return_comments: bool = True):
  """
  Description
  -----------
    For external calls e.g. dojo api.

  Parameters
  ----------
    url: str
      GitHub or GitLab repo url.
    return_json: bool = True
      Returns a JSON string if true, else a YAML string.

  Returns
  -------
    Model info as JSON or YAML string.

  """
  
  # Process the repository into a dictionary for yaml output.
  yaml_dict = process_repo(url, return_comments = return_comments)

  if return_json:
    return yaml_dict
  else:
    # Covert the dictionary to yaml output.
    yaml_str = util.yaml_dump(yaml_dict)
    return yaml_str

def main():
  parser = argparse.ArgumentParser(
  description='Domain Model Examiner (DMX) mines codebases to semi- \
    automate installation and execution', epilog='Good luck.'
    )
  parser.add_argument('--repo', help="GitHub repo path in double quotes")
  parser.add_argument('--url',  help="GitHub repo URL in double quotes")
  args = parser.parse_args()

  if args.url is not None:
    process_repo(url = args.url, repo = None, write_output=True)
  elif args.repo is not None:
    process_repo(url = None, repo = args.repo, write_output=True)
  else:
    # resort to reading from parameters.json
    if os.name == str("nt"):
      filepath = 'data_files\\parameters.json'
    else:
      filepath = 'data_files/parameters.json'
    
    try:
      try:
        # The necessary code to load from pkg doesn't currently work in VS Code Debug, so wrap in try/except.
        with resource_stream(__name__, filepath) as f:
          params = f.read()
      except Exception:
        with open(Path(__file__).parent / filepath, 'r') as f:
          params = f.read()

      params = json.loads(params)
      for repo in params['repositories']:
        process_repo(url = None, repo = repo['path'], write_output=True)
    except FileNotFoundError:
      logging.error(f"{filepath} not found")
    except Exception as e:
      logging.error(e)

def process_repo(url: str, repo: str = None, write_output: bool = False, return_comments: bool = True):
  """
  Description
  -----------
    Examines the repo at the url or locally (repo).

  Parameters
  ----------
    url: str
      Github repo url.

    repo: str
      If no url, the local repository path.

    write_output: bool = False
      Whether to write to the .yaml file. Defaults to False.

  Returns
  -------
    The list of dict.
  """

  try:
    if url is not None:
      repo_miner.clone_repo(url)
      repo_name = splitext(basename(url))[0]
      repo = 'tmp'
    elif repo is not None:
      repo_name = basename(repo)
    else:
      # TODO blow some error
      return

    # Call Repominer to get owner info and About descriptions. Pass these to
    # to language-specific Miner class so they are at the top of the yaml/json.
    owner_info = repo_miner.extract_owner(url, repo)
    about_desc = repo_miner.extract_about(url, repo, repo_name)

    # Call language-specific mining which returns a dictionary for yaml output.
    lang = language.detect_language(repo)
    if (lang == '.py'):
      yaml_dict = pyminer.PyRepoMiner(repo, repo_name, about_desc, owner_info, return_comments).yaml_dict
    elif (lang == '.R'):
      yaml_dict = rminer.RRepoMiner(repo, repo_name, about_desc, owner_info, return_comments).yaml_dict
    elif (lang == '.jl'):
      yaml_dict = julieminer.JuliaRepoMiner(repo, repo_name, about_desc, owner_info, return_comments).yaml_dict
    else:
      yaml_dict = arbminer.ArbitraryRepoMiner(repo, repo_name, lang, about_desc, owner_info, return_comments).yaml_dict

    # Write yaml file using utility to control newlines in comments.
    if write_output:
      util.yaml_write_file(repo_name, yaml_dict)

    # Remove downloaded repo if url was passed.
    if url is not None:
      repo_miner.delete_repo()

    # Return the dictionary for yaml output.
    return yaml_dict

  except Exception as e:
    logging.error(e)

if __name__ == "__main__":
  main()