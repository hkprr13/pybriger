#-------------------------------------------------------------------------------
from .Constraints import Constraints # 基底クラス
from ..common     import private     # プライベートメソッド
from ..common     import public      #　パブリックメソッド
#-------------------------------------------------------------------------------
class ForeignKey(Constraints):
    """
    外部キー制約の定義クラス
    """
    def __init__(
            self,
            referenceName : str,
            onUpdate      : bool | None = None,
            onDelete      : bool | None = None
        ):
        """
        外部キー制約の定義クラス 
        Args: 
            referenceName (str)  : "table.column" 形式の参照名 
            onUpdate      (bool | None) : ON UPDATE CASCADE の適用有無 
                                          Noneなら未明示 
            onDelete      (bool | None) : ON DELETE CASCADE の適用有無 
                                          Noneなら未明示 
        """
        self.setReferenceName(referenceName)
        # カラムの変更があった場合,更新するかどうか
        self.onUpdate = onUpdate
        # カラムの変更があった場合,削除するかどうか
        self.onDelete = onDelete
    #---------------------------------------------------------------------------
    @private
    def setReferenceName(self, referenceName : str):
        # 文字列かどうか判断
        if not isinstance(referenceName, str):
            raise TypeError("文字列である必要があります")
        else: pass
        strings : list = referenceName.split(".")
        # 指定された文字列を分離させる
        # User.user_id
        if  len(strings) == 2:
            # 参照先のテーブル
            self.referencedTable  = strings[0] # User
            # 参照先のカラム
            self.referencedColumn = strings[1] # user_id
        else:
            raise ValueError(
                f"入力された値 '{referenceName}' が間違っています"
            )
    #---------------------------------------------------------------------------
    @public
    def getReferencedTable(self) -> str:
        """
        参照先のテーブル名の取得
        Returns:
            参照先のテーブル名
        """
        return self.referencedTable
    #---------------------------------------------------------------------------
    @public
    def getReferencedColumn(self) -> str:
        """
        参照先のテーブルのカラムの取得
        Returns:
            str : 参照先のテーブルのカラム
        """
        return self.referencedColumn
    #---------------------------------------------------------------------------
    @public
    def getOnUpdate(self) -> bool | None:
        """
        更新時に連動するかを取得
        Returns:
            bool : 更新するならTrue
                   しないならFalse
                   未明示ならNone
        """
        return self.onUpdate
    #---------------------------------------------------------------------------
    @public
    def getOnDelete(self) -> bool  | None:
        """
        削除時に連動するかを取得
        Returns:
            bool : 更新するならTrue
                   しないならFalse
                   未明示ならNone
        """
        return self.onDelete
    #---------------------------------------------------------------------------
    @public
    def toSql(self) -> str:
        """
        外部キー制約をSQL形式で返す
        Returns:
            str : 外部キー制約のSQL文
        Notes:
            FOREIGN KEY (~~~) ... で出力されるのでカラム名が決定したら
            ~~~を入れ替える必要あり
        """
        # SQL
        sql = f"FOREIGN KEY (~~~) "\
            + f"REFERENCES {self.referencedTable}({self.referencedColumn})"
        # 更新時に連動するなら
        if self.onUpdate is None:
            pass # Noneならsqlに未明示
        elif self.onUpdate == True:
            sql += " ON UPDATE CASCADE"
        else:
            sql += " ON UPDATE NO ACTION"
        # 削除時に連動するなら
        if self.onDelete is None:
            pass # Noneならsqlに未明示
        elif self.onDelete == True:
            sql += " ON DELETE CASCADE"
        else:
            sql += " ON DELETE NO ACTION"
        return sql
#-------------------------------------------------------------------------------