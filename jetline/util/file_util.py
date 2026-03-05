"""ファイル入出力と簡易テキスト変換ユーティリティ。."""

from ..substr.place_holder import PlaceHolder


class FileUtil:
    """ファイル文字列処理を提供する。."""

    @classmethod
    def file_to_str(cls, filename: str, input_value: dict | None = None) -> str:
        """テンプレート展開済みファイル文字列を返す。.

        Args:
            filename: 読み込み対象ファイルパス。
            input_value: テンプレート置換用パラメータ。

        Returns:
            str: 展開後の文字列。
        """
        params = {} if input_value is None else input_value
        place_holder = PlaceHolder(filename, params)
        return place_holder.apply()

    @classmethod
    def str_to_file(cls, filename: str, text: str) -> int:
        """文字列をファイルへ上書き保存する。."""
        with open(filename, mode="w", encoding="utf8") as file:
            return file.write(text)

    @classmethod
    def str_to_file_append(cls, filename: str, text: str) -> int:
        """文字列をファイルへ追記保存する。."""
        with open(filename, mode="a", encoding="utf8") as file:
            return file.write(text)

    @classmethod
    def tsv_str_to_html_table(cls, tsv_contents: str, column_str: str) -> str:
        """TSV 文字列を HTML テーブルへ変換する。."""
        tsv_lines = (column_str + tsv_contents).split("\n")
        html_table = "<table>"
        for tsv_line in tsv_lines:
            html_table += "<tr>"
            for tab in tsv_line.split("\t"):
                html_table += f"<td>{tab}</td>"
            html_table += "</tr>"
        html_table += "</table>"
        return html_table
