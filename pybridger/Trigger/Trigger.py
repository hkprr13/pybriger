#-------------------------------------------------------------------------------
from ..common       import private   # プライベートメソッド
from ..common       import public    # パブリックメソッド
from ..config       import Config    # コンフィグクラス
from ..query        import Query     # クエリクラス
#-------------------------------------------------------------------------------
class Trigger:
    def  __init__(
            self,
            triggerName : str,
            tableName   : str
        ) -> None:
        """
        テーブルにトリガーを作成する
        ※出力はしない
        Args:
            triggerName (str) : トリガー名
            tableName   (str) : テーブル名
        Examples:
            trigger = Trigger(
                triggerName = "triggerName",
                tableName   = "tableName"
            )
        """
        self.__triggerName = triggerName
        self.__tableName   = tableName
    #---------------------------------------------------------------------------
    @property
    @private
    def __sqlEngine(self):
        engine = Config.sqlEngine
        if engine is None:
            raise Exception("エンジンが未設定です")
        return engine
    #---------------------------------------------------------------------------
    @private
    def __buildCreateQuery(
            self,
            timing : str,
            event  : str,
            body   : str
        ) -> Query:
        
        """
        Args:
            timing (str) : タイミング
            event  (str) : イベント  
            body   (str) : 実行するSQL文
        Raises:
            ValueError : 使用できない引数を指定している場合
        Returns:
            Query : クエリクラス
        """
        timingUpper : str = timing.upper()
        eventUpper  : str = timing.upper()
        if not timingUpper in ("BEFORE", "AFTER"):
            raise ValueError(f"使用できない引数({timing})を指定しています")
        if not eventUpper in ("INSERT", "UPDATE", "DELETE"):
            raise ValueError(f"使用できない引数({event})を指定しています")
        query = Query(
            f"CREATE TRIGGER {self.__triggerName} "
            f"{timingUpper} {eventUpper} ON {self.__tableName}"
            f"FOR EACH ROW BEGIN {body} END;"
        )
        return query
    #---------------------------------------------------------------------------
    @property
    @private
    def __buildShowQuery(self):
        """
        Show用のクエリ
        Raises:
            Exception : 未対応のエンジン時
        """
        if self.__sqlEngine == Config.MySqlEngine:
            query = "SHOW TRIGGERS;"
        elif self.__sqlEngine == Config.sqlite3Engine:
            query = "SELECT name, tbl_name, sql "\
                  + "FROM sqlite_master WHERE type='trigger';"
        else:
            raise Exception("未対応のエンジンです")
        return Query(query)
    #---------------------------------------------------------------------------
    @property
    @private
    def __buildDropQuery(self):
        """
        Delete用のクエリ
        """
        return Query(f"DROP TRIGGER IF EXISTS {self.__triggerName}")
    #---------------------------------------------------------------------------
    @public
    def create(
            self,
            timing : str,
            event  : str,
            body   : str
        ):
        """
        トリガーの作成
        Args:
            timing (str) : タイミング BEFORE AFTER
            event  (str) : イベント  INSERT UPDATE DELETE
            body   (str) : 実行するSQL文
        Examples:
            trigger = Trigger("triggerName", "tableName")
            trigger.create("before | after", "inser | update | delete", "SQL文")
        """
        self.__sqlEngine.execute(
            self.__buildCreateQuery(timing, event, body)
        )
    #---------------------------------------------------------------------------
    @public
    def show(self): 
        """
        トリガーの確認
        """
        self.__sqlEngine.execute(self.__buildShowQuery)
        return self.__sqlEngine.fetchall()
    #---------------------------------------------------------------------------
    def drop(self): 
        """
        トリガーの削除
        """
        self.__sqlEngine.execute(self.__buildDropQuery)
#-------------------------------------------------------------------------------