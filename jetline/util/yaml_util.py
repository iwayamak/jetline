# -*- coding: utf-8 -*-

import os
import glob
import yaml
from .file_util import FileUtil


class YamlUtil(object):

    @staticmethod
    def load_file(filename):
        s = FileUtil.file_to_str(filename)
        return yaml.load(s, Loader=yaml.SafeLoader)

    @staticmethod
    def load_dir(dir_path):
        dict_obj = {}
        file_list = glob.glob(os.path.join(dir_path, '*'))
        for file in file_list:
            dict_obj.update(YamlUtil.load_file(file))
        return dict_obj

    @staticmethod
    def write_file(filename, data):
        with open(filename, 'w', encoding='utf8') as fd:
            fd.write(yaml.dump(data))
