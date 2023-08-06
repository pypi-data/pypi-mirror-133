import sqlite3
from sqlite3 import Cursor
from typing import Any

quote = '"'
class Field:
    def __init__(self, data:"Data"):
        self.data = data
        self.name:str = data.name
        self.type = data.type



    def to_python(self):
        pass



class Data:
        def __init__(self, db: "Sqlite3View", table: "Table", data:"Data"={}):
            self.db:Sqlite3View = db
            self.data:Data = data
            self.table:Table = table
            self._keys = []
            self._values = []
            self.attrs = ['data', '_keys', '_values', 'attrs']
            for k, v in data.items():
                self._keys.append(k)
                self._values.append(v)
                setattr(self, k, v)
            self.__getitem__ = self.data.__getitem__
            
        
        def __getattr__(self, key) -> "Data":
            return self.data.get(key, None)
        
        def __repr__(self) -> str:
            return f"<Data values={list(self.data.keys())} id={self.id} >"
        
        def __iter__(self) -> list:
            for i in range(len(self._values)):
                yield self._values[i]
        
        def update(self, **kwargs) -> "Data":
            sql = f"""UPDATE {self.table.name}
            SET { " AND ".join("{k}={v}".format(k=k, v=v) for k, v in kwargs.items()) }
            WHERE id = {self.id} """
            self.db.exec(sql)
            new_data = self.table(id=self.id)
            return new_data[0]

        def delete(self) -> None:
            self.db.exec(f"DELETE FROM {self.table.name} WHERE id={self.id};")
                

class Table:
        def __init__(self, db:"Sqlite3View", data:dict):
            self.name: str = data.name
            self.db: Sqlite3View = db
            self.fields: list = self.db._fields(self)
            
        
        def __repr__(self) -> str:
            return f"<Table name='{self.name}' >"

        @property
        def values(self, columns:list=[]) -> list:
            return self.db.exec(f"SELECT { '*' if len(columns) == 0 else ', '.join(columns)[:-1] } FROM %s" % self.name)
        
        def __call__(self,*args,**kwargs) -> list:
            columns = "*" if len(args) == 0 else ", ".join(args)
            filt = "WHERE " + " AND ".join("{k}={v}".format(k=k, v=v) for k, v in kwargs.items()) if kwargs else ""
            res = self.db.exec(f"""SELECT {columns} FROM "{self.name}" {filt}""", commit=True, table=self)
            return res
        
        def get(self, _id:int, *args):
            columns = "*" if len(args) == 0 else ", ".join(args)
            res = self.db.exec(f"""SELECT {'id,' if 'id' not in args else "" if columns == "*" else ""} {columns} FROM "{self.name}" WHERE id={_id}""", commit=True, table=self)
            return res


        def create(self, **kwargs) -> Data:
            columns = ', '.join('{k}'.format(k=k) for k in kwargs.keys())
            print(columns)

            values = ', '.join(f'{ quote if isinstance(k, str) else "" }{k}{ quote if isinstance(k, str) else "" }'for k in kwargs.values() )
            print(values)
            self.db.exec(f"INSERT INTO {self.name} ({ columns}) VALUES ({ values });")
            return self.get(self()[-1].id, 'chat_id')

        def delete(self) -> None:
            self.db.exec(f"DROP TABLE {self.name};")

        def __getitem__(self, key:int) -> "Data":
            return self.get(key)
        
        def clear(self) -> None:
            self.db.exec(f"DELETE FROM {self.name};")
        
        def __delattr__(self, name:str):
            data = self[name]
            if data is not None: data.delete()

        
        

        
class Dataset:
    def __init__(self, table:Table) -> None:
        self.table:Table = table
        self.db = self.table.db


class Sqlite3View:
    def __init__(self, path: str=":memory:"):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = self.dict_factory
        self.cursor: Cursor = self.db.cursor()
    
    def dict_factory(self, cursor:Cursor, row:tuple) -> Data:
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return Data(self, self.executing_table, d)

    @property
    def cur(self) -> None:
        self.cursor = self.db.cursor()

    @property
    def commit(self): self.db.commit()

    def exec(self, sql: str, commit: bool = True, table:Table=None) -> list:
        self.executing_table = table
        self.cursor.execute(sql)
        self.executing_table = table
        if commit: self.commit
        return self.cursor.fetchall()
    

    def _tables(self, name:str=None) -> list:
        if name is None:
            tables: list = self.exec(f"""SELECT * FROM sqlite_schema WHERE type='table';""")
            res: list = []

            for data in tables:
                res.append(Table(self, data))
            return res
        else:
            res = self.exec(f"""SELECT * FROM sqlite_schema WHERE type='table' AND name="{name}";""")
            return Table(self, res[0]) if res != [] else None


    @property
    def tables(self) -> list[Table]:
        return self._tables()
    
    def __getattr__(self, name:str) -> Table:
        return self._tables(name)


    def __getitem__(self, name:str) -> Table:
        return self._tables(name)

    def _fields(self, table:Table) -> list:
        fields: list = self.exec(f"PRAGMA table_info({table.name});")
        res:list = []
        for field in fields:
            res.append(Field(field))
        return res
    
    def __delattr__(self, name) -> None:
        table:Table = getattr(self, name)
        if table is not None: table.delete()