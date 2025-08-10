#-------------------------------------------------------------------------------
from ..common     import private   # プライベートメソッド
from ..common     import public    # パブリックメソッド
from ..config     import Config    # コンフィグクラス
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
        query = f"CREATE {self.__triggerName} " # 末尾にスペース
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
        query += f"ON {self.__tableName} EACH ROW BIGIN {body} END;"
        self.__sqlEngine.execute(query)
    #---------------------------------------------------------------------------
    @public
    def show(self): 
        """
        トリガーの確認
        """
        self.__sqlEngine.execute("SHOW TRIGGERS;")
    #---------------------------------------------------------------------------
    def drop(self): 
        """
        トリガーの削除
        """
        self.__sqlEngine.execute(
            f"DROP TRIGGER IF EXISTS {self.__triggerName}"
        )
#-------------------------------------------------------------------------------