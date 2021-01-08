# !usr/bin/env python

import os
import zipfile
import yaml
import re
import csv
import argparse
import json
from pathlib import Path

error_list = []
project_list = []

"""
读取實例
multimc_dir: multimc目录
"""

parser = argparse.ArgumentParser()
parser.add_argument('-c','--config', nargs='?', const=1, type=str,default='config.yml',help='config file name')
args = parser.parse_args()
print(args)

config_path = Path(args.config).expanduser()
with open(config_path, 'r') as f:
    config = yaml.load(f)
    multimc_dir = config['multimc_dir']
    
multimc_instances_dir = Path(multimc_dir).expanduser().joinpath('instances')
if os.path.exists(multimc_instances_dir):
    files = os.listdir(multimc_instances_dir)
    files.remove('instgroups.json')
    for i in range(3,len(files)):
        print(i,files[i])
    no = input()
    print(files[int(no)])
    instances_name = files[int(no)]
    with open(multimc_instances_dir.joinpath(instances_name,'mmc-pack.json'),'r') as f:
        data = json.load(f)
        minecraft_version = data["components"][1]['version']
    config['version'] = minecraft_version
    config['origin_mod_dir'] = multimc_instances_dir.joinpath(instances_name,'.minecraft','mods').as_uri().replace('file://','')
    with open(instances_name+'.yaml', "w") as f:
        yaml.dump(config, f)
