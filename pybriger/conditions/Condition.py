#-------------------------------------------------------------------------------
from ..column   import Column
#-------------------------------------------------------------------------------
class Condition:
    #---------------------------------------------------------------------------
    def __init__(self, left, operator = None, right = None):
        self.left     = left
        self.operator = operator
        self.right    = right
    #---------------------------------------------------------------------------
    def toSql(self, placeHolder = "?"):
        # leftがConditonオブジェクトなら,再帰的にtoSql()を呼び出す
        if isinstance(self.left, Condition):
            # 複数条件をネストしてSQLに変換するため
            leftSql, leftValues = self.left.toSql(placeHolder)
        # leftが単なる列名の場合文字列化してSQLとして扱う
        else:
            leftSql    = str(self.left)
            leftValues = []
        if self.right is not None \
        and hasattr(self.right, "toSql"):
            rightSql, rightValues = self.right.toSql()
            sql = f"{leftSql} {self.operator} {rightSql}"
            return sql, leftValues + list(rightValues)
        
        # NULL判定(IS NULL / IS NOT NULL)
        if  isinstance(self.right, str) and self.right.upper() == "NULL":
            sql = f"{leftSql} {self.operator} NULL"
            return sql, leftValues

        # IN/NOT IN条件の場合
        # rightがリストやタプルかどうか確認
        if  self.operator in ("IN", "NOT IN") \
        and isinstance(self.right, (list, tuple)):
            if not self.right:
                raise ValueError("IN句に空のリストは使えません")
            # INの中身の値の個数に応じて, プレイスホルダーを並べる
            placeHolders = ", ".join([placeHolder] * len(self.right))
            sql = f"{leftSql} {self.operator} ({placeHolders})"
            return sql, leftValues + list(self.right)
        
        # BETWEEN/NOT BETWEEN条件の場合
        # 値は(下限, 上限)である必要あり
        if self.operator == "BETWEEN" \
        and  isinstance(self.right, (tuple, list)) \
        and  len(self.right) == 2:
            sql = f"{leftSql} {self.operator} {placeHolder} AND {placeHolder}"
            return sql, [self.right[0], self.right[1]]

        # LIKE/NOT LIKE条件の場合
        if self.operator in ("LIKE", "NOT LIKE"):
            sql = f"{leftSql} {self.operator} {placeHolder}"
            return sql, leftValues + [self.right]
        
        # 論理式(AND/OR/NOT)
        # rightがconditionオブジェクトなら, 再帰的にtoSql()を呼び出す
        if isinstance(self.right, Condition):
            rightSql, rightValues = self.right.toSql(placeHolder)
            sql = f"{leftSql} {self.operator} {rightSql}"
            return sql, leftValues + rightValues
        
        # 単独NOT
        if self.operator == "NOT" and isinstance(self.right,Condition):
            rightSql, rightValues = self.right.toSql(placeHolder)
            sql = f"(NOT {rightSql})"
            return sql, rightValues
        
        # 通常の比較演算子(=, !=, >, ...)
        sql = f"({leftSql} {self.operator} {placeHolder})"
        return sql, \
               leftValues + ([self.right] if self.right is not None else [])
    #---------------------------------------------------------------------------
    def __and__(self, other):
        return Condition(self, "AND", other)
    #---------------------------------------------------------------------------
    def __or__(self, other):
        return Condition(self, "OR", other)
#-------------------------------------------------------------------------------