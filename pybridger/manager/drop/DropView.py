#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class DropView(Base):
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
        self.__query = f"DROP VIEW {viewName};"
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    def execute(self):
        self.sqlEngine.execute(self.__query)
#-------------------------------------------------------------------------------