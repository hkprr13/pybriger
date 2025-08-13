#-------------------------------------------------------------------------------
# psycopgのインストールが出来ているかどうか確認
try:
    import psycopg
except Exception as e:
    raise Exception(
        "psycopgがインストールされていません\n"
        "下記をターミナルで実行してください\n"
        "pip install psycopg[binary]"
    )
#-------------------------------------------------------------------------------
from typing         import Any                  # Any型クラス
from .SqlEngine     import SqlEngine            # 基底SQLエンジンクラス
from .datetypes     import PostgreSqlDateTypes  # PostgreSQLのデータ型クラス
from ...common      import override             # オーバライドメソッド
from ...common      import public               # パブリックメソッド
from ...common      import private              # プライベートメソッド
from ...Log          import Log                  # ログクラス
#-------------------------------------------------------------------------------
class PostgreSqlEngine(SqlEngine, PostgreSqlDateTypes):
    """
    PostgreSQLエンジンクラス
    Attributes:
        hostName     (str)        : ホスト名
        userName     (str)        : ユーザー名
        password     (str)        : パスワード
        databaseName (str)        : データベース名
        port         (int)        : ポート番号
        sqlEngine    (psycopg)    : psycopgクラス
        conn         (Any | None) : psycopgコネクトオブジェクト
        cur          (Any | None) : psycopgカーソルオブジェクト
        __isLog      (bool)       : ログフラグ 
        __Log        (Log)        : ログオブジェクト
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            hostName     : str,
            userName     : str,
            password     : str,
            databaseName : str,
            port         : int,
            logFile      : str | None = None
        ):
        """
        PostgreSQLエンジンの初期化
        Args:
            hostName     (str)        : ホスト名
            userName     (str)        : ユーザー名
            password     (str)        : パスワード
            databaseName (str)        : データベース名
            port         (str)        : ポート番号
            logFile      (str | None) : ログファイル名
        """
        super().__init__()
        # インスタンス変数
        self.hostName     = hostName
        self.userName     = userName
        self.password     = password
        self.databaseName = databaseName
        self.port         = port
        # インスタンス変数,(オブジェクト)
        self.sqlEngine  = psycopg
        self.conn = None
        self.cur  = None
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
    def connect(self) -> Any:
        """
        データベースの接続
        Returns:
            Any : コネクトオブジェクトを返す
        Raises:

        """
        try:
            self.conn = self.sqlEngine.connect(
                host     = self.hostName,
                user     = self.userName,
                password = self.password,
                database = self.databaseName,
                port     = self.port
            )
            return self.conn
        except Exception as e:
            msg = "データベースの接続に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def cursor(self) -> Any:
        """
        カーソルの作成
        Returns:
            Any : カーソルオブジェクトを返す
        Raises:
            Exception : カーソルの失敗した場合
        """
        try:
            assert self.conn is not None # 明示する
            if self.cur:
                try:
                    self.cur.close()
                except Exception:
                    pass # カーソルが閉じ済みの時用
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as e:
            msg = "カーソルの作成に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def execute(self, query: Any, value: tuple = ()) -> None:
        """
        クエリの実行
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
    def executeAny(self, query: Any, data: list[tuple[str]]) -> None:
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
    def commit(self) -> None:
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
    def connectOpen(self) -> None:
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
                if self.cur is not None:
                    self.cur.close()
                self.conn.close()
                self.conn = None # 初期値に戻す
                self.cur  = None # 初期値に戻す
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
        MySQLに接続中かどうか返す
        Returns:
            bool : 接続されていればTrue
        """
        return self.conn is not None
#-------------------------------------------------------------------------------