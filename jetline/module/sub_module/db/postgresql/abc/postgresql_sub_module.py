"""PostgreSQL サブモジュールの共通基底."""

import logging

from ......util.file_util import FileUtil
from ....abc.sub_module import SubModule

logger = logging.getLogger("jetline")


class PostgreSQLSubModule(SubModule):
    """PostgreSQL 系サブモジュールの共通処理を提供する基底クラス."""

    def set_up(self):
        """実行前処理として共通コンテキストをログ出力する."""
        super().set_up()
        self._log_execution_context()

    def resolve_postgresql_component(self):
        """パラメータのコンポーネントキーから PostgreSQL コンポーネントを解決する."""
        return self.resolve_component(self._parameter.postgresql_component_key.get())

    def load_sql_from_parameter(self) -> str:
        """パラメータに指定された SQL ファイルを入力値で展開して読み込む."""
        return FileUtil.file_to_str(
            self._parameter.sql_file_name.get(),
            self._parameter.input_value.get(),
        )

    def _log_execution_context(self) -> None:
        """サブモジュール実行時の主要コンテキストをログへ出力する."""
        component_key = self._parameter.postgresql_component_key.get()
        logger.info(
            "Executing %s (component_key=%s)",
            self.__class__.__name__,
            component_key,
        )

        sql_file_value = getattr(self._parameter, "sql_file_name", None)
        if sql_file_value is not None:
            logger.debug("SQL file: %s", sql_file_value.get())
