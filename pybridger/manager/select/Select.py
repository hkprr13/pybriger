#-------------------------------------------------------------------------------
from ..Base        import Base           # ベース
from .GroupBy      import GroupBy        # GROUP BY
from .Where        import Where          # WHERE
from .join         import CrossJoin      # CROSS JOIN句
from .join         import FullOuterJoin  # FULL OUTER JOIN句
from .join         import InnerJoin      # INNER JOIN句
from .join         import LeftJoin       # LEFT JOIN句
from .join         import NaturalJoin    # NATURAL JOIN句
from .join         import RightJoin      # RIGHT JOIN句
from .join         import SelfJoin       # SELF JOIN句
from ...column     import Column         # カラムクラス
from ...conditions import Condition      # 条件クラス
from ...conditions import ConditionGroup # 複数条件クラス
from ...common     import public         # パブリックメソッド
from ...model      import Model          # モデルクラス
#-------------------------------------------------------------------------------
class Select(Base):
    """SELECTクラス"""
    #---------------------------------------------------------------------------
    def __init__(
            self,
            tableName  : str, 
            columns    : str,
        ) -> None:
        """"
        SELECTクラスの初期化
        Args:
            tableName (str) : テーブル名
            columns   (str) : カラム
        """
        super().__init__(tableName)
        self.__columns = columns
        self.__query   = ""
    #---------------------------------------------------------------------------
    @property
    @public
    def query(self):
        """クエリ"""
        return self.__query
    #---------------------------------------------------------------------------
    @public
    def getRecord(self) -> list:
        """
        指定したカラムの全てのレコードを取得する
        Returns:
            List : クエリ結果のレコードリスト
        """
        # クエリ
        self.__query = f"SELECT {self.__columns} FROM {self.tableName};"
        # クエリから結果を取得する
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def getAllRecord(self) -> list:
        """
        テーブル内の全カラムの全てのレコードを取得する
        Returns:
            List : クエリ結果のレコードリスト
        """
        # クエリ
        self.__query = f"SELECT * FROM {self.tableName};"
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def where(
            self,
            *condition : Condition | ConditionGroup
        )-> Where:
        """
        WHERE句
        Args:
            *condition (Condition | ConditionGroup) : 条件
        Examples:
            engine = Engine(...)
            engine.launch()
            user   = engine.select(User, User.id, User.name)
            result = user.where((User.age >= 20) & (User.age <= 29)).fetchall()
        """
        placeHolder = self.sqlEngine.PLACEHOLDER
        parts  = []
        values = []
        for cond in condition:
            sql, vals = cond.toSql(placeHolder)
            parts.append(sql)
            values.extend(vals)
        whereClause = " AND ".join(parts)
        values = tuple(values)            
        return Where(
            tableName = self.tableName,
            columns   = self.__columns,
            condition = whereClause,
            value     = values
        )
    #---------------------------------------------------------------------------  
    @public
    def orderBy(
            self,
            asc  : Column | None = None, # 昇順
            desc : Column | None = None, # 降順
        ) -> list:
        """
        データを昇順・降順で並び替える
        Args:
            asc  (Column) : 昇順にソートするカラム
            desc (Column) : 降順にソートするカラム
        Returns:
            list : 並び替え後のレコードリスト
        """
        query = f"SELECT {self.__columns} FROM {self.tableName} "
        # ASCが未指定かつ, DESCが未指定
        if asc is None and desc is None:
            raise Exception("ascまたはdescのいずれかを指定してください")
        # ASCが未指定かつ, DESCが指定されている
        if asc is None and not desc is None:
            query += f"ORDER BY {desc.columnName} DESC;"
         # ASCが指定されている, かつDESCが未指定
        if not asc is None and desc is None:  
            query += f"ORDER BY {asc.columnName} ASC;"
         # ASCが指定されている, かつDESCがされている
        if not desc is None and not asc is None:
            query += f"ORDER BY {asc.columnName} ASC, {desc.columnName} DESC;"
        cur = self.cursor()
        cur.execute(query)
        self.__query = query
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def limitOffset(
            self,
            limit  : int,
            offset : int
        ) -> list:
        """
        LIMITとOFFSETを使ってページネーションされたレコードを取得する
        Args:
            limit  (int) : 最大取得件数
            offset (int) : 取得開始位置
        Returns:
            list : クエリ結果の一部
        """
        #クエリ
        query = f"SELECT {self.__columns} " \
              + f"FROM {self.tableName} " \
              + f"LIMIT {limit} OFFSET {offset}"
        cur = self.sqlEngine.cursor()
        cur.execute(query)
        self.__query = query
        return cur.fetchall()
    #---------------------------------------------------------------------------  
    @public
    def count(self):
        """
        レコード件数を取得する
        Returns:
            int : 件数のタプル
        """
        # クエリ
        self.__query = f"SELECT COUNT(*) " \
                     + f"FROM {self.tableName} "
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def getAvg(
            self,
            column : Column
        ):
        """
        指定列の平均値を取得する
        Returns:
            List[Tuple] : 平均値のタプル (例: [(34.5,)])
        """
        self.__query = f"SELECT AVG({column.columnName}) " \
                     + f"FROM {self.tableName} "    
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def getSum(
            self,
            column : Column
        ):
        """
        指定列の合計値を取得する
        Args:
            column (Column) : 対象カラム
        Returns:
            List[Tuple] : 合計値のタプル
        """
        self.__query = f"SELECT SUM({column.columnName}) " \
                     + f"FROM {self.tableName} "    
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def getMax(
            self,
            column : Column
        ):
        """
        指定列の最大値を取得する
        Args:
            column (Column) : 対象カラム
        Returns:
            List[Tuple] : 最大値のタプル
        """
        self.__query = f"SELECT Max({column.columnName}) " \
                     + f"FROM {self.tableName} "    
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def getMin(
            self,
            column : Column
        ):
        """
        指定列の最小値を取得する
        Args:
            column (Column) : 対象カラム
        Returns:
            List[Tuple] : 最小値のタプル
        """
        self.__query = f"SELECT Min({column.columnName}) " \
                     + f"FROM {self.tableName} "    
        cur = self.sqlEngine.cursor()
        cur.execute(self.__query)
        return cur.fetchall()
    #---------------------------------------------------------------------------
    @public
    def groupBy(
            self,
            column : Column  # グループ化する列
        ):
        """
        指定列でGROUP BYを実行する
        Args:
            column (Column) : グループ化対象のカラム
        Returns:
            GroupBy : グループ化クエリオブジェクト
        """
        return GroupBy(
            tableName = self.tableName,
            columns   = self.__columns,
            condition = "",
            byColumn  = column.columnName
        )
    #---------------------------------------------------------------------------
    @public
    def whereGroupBy(
            self,
            condition, # 条件
            column : Column  # グループ化する列
        ):
        """
        WHERE + GROUP BY句による条件付きグループ化
        Args:
            condition (str) : WHERE条件式
            column    (Column) : グループ化対象のカラム
        Returns:
            GroupBy : グループ化クエリオブジェクト
        """
        return GroupBy(
            tableName = self.tableName,
            columns   = self.__columns,
            condition = condition,
            byColumn  = column.columnName
        )
    #---------------------------------------------------------------------------
    @public
    def crossJoin(
            self
        ):
        """
        """
        return CrossJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public
    def fullOuterJoin(
            self
        ):
        """
        """
        return FullOuterJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public
    def innerJoin(
            self,
            joinTable : type[Model],
            *condition   : Condition
        ):
        """
        """
        placeHolder = self.sqlEngine.PLACEHOLDER
        parts  = []
        values = []
        for cond in condition:
            sql, vals = cond.toSql(placeHolder)
            parts.append(sql)
            values.extend(vals)
        whereClause = " AND ".join(parts)
        values = tuple(values)
        print(whereClause)
        print(values)
        return InnerJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public
    def leftJoin(
            self
        ):
        """
        """
        return LeftJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public 
    def naturalJoin(
            self
        ):
        """
        
        """
        return NaturalJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public
    def RightJoin(
            self
        ):
        """
        """
        return RightJoin(
            tableName = self.tableName
        )
    #---------------------------------------------------------------------------
    @public
    def selfJoin(
            self
        ):
        """
        """
        return SelfJoin(
            tableName = self.tableName
        )

#-------------------------------------------------------------------------------