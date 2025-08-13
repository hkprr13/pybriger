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
# 非同期psycopgのインストールが出来ているかどうか確認
try:
    from psycopg import AsyncConnection, AsyncCursor
except Exception as e:
    raise Exception(
        "非同期psycopgがインストールされていません\n"
        "下記をターミナルで実行してください\n"
        "pip install psycopg[async]"
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
class AsyncPostgreSqlEngine(SqlEngine, PostgreSqlDateTypes):
    """
    非同期PostgreSQLエンジンクラス
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
        self.conn : AsyncConnection | None = None
        self.cur  : AsyncCursor     | None = None
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
    async def connect(self) -> AsyncConnection:
        """
        非同期でデータベースの接続
        Returns:
            AsyncConnection : コネクトオブジェクトを返す
        Raises:
            Exception : データベースの接続に失敗した場合
        """
        try:
            self.conn = await self.sqlEngine.AsyncConnection.connect(
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
    async def cursor(self) -> AsyncCursor:
        """
        非同期でカーソルの作成
        Returns:
            AsyncCursor : カーソルオブジェクトを返す
        Raises:
            Exception : カーソルの失敗した場合
        """
        try:
            assert self.conn is not None # 明示する
            if self.cur:
                try:
                   await self.cur.close()
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
    async def execute(self, query: Any, value: tuple = ()) -> None:
        """
        クエリの実行
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{value}")
            cur = await self.cursor()
            await cur.execute(query, value)
        except Exception as e:
            msg  = "クエリの実行に失敗しました"
            qmsg = f"クエリ:{query}, 値:{value}"
            self.__logError(msg)
            self.__logError(qmsg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def executeAny(self, query: Any, data: list[tuple[str]]) -> None:
        """
        クエリの実行(複数)
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{data}")
            cur = await self.cursor()
            await cur.executemany(query, data)
        except Exception as e:
            msg  = "クエリの実行に失敗しました"
            qmsg = f"クエリ:{query}, 値:{data}"
            self.__logError(msg)
            self.__logError(qmsg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def commit(self) -> None:
        """
        データベースにコミットする
        Raises:
            Exception : コミットに失敗した場合
        """
        try:
            if self.conn:
                await self.conn.commit()
        except Exception as e:
            # コミットが失敗した場合ロールバックする
            msg = "コミットが失敗したためロールバックしました"
            self.__logError(msg)
            await self.rollback()
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def connectOpen(self) -> None:
        """
        コネクトとカーソルの開放(非同期)
        Raises:
            Exception : コネクトとカーソルの開放に失敗した場合
        """
        try:
            await self.connect()
            await self.cursor()
        except Exception as e:
            msg = "コネクトとカーソルの開放に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")  
    #---------------------------------------------------------------------------
    @override
    @public
    async def connectClose(self) -> None:
        """
        コネクションとカーソルのクローズ(非同期)
        Raises:
            Exception : コネクトとカーソルのクローズに失敗した場合
        """
        try:
            # カーソルがあれば
            if self.cur:
                await self.cur.close()
            # コネクトが接続していれば
            if self.conn:
                await self.conn.close()
            self.conn = None # 初期値に戻す
            self.cur  = None # 初期値に戻す
        except Exception as e:
            msg = "コネクトとカーソルのクローズに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    async def transaction(self) -> None:
        """
        非同期トランザクションの開始
        Raises:
            Exception : トランザクションに失敗した場合
        """
        try:
            if self.conn:
                cur = await self.cursor()
                await cur.execute("BEGIN")
        except Exception as e:
            msg = "トランザクションに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    async def rollback(self) -> None:
        """
        非同期ロールバック
        Raises:
            Exception : ロールバックに失敗した場合
        """
        try:
            if self.conn:
                await self.conn.rollback()
        except Exception as e:
            msg = "ロールバックに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def isConnected(self) -> bool:
        """
        PostgreSQLに接続中かどうか返す
        Returns:
            bool : 接続されていればTrue
        """
        return self.conn is not None
#-------------------------------------------------------------------------------