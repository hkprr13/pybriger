#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class UpdateRecord(Base):
    """
    レコード更新クラス
    """
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName    : str,
            columns      : str,
            values       : tuple,
        ):
        """
        レコード更新の初期化
        """
        super().__init__(tableName)
        self.__columns = columns # カラム
        self.__values  = values  # 値
    #---------------------------------------------------------------------------
    @public
    def where(self, **conditionsColumn):
        """
        指定したレコードを更新するメソッド
        Args:
            **conditionsColumn (str) : 更新したい条件カラムを指定
        Examples:
            user = User.updateRecord(name = "a", age = 20)
            user.where(id = 1) ※複数条件は指定できない
            user.execute()
            user.commit()
        Returns:
            Where : 条件指定クラスを返す
        """
        conditions = ""
        for key, value in conditionsColumn.items():
            conditions    += f"{key} = ?"
            self.__values += tuple(str(value))
        return Where(
            tableName    = self.tableName, # テーブル名
            columns      = self.__columns, # カラム
            values       = self.__values,  # 値
            conditions   = conditions,     # 条件カラム
        )
#-------------------------------------------------------------------------------
class Where(Base):
    """
    条件クラス(UpdateRecord用)
    """
    def __init__(
            self,
            tableName    : str,
            columns      : str,
            values       : tuple,
            conditions   : str,
        ) -> None:
        """
        条件クラスの初期化
        Args:
            tableName  (str)   : テーブル名
            columns    (str)   : 更新するカラム
            values     (tuple) : 値
            conditions (str)   : 条件のカラム
        """
        super().__init__(tableName)
        # クエリ
        query = f"UPDATE {tableName} SET {columns} WHERE {conditions};"
        # プレイスホルダーをSQLによって変更
        self.query = query.replace(
            "?", self.sqlEngine.PLACEHOLDER
        )
        # 値
        self.value = values
#-------------------------------------------------------------------------------