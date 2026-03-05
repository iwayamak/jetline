"""Jinja2 ベースのテンプレート置換処理。."""

import os

from jinja2 import Environment, FileSystemLoader

from ..share_parameter.share_parameter import ShareParameter
from ..util.path_util import PathUtil
from .template_string.template_string import TemplateString


class PlaceHolder:
    """ファイルテンプレートへ実行時変数を注入する。."""

    def __init__(self, filename: str, input_value: dict):
        """テンプレート置換対象を初期化する。.

        Args:
            filename: テンプレートファイルパス。
            input_value: 置換対象の入力変数辞書。
        """
        self._filename = filename
        self._input_value = input_value

    def apply(self) -> str:
        """テンプレートを評価して文字列を返す。."""
        return self._evaluate()

    def _build_context(self) -> dict:
        """テンプレート評価に使うコンテキストを構築する。."""
        context = dict(self._input_value)
        context.update(
            {
                "batch_name": ShareParameter.batch_name,
                "exec_date": TemplateString.exec_date,
                "log_dir": ShareParameter.log_dir,
                "timestamp": TemplateString.timestamp,
                "jetline_root": PathUtil.jetline_root_path(),
            }
        )
        return context

    def _evaluate(self) -> str:
        """テンプレートを評価する。."""
        template_dir = os.path.abspath(os.path.dirname(self._filename))
        env = Environment(loader=FileSystemLoader(template_dir, encoding="utf-8"))
        template = env.get_template(os.path.basename(self._filename))
        return template.render(self._build_context())
