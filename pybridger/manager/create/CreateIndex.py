#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
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
        self.__query = f"CREATE {indexName} ON {tableName} ({columns});"
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        return self.__query 
    #---------------------------------------------------------------------------
    @public
    def exexute(self):
        self.sqlEngine.execute(self.__query)
#-------------------------------------------------------------------------------