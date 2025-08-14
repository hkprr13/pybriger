#-------------------------------------------------------------------------------
from ...Base    import Base
from ....common import public
#-------------------------------------------------------------------------------
class InnerJoin(Base):
    #--------------------------------------------------------------------------
    def __init__(
            self,
            tableName : str,
            columns   : str,
            joinTable : str,
            joinSql   : str,
            
        ):
        super().__init__(tableName)
        self.__query = f"SELECT {columns} FROM {tableName} "\
                     + f"INNER JOIN {joinTable} ON {joinSql};"
    #--------------------------------------------------------------------------
    @property
    @public
    def query(self):
        return self.__query
    #--------------------------------------------------------------------------
    def execute(self):
        return super().execute(self.__query)
#-------------------------------------------------------------------------------