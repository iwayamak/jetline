"""Jinja2 から利用する日時テンプレート関数群。."""

from datetime import datetime

from dateutil.relativedelta import relativedelta

from ...share_parameter.share_parameter import ShareParameter


class TemplateString:
    """テンプレート用の日時関数を提供する。."""

    @classmethod
    def exec_date(
        cls,
        format_str: str = "%Y%m%d",
        years: float | None = None,
        months: float | None = None,
        days: float | None = None,
    ) -> str:
        """実行日基準でオフセット適用後の日時文字列を返す。."""
        exec_date = datetime.strptime(ShareParameter.exec_date, "%Y%m%d")
        if years is not None:
            exec_date += relativedelta(years=years)
        if months is not None:
            exec_date += relativedelta(months=months)
        if days is not None:
            exec_date += relativedelta(days=days)
        return exec_date.strftime(format_str)

    @classmethod
    def timestamp(
        cls,
        format_str: str = "%Y%m%d",
        years: float | None = None,
        months: float | None = None,
        days: float | None = None,
    ) -> str:
        """現在時刻基準でオフセット適用後の日時文字列を返す。."""
        timestamp = datetime.now()
        if years is not None:
            timestamp += relativedelta(years=years)
        if months is not None:
            timestamp += relativedelta(months=months)
        if days is not None:
            timestamp += relativedelta(days=days)
        return timestamp.strftime(format_str)
