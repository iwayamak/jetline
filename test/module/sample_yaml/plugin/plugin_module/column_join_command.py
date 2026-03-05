"""CSV 列結合を行うサンプルカスタムコマンド."""

import csv
import logging

from jetline.command.abc.custom_command import CustomCommand

logger = logging.getLogger("jetline")


class ColumnJoinCommand(CustomCommand):
    """複数CSVを行単位で結合して1ファイルへ出力するコマンド."""

    def set_up(self) -> None:
        """実行前処理を行う."""
        super().set_up()

    def body(self) -> None:
        """メイン処理のフックを呼び出す."""
        super().body()

    def run(self) -> None:
        """対象CSVを読み込み、同一行の列を連結して書き出す."""
        target_file_list = self._kwargs["target_files"]
        result_file = self._kwargs["result_file"]
        data_array: list[list[str]] = []
        super().run()

        for target_file in target_file_list:
            logger.info('loading "%s"', target_file)
            with open(target_file, newline="", encoding="utf-8") as file_obj:
                read_data = [row for row in csv.reader(file_obj)]
                if not data_array:
                    data_array = read_data
                    continue

                for index, row in enumerate(read_data):
                    data_array[index].extend(row)

        with open(result_file, mode="w", newline="", encoding="utf-8") as file_obj:
            logger.info("Exporting to %s", result_file)
            csv.writer(file_obj).writerows(data_array)
        logger.info("Processing is complete.")

    def dry_run(self) -> None:
        """Dry-run 時のフックを呼び出す."""
        super().dry_run()

    def tear_down(self) -> None:
        """後処理のフックを呼び出す."""
        super().tear_down()
