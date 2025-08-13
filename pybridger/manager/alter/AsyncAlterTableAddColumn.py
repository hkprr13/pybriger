#-------------------------------------------------------------------------------
from ..AsyncBase import AsyncBase # 基底クラス
from ...common   import public    # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncAlterTableAddColumn(AsyncBase):
    """テーブルにカラムを追加するクラス"""
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName   : str,
            column      : str,
            dataType    : str,
            constraints : str,
        ):
        """
        テーブルにカラムを追加するクラスの初期化
        Args:
            tableName   (str) : テーブル名
            column      (str) : カラム名
            dataType    (str) : データ型
            constraints (str) : 制約
        """
        super().__init__(tableName)
        self.__query = f"ALTER TABLE {tableName} ADD " \
                     + f"{column} {dataType} {constraints};"
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    async def execute(self):
        return await super().execute(self.__query)
#-------------------------------------------------------------------------------