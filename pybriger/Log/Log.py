#-------------------------------------------------------------------------------
import logging  # ログ
#-------------------------------------------------------------------------------
class Log:
    """
    ログクラス
    ログをログファイルに出力する
    """
    def __init__(
            self,
            fileName : str,
        ) -> None:
        """
        ログクラスの初期化
        Args:
            fileName (str) : ファイル名(拡張子も)
        """
        self.__logging = logging
        self.__logging.basicConfig(
            filename = fileName,
            level    = self.__logging.INFO,
            format   = "%(asctime)s - %(levelname)s - %(message)s",
            encoding = "utf-8"
        )
    #---------------------------------------------------------------------------
    def debug(self, msg : str):
        """デバックメッセージ"""
        self.__logging.debug(msg)
    #---------------------------------------------------------------------------
    def info(self, msg : str):
        """インフォメッセージ"""
        self.__logging.info(msg)
    #---------------------------------------------------------------------------
    def warning(self, msg : str):
        """警告メッセージ"""
        self.__logging.warning(msg)
    #---------------------------------------------------------------------------
    def error(self, msg : str):
        """エラーメッセージ"""
        self.__logging.error(msg)
    #---------------------------------------------------------------------------
    def critical(self, msg : str):
        """致命的エラー"""
        self.__logging.critical(msg)
#-------------------------------------------------------------------------------