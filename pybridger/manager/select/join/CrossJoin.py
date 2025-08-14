#-------------------------------------------------------------------------------
from ...Base    import Base
from ....common import public
#-------------------------------------------------------------------------------
class CrossJoin(Base):
    #--------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            joinTable : str,            
        ):
        super().__init__(tableName)
        self.__query = f"SELECT * FROM {tableName} "\
                     + f"CROSS JOIN {joinTable};"
    #--------------------------------------------------------------------------
    @property
    @public
    def query(self):
        return self.__query
    #--------------------------------------------------------------------------
    def execute(self):
        return super().execute(self.__query)
#-------------------------------------------------------------------------------