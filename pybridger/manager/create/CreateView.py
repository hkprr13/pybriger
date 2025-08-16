#-------------------------------------------------------------------------------
from ..Base     import Base   # 基底クラス
from ...common  import public # パブリックメソッド
from ...query   import Query  # クエリクラス
#-------------------------------------------------------------------------------
class CreateView(Base):
    def __init__(
            self,
            viewName  : str,
            tableName : str,
            columns   : str
        ):
        super().__init__(tableName)
        self.__viewName  = viewName
        self.__columns   = columns
    #---------------------------------------------------------------------------
    @public
    def where(self, **conditon):
        return ...
#-------------------------------------------------------------------------------

class Where(Base):
    def __init__(self, tableName: str):
        super().__init__(tableName)