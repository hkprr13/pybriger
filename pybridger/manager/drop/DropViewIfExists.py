#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class DropViewIfExists(Base):
    """ビュー削除クラス"""
    def __init__(
            self,
            tableName : str,
            viewName  : str
        ):
        """
        ビュー削除クラスの初期化
        Args:
            tableName (str) : テーブル名
            vieName   (str) : 削除するビュー名
        """
        super().__init__(tableName)
        self.query = f"DROP VIEW IF NOT EXISTS {viewName};"
#-------------------------------------------------------------------------------