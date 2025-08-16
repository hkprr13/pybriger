#-------------------------------------------------------------------------------
from ..Base         import Base   # 基底クラス
from ...common      import public # パブリックメソッド
from ...query       import Query  # クエリクラス
#-------------------------------------------------------------------------------
class CreateIndex(Base):
    """インデックス作成クラス"""
    def __init__(
            self,
            indexName : str,
            tableName : str,
            columns   : str
        ):
        """
            インデックス作成クラス
            Args:
                indexName (str) : インデックス名
                tableName (str) : テーブル名
                columns   (str) : カラム(文字列形式)
        """
        super().__init__(tableName)
        self.query = f"CREATE {indexName} ON {tableName} ({columns});"
#-------------------------------------------------------------------------------