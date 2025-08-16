#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class InsertRecord(Base):
    """
    レコードを挿入するクラス
    """
    def __init__(
            self,
            tableName    : str,
            columns      : str,
            values       : tuple,
            placeHolders : str
        ):
        """
        レコード挿入の初期化
        Args:
            tableName    (str)   : テーブル名
            columns      (str)   : カラム(str) id, name, age
            values       (tuple) : 値 1, "name", 19
            placeHolders (str)   : プレイスホルダー
        """
        # オーバーロード
        super().__init__(tableName)        
        # プレイスホルダーをSQLによって変える
        placeHolders = placeHolders.replace(
            "?", self.sqlEngine.PLACEHOLDER
        )
        # クエリ
        self.query = f"INSERT INTO {self.tableName} "\
                     + f"({columns}) VALUES ({placeHolders});"
        # 値
        self.value = values
#-------------------------------------------------------------------------------