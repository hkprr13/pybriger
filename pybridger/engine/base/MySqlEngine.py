#-------------------------------------------------------------------------------
from typing         import Any              # Any型クラス
from .SqlEngine     import SqlEngine        # 基底SQLエンジンクラス
from .datetypes     import MySqlDateTypes   # MySQLのデータ型クラス
from ...common      import override         # オーバライドメソッド
from ...common      import public           # パブリックメソッド
from ...common      import private          # プライベートメソッド
from ...Log         import Log              # ログクラス
#-------------------------------------------------------------------------------
class MySqlEngine(SqlEngine, MySqlDateTypes):
    """
    MySQLエンジンクラス
    Attributes:
        hostName     (str)             : ホスト名
        userName     (str)             : ユーザー名
        password     (str)             : パスワード
        databaseName (str)             : データベース名
        sqlEngine    (mysql.connector) : mysql.connectorクラス
        conn         (Any | None)      : mysqlコネクトオブジェクト
        cur          (Any | None)      : mysqlカーソルオブジェクト
        __isLog      (bool)            : ログフラグ 
        __Log        (Log)             : ログオブジェクト
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
        MySQLエンジンの初期化
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
        # インスタンス変数(オブジェクト)
        # インスタンスされたタイミングでインポートを行う
        try:
            import mysql.connector
            self.sqlEngine  = mysql.connector
        except Exception as e:
            raise Exception(
                "mysql.connnectorがインストールされていません\n"
                "下記をターミナルで実行してください\n"
                "pip install mysql-connector-python"
            )
        # コネクトオブジェクトとカーソルオブジェクトの初期化
        self.conn       = None # 初期値はNone
        self.cur        = None # 初期値はNone
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
            ProgrammingError : 認証エラーやデータベース指定ミス
            InterfaceError   : ソケットエラーやネットワークの接続エラー
            Error            : その他のMySQLエラー
        """
        try:
            self.conn = self.sqlEngine.connect(
                host     = self.hostName,
                user     = self.userName,
                password = self.password,
                database = self.databaseName
            )
            # 問題なければ返す
            return self.conn
        # データベースとの接続が切れた場合
        except self.sqlEngine.errors.OperationalError as oe:
            try:
                self.__logInfo("接続が切れています。再接続を試みます...")
                # 再接続を試みる
                self.conn = self.sqlEngine.connect(
                    host     = self.hostName,
                    user     = self.userName,
                    password = self.password,
                    database = self.databaseName
                )
                return self.conn
            # 再接続に失敗した場合
            except Exception as e:
                msg = "MySQLの再接続に失敗しました"
                # ログ
                self.__logError(msg)
                print(f"{msg}: {e}")
                raise Exception
        # 認証エラーやデータベース指定ミスの場合
        except self.sqlEngine.errors.ProgrammingError as pe:
            msg = "認証エラーやデータベース指定ミスです"
            self.__logError(msg)
            raise Exception(f"{msg}: {pe}")
        # ネットワークの接続やソケットエラーの場合
        except self.sqlEngine.errors.InterfaceError as ie:
            msg = "ソケットエラーやネットワークの接続エラーです"
            self.__logError(msg)
            raise Exception(f"{msg}: {ie}")
        except self.sqlEngine.errors.Error as e:
            # ユーザ名またはパスワードが違う場合
            if e.errno == 1045:
                msg = "ユーザ名またはパスワードが間違っています"
                self.__logError(msg)
                raise Exception(msg)
            # 指定されたデータベースが存在しない場合
            elif e.errno == 1049:
                msg = "指定されたデータベースが存在しません"
                self.__logError(msg)
                raise Exception(msg)
            # その他
            else:
                msg = f"MySQLエラー({e.errno})です"
                self.__logError(msg)
                raise Exception(f"{msg}: {e.msg}")
    #---------------------------------------------------------------------------
    @override
    @public
    def cursor(
            self,
            dictionary : bool = False
        ) -> Any: # Anyじゃないとエラーになりやすい
        """
        カーソルの作成
        Args:
            dictionary (bool) : 辞書型の指定
        Returns:
            Any : カーソルオブジェクトを返す
        Raises:
            Exception : カーソルの失敗した場合
        """
        try:
            # 接続されていなければ
            if self.conn is None or not self.conn.is_connected():
                self.connect()
            assert self.conn is not None # 明示する
            if self.cur:
                try:
                    self.cur.close()
                except Exception:
                    pass # カーソルが閉じ済みの時用
            self.cur = self.conn.cursor(dictionary = dictionary)
            return self.cur
        except Exception as e:
            msg = "カーソルの作成に失敗しました"
            self.__logError(msg)
            raise Exception(f"{msg}: {e}")
    #---------------------------------------------------------------------------
    @override
    @public
    def execute(self, query: str, value : tuple = ()) -> None:
        """
        クエリの実行
        Args:
            query (str)     : SQL文
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
    def executeAny(self, query: str, data : list[tuple[str]]) -> None:
        """
        クエリの実行(複数)
        Args:
            query (str)             : SQL文
            value (list[tuple[str]) : プレイスホルダーに渡す値
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
            if self.conn and self.conn.is_connected():
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
            if self.conn and self.conn.is_connected():
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
            if self.conn and self.conn.is_connected():
                self.cursor().execute("START TRANSACTION")
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
            if self.conn and self.conn.is_connected():
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
        return self.conn is not None and self.conn.is_connected()
#-------------------------------------------------------------------------------