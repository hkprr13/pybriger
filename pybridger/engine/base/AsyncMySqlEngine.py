#-------------------------------------------------------------------------------
from typing         import Any              # Any型クラス
from .SqlEngine     import SqlEngine        # 基底SQLエンジンクラス
from .datetypes     import MySqlDateTypes   # MySQLのデータ型クラス
from ...common      import override         # オーバライドメソッド
from ...common      import public           # パブリックメソッド
from ...common      import private          # プライベートメソッド
from ...Log         import Log              # ログクラス
#-------------------------------------------------------------------------------
class AsyncMySqlEngine(SqlEngine, MySqlDateTypes):
    """
    非同期MySQLエンジンクラス
    Attributes:
        hostName     (str)        : ホスト名
        userName     (str)        : ユーザー名
        password     (str)        : パスワード
        databaseName (str)        : データベース名
        sqlEngine    (aiomysql)   : aiomysqlクラス
        conn         (Any | None) : aiomysqlコネクトオブジェクト
        cur          (Any | None) : aiomysqlカーソルオブジェクト
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
        logFile      : str | None = None
    ):
        """
        非同期MySQLエンジンの初期化
        Args:
            hostName     (str)        : ホスト名
            userName     (str)        : ユーザー名
            password     (str)        : パスワード
            databaseName (str)        : データベース名
            logFile      (str | None) : ログファイル名
        """
        super().__init__()
        # インスタンス変数
        self.hostName     = hostName
        self.userName     = userName
        self.password     = password
        self.databaseName = databaseName
        # インスタンスされたタイミングでインポートを行う
        # インスタンス変数(オブジェクト)
        try:
            import aiomysql
            self.sqlEngine  = aiomysql
         # ドライバがインストールされていない場合エラーメッセージを表示させる
        except Exception as e:
            raise Exception(
                "mysql.connnectorがインストールされていません\n"
                "下記をターミナルで実行してください\n"
                "pip install aiomysql"
            )
        # コネクトオブジェクトとカーソルオブジェクトの初期化
        self.conn = None # 初期値はNone
        self.cur  = None # 初期値はNone
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
    async def connect(self) -> Any:
        """
        非同期でMySQLに接続し、プールを作成
        Returns:
            Any : コネクトオブジェクトを返す
        Raises:
            Exception : データベースの接続に失敗した場合
        """
        try:
            self.pool = await self.sqlEngine.create_pool(
                host       = self.hostName,
                user       = self.userName,
                password   = self.password,
                db         = self.databaseName,
                autocommit = False
            )
            self.conn = await self.pool.acquire()
            return self.conn
        except Exception as e:
            msg = "データベースの接続に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def cursor(self):
        """
        非同期カーソルの作成
        Args:
            dictionary (bool) : 辞書型の指定
        Returns:
            Any : カーソルオブジェクトを返す
        Raises:
            Exception : カーソルの失敗した場合
        """
        try:
            # 接続してなければ
            if self.conn is None:
                await self.connect()
            # 絶対Noneがないと明示する
            # 接続があればカーソル取得
            if not self.conn:# 安全チェック
                raise Exception
            # 戻り値は接続オブジェクトのコルーチンの完了を待って設定
            self.cur  = await self.conn.cursor()
            return self.cur
        except Exception as e:
            msg = "カーソルの作成に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def execute(self, query: str, value: tuple = ()): 
        """
        非同期にSQLクエリを実行する
        Args:
            query (str)     : SQL文
            value (tuple)   : プレイスホルダーに渡す値
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
    async def executeAny(self, query : str, data : list[tuple[str]]) -> None:
        """
        非同期にSQLクエリ(複数)を実行する
        Args:
            query (str)              : クエリ文
            value (list[tuple[str]]) : プレイスホルダーに渡す値
        Args:
            query (str)             : SQL文
            value (list[tuple[str]) : プレイスホルダーに渡す値
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{data}")
            # カーソルオブジェクトはコルーチンの完了を持って設定
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
    async def commit(self):
        """
        非同期にデータベースにコミットする
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
    async def connectOpen(self):
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
    async def connectClose(self):
        """
        非同期でコネクションとカーソルのクローズ
        Raises:
            Exception : コネクトとカーソルのクローズに失敗した場合
        """
        try:
            if self.cur:
                await self.cur.close()
            if self.conn:
                self.pool.release(self.conn)
                self.cur  = None
                self.conn = None
        except Exception as e:
            msg = "コネクトとカーソルのクローズに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    async def transaction(self):
        """
        非同期でトランザクションの開始
        Raises:
            Exception : トランザクションに失敗した場合
        """
        try:
            await self.cursor()
            await self.execute("START TRANSACTION")
        except Exception as e:
            msg = "トランザクションに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    async def rollback(self):
        """
        非同期でトランザクションをロールバックする
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
        MySQLに接続中かどうか返す
        Returns:
            bool : 接続されていればTrue
        """
        return self.conn is not None
#-------------------------------------------------------------------------------
