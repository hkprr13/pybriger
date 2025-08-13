#-------------------------------------------------------------------------------
from ...Base import Base
#-------------------------------------------------------------------------------
class InnerJoin(Base):
    def __init__(self, tableName: str):
        super().__init__(tableName)
        query = f""