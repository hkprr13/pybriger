#-------------------------------------------------------------------------------
from ..Base    import Base   # 基底クラス
from ...common import public # パブリックメソッド
#-------------------------------------------------------------------------------
class AsyncCreateView(Base):
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
    async def where(self, **conditon):
        query = f"CREATE VIEW {self.__viewName} AS"
        con = ""
        for key, value in conditon.items():
            con += f"{key} = {value}"
        return ...
#-------------------------------------------------------------------------------