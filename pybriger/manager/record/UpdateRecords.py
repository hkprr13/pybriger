
#-------------------------------------------------------------------------------
from ..Base    import Base          # 基底クラス
from ...common import public        # パブリックメソッド
#-------------------------------------------------------------------------------
class UpdateRecords(Base):
    """
    複数レコード更新クラス
    """
    def __init__(
            self,
            tableName : str,
            columns   : str,
            data      : list[tuple[str]]  
        ):
        """
        複数レコード更新の初期化
        """
        super().__init__(tableName)
        self.__columns   = columns
        self.__data      = data
    #---------------------------------------------------------------------------
    @ public
    def where(self, **conditionsColumn):
        """
        指定したレコードを更新するメソッド
        Args:
            **conditionsColumns : 更新したい条件カラムを指定する
        Examples:
            user = User.updateRecords(
                name = ["a","b","c"], age = [20,22,24]
            ).where(id = [1,2,3]) ※whereも忘れずに
            user.execute()
            user.commit()
        Returns:
            Where : 条件指定クラスを返す
        """
        conditions = "" # 条件文
        datas      = [] # 値のリスト(最終的にタプルにする)
        # 成型
        for key, values in conditionsColumn.items():
            conditions += f"{key} = ?"
            # プレイスホルダーで使用できるようにする
            for i in range(len(values)):
                data = list(self.__data[i]) # appendできるようにリスト型に変更
                data.append(values[i])      # プレイスホルダーで使用できるように
                                            # 末尾にデータを足す
                datas.append(tuple(data))   # タプル型に変更し、リストに加える
        print(datas)
        return Where(
            tableName  = self.tableName, # テーブル名
            columns    = self.__columns, # カラム
            data       = datas,          # 値
            conditions = conditions,     # 条件
        )
#-------------------------------------------------------------------------------
class Where(Base):
    """
    条件クラス(UpdateRecords用)
    """
    def __init__(
            self,
            tableName  : str,
            columns    : str,
            data       : list[tuple[str]],
            conditions : str,

        ) -> None:
        """
        条件クラスの初期化
        Args:
            tableName  (str)              : テーブル名
            columns    (str)              : 更新するカラム
            values     (list[tuple[str]]) : 値
            conditions (str)              : 条件のカラム
        """
        super().__init__(tableName)
        # クエリ
        self.__query = f"UPDATE {tableName} SET {columns}" \
                     + f"WHERE {conditions};"
        # プレイスホルダーをSQLによって置き換える
        self.__query = self.__query.replace("?", self.sqlEngine.PLACEHOLDER)
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
    def values(self):
        """値"""
        return self.__data
    #---------------------------------------------------------------------------
    def execute(self):
        return super().executeAny(self.__query, self.__data)
#-------------------------------------------------------------------------------