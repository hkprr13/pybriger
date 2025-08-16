#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class DropTable(Base):
    """テーブル削除クラス"""
    def __init__(self, tableName: str):
        """
        テーブル削除クラスの初期化
        Args:
            tableName (str) : テーブル名
        """
        super().__init__(tableName)
        self.query = f"DROP TABLE {self.tableName}"
#-------------------------------------------------------------------------------