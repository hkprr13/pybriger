#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class DropTableIfExists(Base):
    """テーブル削除クラス"""
    def __init__(self, tableName: str):
        """
        テーブル削除クラスの初期化
        Args:
            tableName (str) : テーブル名
        """
        super().__init__(tableName)
        self.__query = f"DROP TABLE IF NOT EXISTS {self.tableName}"
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