#-------------------------------------------------------------------------------
# aiosqliteのインストールが出来ているかどうか確認
try:
    import aiosqlite
except Exception as e:
    raise Exception(
        "aiosqliteがインストールされていません\n"
        "下記をターミナルで実行してください\n"
        "pip install aiosqlite"
    )
#-------------------------------------------------------------------------------
from .SqlEngine     import SqlEngine        # 規定SQLエンジンクラス
from .datetypes     import Sqlite3DateTypes # Sqlite3のデータ型クラス
from ...common      import override         # オーバライドメソッド
from ...common      import public           # パブリックメソッド
from ...common      import private          # プライベートメソッド
from ...Log         import Log              # ログクラス
#-------------------------------------------------------------------------------
class AsyncSqlite3Engine(SqlEngine, Sqlite3DateTypes):
    """
    非同期Sqlite3エンジンクラス
    Attributes:
        database  (str)                         : データベースパス名
        sqlEngine (aiosqlite)                   : sqlite3クラス
        conn      (aiosqlite.Connection | None) : sqlite3コネクトオブジェクト
        cur       (aiosqlite.Cursor     | None) : sqlite3カーソルオブジェクト
        __isLog   (bool)                        : ログフラグ 
        __Log     (Log)                         : ログオブジェクト
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            databasePath : str,
            logFile      : str | None = None
        ):
        """
        非同期SQLite3データベース接続エンジンの初期化
        Args:
            databasePath (str)        : データベースパス
            logFile      (str | None) : ログファイル名
        """
        super().__init__()
        # インスタンス変数
        self.database  = databasePath # データベースパス
        self.sqlEngine = aiosqlite    # 非同期対応のSqlite3エンジン
        # カーソルとコネクト      
        self.conn : aiosqlite.Connection | None = None # ← 明示的に定義
        self.cur  : aiosqlite.Cursor     | None = None # ← 明示的に定義
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
    async def connect(self) -> aiosqlite.Connection:
        """
        非同期でデータベースの接続
        Returns:
            aiosqlite.Connection : コネクトオブジェクト 
        Raises:
            Exception : データベースの接続に失敗した場合
        """
        try:
            # 戻り値はエンジンのコルーチンの完了を待って設定
            self.conn = await self.sqlEngine.connect(self.database)
            return self.conn
        except Exception as e:
            msg = "データベースの接続に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    async def cursor(self) -> aiosqlite.Cursor:
        """
        非同期にカーソルを作成
        Returns:
            aiosqlite.Cursor : カーソルオブジェクト
        Raises:
            Exception : カーソルの作成に失敗した場合
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
            self.cur = await self.conn.cursor()
            return self.cur
        except Exception as e:
            msg = "カーソルの作成に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------    
    @override
    @public
    async def execute(self, query : str, value : tuple = ()) -> None:
        """
        非同期にSQLクエリを実行する
        Args:
            query (str)     : 実行するクエリ文
            value (tuple)   : プレイスホルダーに渡す値
        Raises:
            Exception : クエリの実行に失敗した場合
        """
        try:
            self.__logDebug(f"クエリ:{query}, 値:{value}")
            # カーソルオブジェクトはコルーチンの完了を持って設定
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
        非同期にトランザクションにコミットする
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
    async def connectClose(self) -> None:
        """
        コネクションとカーソルのクローズ(非同期)
        Raises:
            Exception : コネクトとカーソルのクローズに失敗した場合
        """
        try:
            # コネクトが接続していれば
            if self.conn:
                await self.conn.close()
                self.conn = None
                self.cur  = None
        except Exception as e:
            msg = "コネクトとカーソルのクローズに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------
    #---------------------------------------------------------------------------
    @override
    @public
    async def transaction(self) -> None:
        """
        非同期でトランザクションの開始
        Raises:
            Exception : トランザクションに失敗した場合
        """
        try:
            if self.conn:
                await self.execute("BEGIN")
        except Exception as e:
            msg = "トランザクションに失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}") 
    #---------------------------------------------------------------------------
    @override
    @public
    async def rollback(self) -> None:
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
        Sqlite3に接続中かどうか返す
        Returns:
            bool : 接続されていればTrue
        """
        return self.conn is not None
#-------------------------------------------------------------------------------