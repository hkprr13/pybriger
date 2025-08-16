#-------------------------------------------------------------------------------
from ..Base         import Base   # 基底クラス
from ...common      import public # パブリックメソッド
from ...query       import Query  # クエリクラス
#-------------------------------------------------------------------------------
class CreateTable(Base):
    """
    テーブル作成クラス
    ※存在する場合も
    """
    def __init__(
            self,
            tableName : str,
            columns   : str
        ):
        """
        テーブル作成クラスの初期化
        Args;
            tableName (str) : テーブル名
            columns   (str) : CREATE TABLE (...);の...部分
        """
        super().__init__(tableName)
        # クエリ
        self.query = f"CREATE TABLE {tableName} ({columns});"
#-------------------------------------------------------------------------------