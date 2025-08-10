#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class InsertRecords(Base):
    """
    レコードを複数挿入するクラス
    """
    def __init__(
            self,
            tableName    : str,
            columns      : str,
            data         : list[tuple[str]],
            placeHolders : str
        ):
        """
        レコード挿入の初期化
        Args:
            tableName    (str)              : テーブル名
            columns      (str)              : カラム(str) id, name, age
            data         (list[tuple[str]]) : 値
                                              [(1,  2,  3 ),
                                               (a,  b,  c ),
                                               (19, 22, 17)]
            placeHolders (str)              : プレイスホルダー
        """
        # オーバーロード
        super().__init__(tableName)        
        # プレイスホルダーをSQLによって変える       
        placeHolders = placeHolders.replace(
            "?", self.sqlEngine.PLACEHOLDER
        )
        # クエリ
        self.__query = f"INSERT INTO {self.tableName} "\
                     + f"({columns}) VALUES ({placeHolders});"
        # 値
        self.__data = data
    #---------------------------------------------------------------------------
    @public
    @property
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    @property
    def data(self):
        """値"""
        return self.__data
    #---------------------------------------------------------------------------
    @public
    def execute(self):
        return super().executeAny(self.__query, self.__data)
#-------------------------------------------------------------------------------