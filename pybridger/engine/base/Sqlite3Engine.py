#-------------------------------------------------------------------------------
import sqlite3                              # sqlite3
from .SqlEngine     import SqlEngine        # 規定SQLエンジンクラス
from .datetypes     import Sqlite3DateTypes # Sqlite3のデータ型クラス
from ...common      import override         # オーバライドメソッド
from ...common      import public           # パブリックメソッド
from ...common      import private          # プライベートメソッド
from ...Log         import Log              # ログクラス
#-------------------------------------------------------------------------------
class Sqlite3Engine(SqlEngine, Sqlite3DateTypes):
    """
    Sqlite3エンジンクラス
    Attributes:
        database  (str)                       : データベースパス名
        sqlEngine (sqlite3)                   : sqlite3クラス
        conn      (sqlite3.Connection | None) : sqlite3コネクトオブジェクト
        cur       (sqlite3.Cursor     | None) : sqlite3カーソルオブジェクト
        __isLog   (bool)                      : ログフラグ 
        __Log     (Log)                       : ログオブジェクト
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            databasePath : str,
            logFile      : str | None = None
        ):
        """
        SQLite3データベース接続エンジンの初期化
        Args:
            databasePath (str)        : データベースパス
            logFile      (str | None) : ログファイル名
        """
        super().__init__()
        # インスタンス変数
        self.database : str = databasePath
        # インスタンス変数(オブジェクト)
        self.sqlEngine = sqlite3
        self.conn : sqlite3.Connection | None = None # ← 明示的に定義
        self.cur  : sqlite3.Cursor     | None = None # ← 明示的に定義
        # ログの初期設定
        self.__setLog(logFile)
    #---------------------------------------------------------------------------
    @private
    def __setLog(self, logFile : str | None):
        """ログクラスとフラグの設定"""
        # ログファイルが未指定なら
        if logFile is None:
            self.__isLog = False
            self.__log   = None
        # ログファイルが指定されていれば
        elif logFile:
            self.__isLog = True
            self.__log   = Log(logFile)
        else:
            self.__isLog = False
            self.__log   = None
    #---------------------------------------------------------------------------
    @private
    def __logDebug(self, msg):
        """デバックメッセージ"""
        if self.__isLog and self.__log is not None:
            self.__log.debug(msg)
    #---------------------------------------------------------------------------
    @private
    def __logInfo(self, msg):
        """インフォメッセージ"""
        if self.__isLog and self.__log is not None:
            self.__log.info(msg)
    #---------------------------------------------------------------------------
    @private
    def __logWarning(self, msg):
        """警告メッセージ"""
        if self.__isLog and self.__log is not None:
            self.__log.warning(msg)
    #---------------------------------------------------------------------------
    @private
    def __logError(self, msg):
        """エラーメッセージ"""
        if self.__isLog and self.__log is not None:
            self.__log.error(msg)
    #---------------------------------------------------------------------------
    @private
    def __logCritical(self, msg):
        """致命的エラーメッセージ"""
        if self.__isLog and self.__log is not None:
            self.__log.critical(msg)   
    #---------------------------------------------------------------------------
    @override
    @public
    def connect(self) -> sqlite3.Connection:
        """
        データベースの接続
        Returns:
            sqlite3.Connection : コネクトオブジェクト
        Raises:
            Exception : データベースの接続に失敗した場合
        """
        try:
            self.conn = self.sqlEngine.connect(self.database)
            return self.conn
        except Exception as e:
            msg = "データベースの接続に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def cursor(self) -> sqlite3.Cursor:
        """
        カーソルの作成
        Returns:
            sqlite3.Cursor : カーソルオブジェクト
        Raises:
            Exception : カーソルの作成に失敗した場合
        """
        try:
            # 接続してなければ
            if self.conn is None:
                self.connect()
            # 絶対Noneがないと明示する
            # 接続があればカーソル取得
            assert self.conn is not None # 安全チェック
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as e:
            msg = "カーソルの作成に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------    
    @override
    @public
    def execute(self, query : str, value : tuple = ()) -> None:
        """
        クエリを実行
        Args:
            query (str)     : 実行するクエリ文
            value (tuple)   : プレイスホルダーに渡す値
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{value}")
            self.cursor().execute(query, value)
        except Exception as e:
            msg  = "クエリの実行に失敗しました"
            qmsg = f"クエリ:{query}, 値:{value}"
            self.__logError(msg)
            self.__logError(qmsg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def executeAny(self, query: str, data: list[tuple[str]]):
        """
        クエリの実行(複数)
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{data}")
            self.cursor().executemany(query, data)
        except Exception as e:
            msg  = "クエリの実行に失敗しました"
            qmsg = f"クエリ:{query}, 値:{data}"
            self.__logError(msg)
            self.__logError(qmsg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def commit(self):
        """
        データベースにコミットする
        Raises:
            Exception : コミットに失敗した場合
        """
        try:
            if self.conn:
                self.conn.commit()
        except Exception as e:
            # コミットが失敗した場合ロールバックする
            msg = "コミットが失敗したためロールバックしました"
            self.__logError(msg)
            self.rollback()
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def connectOpen(self):
        """
        コネクトとカーソルの開放
        Raises:
            Exception : コネクトとカーソルの開放に失敗した場合
        """
        try:
            self.connect()
            self.cursor()
        except Exception as e:
            msg = "コネクトとカーソルの開放に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")  
    #---------------------------------------------------------------------------
    @override
    @public
    def connectClose(self) -> None:
        """
        コネクションとカーソルのクローズ
        Raises:
            Exception : コネクトとカーソルのクローズに失敗した場合
        """
        try:
            # コネクトが接続していれば
            if self.conn:
                self.conn.close()
                self.conn = None
                self.cur  = None
        except Exception as e:
            msg = "コネクトとカーソルのクローズに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    def transaction(self) -> None:
        """
        トランザクション
        Raises:
            Exception : トランザクションに失敗した場合
        """
        try:
            if self.conn:
                self.cursor().execute("BEGIN")
        except Exception as e:
            msg = "トランザクションに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    def rollback(self) -> None:
        """
        ロールバック
        Raises:
            Exception : ロールバックに失敗した場合
        """
        try:
            if self.conn:
                self.conn.rollback()
        except Exception as e:
            msg = "ロールバックに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    def isConnected(self) -> bool:
        """
        Sqlite3に接続中かどうか返す
        Returns:
            bool : 接続されていればTrue
        """
        return self.conn is not None
#-------------------------------------------------------------------------------