#-------------------------------------------------------------------------------
from ..Base         import Base   # 基底クラス
from ...common      import public # パブリックメソッド
from ...query       import Query  # クエリクラス
#-------------------------------------------------------------------------------
class CreateTableIfNotExists(Base):
    """テーブル作成クラスの初期化"""
    def __init__(
            self,
            tableName : str,
            columns   : str
        ):
        """
        テーブル作成クラスの初期化
        Args:
            tableName (str) : テーブル名
            columns   (str) : CREATE TABLE (...);の...部分
        """
        super().__init__(tableName)
        self.query = f"CREATE TABLE IF NOT EXISTS {tableName} ({columns});"
#-------------------------------------------------------------------------------