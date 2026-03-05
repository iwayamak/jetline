"""YAML 入出力ユーティリティ。."""

import glob
import os

import yaml

from .file_util import FileUtil


class YamlUtil:
    """YAML の読み書きを提供する。."""

    @staticmethod
    def load_file(filename: str) -> dict:
        """YAML ファイルを辞書として読み込む。."""
        source = FileUtil.file_to_str(filename)
        return yaml.load(source, Loader=yaml.SafeLoader)

    @staticmethod
    def load_dir(dir_path: str) -> dict:
        """ディレクトリ配下の YAML を順に読み込んでマージする。."""
        dict_obj = {}
        file_list = sorted(glob.glob(os.path.join(dir_path, "*")))
        for file in file_list:
            dict_obj.update(YamlUtil.load_file(file))
        return dict_obj

    @staticmethod
    def write_file(filename: str, data: dict) -> None:
        """辞書を YAML ファイルへ書き込む。."""
        with open(filename, "w", encoding="utf8") as fd:
            fd.write(yaml.dump(data))
