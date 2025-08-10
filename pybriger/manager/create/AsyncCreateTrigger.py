#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import private   # プライベートメソッド
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncCreateTrigger(AsyncBase):
    """非同期トリガーの作成"""
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName   : str,
            triggerName : str,
            timing      : str,
            event       : str,
            body        : str
        ):
        """
        非同期トリガーの作成
        Args:
            tableName   (str) : テーブル名
            triggerName (str) : トリガー名 
            timing      (str) : タイミング BEFORE AFTER
            event       (str) : イベント  INSERT UPDATE DELETE
            body        (str) : 実行するSQL文
        Examples:
            trigger = User.createTrigger(
                "tableName",
                "triggerName",
                "before | after",
                "inser | update | delete",
                "SQL文"
            )
            trigger.execute()
            trigger.commit()
        """
        super().__init__(tableName)
        self.__query = self.__buildQuery(
            tableName   = tableName,
            triggerName = triggerName,
            timing      = timing,
            event       = event,
            body        = body
        )
    #---------------------------------------------------------------------------
    @private
    def __buildQuery(
            self,
            tableName   : str,
            triggerName : str,
            timing      : str,
            event       : str,
            body        : str
        ) -> str:
        """
        トリガー作成クエリの作成用のプライベートメソッド
        Args:
            tableName   (str) : テーブル名
            triggerName (str) : トリガー名 
            timing      (str) : タイミング BEFORE AFTER
            event       (str) : イベント  INSERT UPDATE DELETE
            body        (str) : 実行するSQL文
        """
        query = f"CREATE {triggerName} "
        if timing == "before":
            query += "BEFORE " # 末尾にスペース
        elif timing == "after":
            query += "AFTER "  # 末尾にスペース
        else:
            raise Exception(f"使えない引数:{timing} を指定しています。")
        if event == "insert":
            query += "INSERT " # 末尾にスペース
        elif event == "update":
            query += "UPDATE " # 末尾にスペース
        elif event == "delete":
            query += "DELETE " # 末尾にスペース
        else:
            raise Exception(f"使えない引数:{event} を指定しています。")
        query += f"ON {tableName} EACH ROW BIGIN {body} END;"
        return query
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self) -> str:
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    async def execute(self):
        return await super().execute(self.__query)
#-------------------------------------------------------------------------------