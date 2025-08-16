#-------------------------------------------------------------------------------
from ..Base         import Base   # 基底クラス
from ...common      import public # パブリックメソッド
from ...query       import Query  # クエリクラス
#-------------------------------------------------------------------------------
class DropIndex(Base):
    """インデックス削除クラス"""
    def __init__(
            self,
            tableName : str,
            indexName : str
        ):
        """
        インデックス削除クラスの初期化
        Args:
            tableName (str) : テーブル名
            indexName (str) : インデックス名
        """
        super().__init__(tableName)
        self.query = f"DROP INDEX {indexName};"
#-------------------------------------------------------------------------------