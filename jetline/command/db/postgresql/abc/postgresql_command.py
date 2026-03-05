"""PostgreSQL コマンドの共通実装."""

from typing import cast

import psycopg2
from jinja2 import Environment, FileSystemLoader

from .....container.component.postgresql_component import PostgreSQLComponent
from ...abc.db_command import DbCommand


class PostgreSQLCommand(DbCommand):
    """PostgreSQL 接続を伴うコマンドの基底クラス."""

    def __init__(self, component: PostgreSQLComponent, sql_str: str | None = None):
        """PostgreSQL コマンドを初期化する.

        Args:
            component: PostgreSQL 接続情報を持つコンポーネント.
            sql_str: 実行対象 SQL。テンプレート展開時は `set_up` で設定する.
        """
        self._sql_str = sql_str
        super().__init__(component)

    @property
    def postgresql_component(self) -> PostgreSQLComponent:
        """PostgreSQL コンポーネントを型付きで返す。"""
        return cast(PostgreSQLComponent, self.component)

    def run(self):
        """PostgreSQL へ接続し、実行準備を行う."""
        self._connection = psycopg2.connect(
            database=self.postgresql_component.database,
            user=self.postgresql_component.user,
            password=self.postgresql_component.password,
            host=self.postgresql_component.host,
            port=self.postgresql_component.port,
        )
        self._connection.set_client_encoding("utf-8")
        super().run()

    def _query_builder(self):
        """実行 SQL を返す."""
        return self._sql_str

    def _mask_password(self):
        """ログ出力用 SQL を返す."""
        return self._sql_str

    @staticmethod
    def render_sql_template(
        context: dict[str, object],
        template_dir: str,
        template_name: str,
    ) -> str:
        """SQL テンプレートを描画する.

        Args:
            context: テンプレートへ渡すレンダリング用データ.
            template_dir: テンプレートディレクトリ.
            template_name: テンプレートファイル名.

        Returns:
            str: 描画済み SQL 文字列.
        """
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template.render(context)

    def execute_query(self, *, commit: bool = True) -> None:
        """構築済み SQL を実行する.

        Args:
            commit: 実行後にコミットするかどうか.
        """
        self._cursor.execute(self._query)
        if commit:
            self._connection.commit()
