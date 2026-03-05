"""パス解決ユーティリティ。."""

import os


class PathUtil:
    """jetline で利用する各種パスを解決する。."""

    SETTINGS_DIR = 'settings'
    COMPONENT_DIR = 'component'
    LOGGING_CONF = 'logging_config.yaml'
    LOGS_DIR = 'logs'

    @classmethod
    def jetline_root_path(cls):
        """リポジトリルートの絶対パスを返す。.

        Returns:
            str: ルートディレクトリの絶対パス。
        """
        return os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]

    @classmethod
    def settings_root_path(cls):
        """設定ディレクトリを返す。.

        Returns:
            str: 設定ディレクトリの絶対パス。
        """
        key = os.getenv('JETLINE_SETTINGS')
        if key and os.path.exists(key):
            path = key
        else:
            jetline_package_root = os.path.split(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )[0]
            path = os.path.join(jetline_package_root, cls.SETTINGS_DIR)
        return path

    @classmethod
    def component_path(cls):
        """コンポーネント設定ディレクトリを返す。.

        Returns:
            str: コンポーネント設定ディレクトリ。
        """
        return os.path.join(cls.settings_root_path(), cls.COMPONENT_DIR)

    @classmethod
    def logging_conf_path(cls):
        """ロギング設定ファイルパスを返す。.

        Returns:
            str: ロギング設定ファイルのパス。
        """
        return os.path.join(cls.settings_root_path(), cls.LOGGING_CONF)

    @classmethod
    def mkdir_if_not_exists(cls, path):
        """ディレクトリが存在しない場合に作成する。.

        Args:
            path: ファイルパスまたはディレクトリパス。
        """
        dir_path = os.path.dirname(path) if os.path.isfile(path) else path
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @classmethod
    def logs_path(cls):
        """ログディレクトリを返す。.

        Returns:
            str: ログディレクトリの絶対パス。
        """
        return os.path.join(cls.jetline_root_path(), cls.LOGS_DIR)
