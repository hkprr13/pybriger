#-------------------------------------------------------------------------------
from ...Base    import Base
from ....common import public
#-------------------------------------------------------------------------------
class FullOuterJoin(Base):
    #--------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            joinTable : str,
            joinSql   : str            
        ):
        super().__init__(tableName)
        self.__query = f"SELECT * FROM {tableName} "\
                     + f"FULL OUTER JOIN {joinTable} ON {joinSql};"
    #--------------------------------------------------------------------------
    @property
    @public
    def query(self):
        return self.__query
    #--------------------------------------------------------------------------
    def execute(self):
        return super().execute(self.__query)
#-------------------------------------------------------------------------------