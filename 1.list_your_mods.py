# !usr/bin/env python

import os
import zipfile
import yaml
import re
import csv
import argparse
from pathlib import Path

error_list = []
project_list = []

"""
读取配置
origin_mod_dir: 游戏mod目录
mod_list: 数据文件
"""

parser = argparse.ArgumentParser()
parser.add_argument('-c','--config', nargs='?', const=1, type=str,default='config.yml',help='config file name')
args = parser.parse_args()
print(args)

config_path = Path(args.config).expanduser()
with open(config_path, 'r') as f:
    config = yaml.load(f)
    origin_mod_dir = config['origin_mod_dir']
    mod_list =  config['mod_list']

print(origin_mod_dir)
origin_mod_dir = Path(origin_mod_dir).expanduser()
if os.path.exists(origin_mod_dir):
    files = os.listdir(origin_mod_dir)
    for f in files:
        if f.endswith('.jar'):
            zf = zipfile.ZipFile(origin_mod_dir + '/' + f)
            if 'mcmod.info' in zf.namelist():
                mcmod_info_text = zf.open('mcmod.info').read()
                zf.close()

                _ = mcmod_info_text.replace(b'\n', b'').decode(encoding='utf-8')

                id_obj = re.search(r'"modid"\s*:\s*"(.*?)"', _)
                modid = id_obj.group(1) if id_obj else ''

                name_obj = re.search(r'"name"\s*:\s*"(.*?)"', _)
                name = name_obj.group(1) if name_obj else ''

                author_obj = re.search(r'author.*?:\s*\[(.*?)\]', _)
                author = re.sub(r'[\t\r\f ]{2,}', '', author_obj.group(1).replace(',', '、')) if author_obj else ''

                project_list.append((modid, name, f, author))
            else:
                error_list.append(f)
    if os.path.exists(mod_list):
        os.remove(mod_list)
    with open(mod_list, 'w+') as ml:
        for i,n,f,a in project_list:
            ml.write('{0},{1},{2},{3}\n'.format(i, n, f, a))

print('----------------错误列表----------------------------------------')
for _ in error_list:
    print(_)
print('----------------------------------------------------------------')
