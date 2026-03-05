
"""PostgreSQL COPY FROM コマンド."""

import builtins
import gzip
import logging
import os
from collections.abc import Sequence

from ....container.component.postgresql_component import PostgreSQLComponent
from .abc.postgresql_command import PostgreSQLCommand

logger = logging.getLogger('jetline')


class PostgreSQLCopyFromCommand(PostgreSQLCommand):
    """ファイル群を PostgreSQL テーブルへ取り込む."""

    def __init__(
        self,
        component: PostgreSQLComponent,
        table_name: str,
        column_list: list[str] | None,
        csv_file_name_list: Sequence[str],
        delimiter: str,
        null_str: str | None,
        header: bool,
        quote: str,
        escape: str,
        encoding: str,
        gzip_mode: bool,
    ):
        """COPY FROM コマンドを初期化する.

        Args:
            component: PostgreSQL コンポーネント。
            table_name: 取込先テーブル名。
            column_list: 取込対象カラム一覧。
            csv_file_name_list: 取込対象ファイル一覧。
            delimiter: 区切り文字。
            null_str: NULL 表現文字列。
            header: ヘッダー有無。
            quote: クォート文字。
            escape: エスケープ文字。
            encoding: 入力ファイルの文字コード。
            gzip_mode: gzip 圧縮ファイルを扱うかどうか。
        """
        self._template_context = {
            'table_name': table_name,
            'column_list': column_list,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape,
        }
        self._csv_file_name_list = list(csv_file_name_list)
        self._encoding = encoding
        self._gzip = gzip_mode
        super().__init__(component)

    def set_up(self):
        """テンプレート SQL を生成する."""
        template_name = f'{os.path.splitext(os.path.basename(__file__))[0]}.sql'
        self._sql_str = self.render_sql_template(
            self._template_context,
            template_dir=os.path.join(os.path.dirname(__file__), 'sql'),
            template_name=template_name,
        )

    def run(self):
        """CSV/TSV（または gzip）を COPY FROM で取り込む."""
        super().run()
        module, mode = (gzip, 'rt') if self._gzip else (builtins, 'r')

        for csv_file_name in self._csv_file_name_list:
            logger.info('Loading from %s', csv_file_name)
            with module.open(
                csv_file_name,
                mode=mode,
                encoding=self._encoding,
                errors='ignore',
            ) as file_obj:
                self._cursor.copy_expert(self._sql_str, file_obj)
        self._connection.commit()
