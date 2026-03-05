
"""PostgreSQL COPY TO コマンド."""

import builtins
import gzip
import logging
import os
from collections.abc import Sequence

from ....container.component.postgresql_component import PostgreSQLComponent
from .abc.postgresql_command import PostgreSQLCommand

logger = logging.getLogger('jetline')


class PostgreSQLCopyToCommand(PostgreSQLCommand):
    """SQL 結果をファイルへエクスポートする."""

    def __init__(
        self,
        component: PostgreSQLComponent,
        sql_str: str,
        csv_file_name: str,
        delimiter: str,
        null_str: str | None,
        header: bool,
        quote: str,
        escape: str,
        force_quote_list: Sequence[str] | None,
        encoding: str,
        gzip_mode: bool,
    ):
        """COPY TO コマンドを初期化する.

        Args:
            component: PostgreSQL コンポーネント。
            sql_str: 出力対象レコードを返す SQL。
            csv_file_name: 出力先ファイル名。
            delimiter: 区切り文字。
            null_str: NULL 表現文字列。
            header: ヘッダー有無。
            quote: クォート文字。
            escape: エスケープ文字。
            force_quote_list: 強制クォート対象カラム一覧。
            encoding: 出力ファイルの文字コード。
            gzip_mode: gzip 形式で出力するかどうか。
        """
        force_quote = None
        if force_quote_list is not None:
            force_quote = ','.join(force_quote_list)
        self._template_context = {
            'sql_str': sql_str.rstrip().rstrip(';'),
            'csv_file_name': csv_file_name,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape,
            'force_quote': force_quote
        }
        self._csv_file_name = csv_file_name
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
        """COPY TO を実行してファイルへ出力する."""
        super().run()
        module, mode = (gzip, 'wt') if self._gzip else (builtins, 'w')
        logger.info('Exporting to %s', self._csv_file_name)
        with module.open(self._csv_file_name, mode=mode, encoding=self._encoding) as file_obj:
            self._cursor.copy_expert(self._sql_str, file_obj)
        self._connection.commit()
