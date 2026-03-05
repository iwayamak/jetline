"""PostgreSQLProcessingCommand のユニットテスト."""

from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter

from ....abc.base_test_case import BaseTestCase


class TestPostgreSQLProcessingCommand(BaseTestCase):
    """PostgreSQLProcessingCommand の基本実行を検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._component = Container().component("POSTGRESQL_COMPONENT.ID=UT")
        self._sql_str = "select current_timestamp"
        super().__init__(*args, **kwargs)

    def test_select_dry_run(self) -> None:
        """Dry-run 時に SQL が実行可能なことを確認する."""
        ShareParameter.dry_run_mode = True
        PostgreSQLProcessingCommand(self._component, self._sql_str).execute()

    def test_select_run(self) -> None:
        """通常実行時に SQL が実行可能なことを確認する."""
        ShareParameter.dry_run_mode = False
        PostgreSQLProcessingCommand(self._component, self._sql_str).execute()
