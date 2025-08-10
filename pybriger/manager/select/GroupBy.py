#-------------------------------------------------------------------------------
from ..Base import Base
#-------------------------------------------------------------------------------
class GroupBy(Base):
    """
        SQLのGROUP BY構文を構築・実行するクラス
        Parameters:
            tableName (str) : 対象のテーブル名
            columns   (str) : 取得するカラム（例: "name, COUNT(*)"）
            condition (str) : WHERE句で使用する条件（空文字で無条件）
            byColumn  (str) : GROUP BYでグループ化する列名
        Attributes:
            tableName (str) : テーブル名
            columns   (str) : SELECT対象のカラム
            condition (str) : 条件式（※綴りミスがあるため注意）
            byColumn  (str) : GROUP BYの対象列
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            columns   : str,
            condition : str,
            byColumn  : str
        ):
        super().__init__(tableName)
        self.tableName = tableName
        self.columns   = columns
        self.condition = condition  
        self.byColumn  = byColumn
    #---------------------------------------------------------------------------
    def getRecord(self):
        """
            GROUP BY構文を用いてレコードを取得する
            Returns:
                List[Tuple] : グループ化されたクエリの結果一覧
            Raises:
                DatabaseConnectionError : 実行時にDB接続エラーが発生した場合
        """
        # 基本となるクエリ
        query = f"SELECT {self.columns} FROM {self.tableName} "
        # 条件が存在するなら
        if self.condition == "":
            query += f"GROUP BY {self.byColumn};"
        # 条件が存在しないなら
        else:
            query += f"WHERE {self.condition} GROUP BY {self.byColumn};"
        cur = self.sqlEngine.cursor()
        cur.execute(query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    def having(self, aggregate):
        """
            GROUP BY + HAVING構文を用いて集計条件付きレコードを取得する
            Parameters:
                aggregate (Column) : HAVING句で使用する集計関数付きカラム
                                     例: Column("COUNT(*) > 1")
            Returns:
                List[Tuple] : HAVING句適用後のクエリ結果一覧
            Raises:
                DatabaseConnectionError : 実行時にDB接続エラーが発生した場合
        """
        # 基本となるクエリ
        query = f"SELECT {self.columns} FROM {self.tableName} "
        # 条件が存在するなら
        if self.condition == "":
            query += f"GROUP BY {self.byColumn} "
        # 条件が存在しないなら
        else:
            query += f"WHERE {self.condition} GROUP BY {self.byColumn} "
        # HAVING句を足す
        query += f"HAVING {aggregate.columnName};"
        cur = self.sqlEngine.cursor()
        cur.execute(query)
        return cur.fetchall()
#-------------------------------------------------------------------------------
