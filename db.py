'''
This module is a collection of all db classes for Incident, Attacker, Counter Attack, and Pot.
'''

def _Connect_DB(database_name, table_name):
    '''
    Connects the given database file and return the given table name instance
    '''
    database = dataset.connect("sqlite:///" + str(database_name))
    table = database[str(table_name)]
    return table


def Exist(field, value, db_name, tbl_name):
    '''
    Check if the given value already exists in the given field
        of the table in the db.
    @Return True if exists, False otherwise
    '''
    table = _Connect_DB(db_name, tbl_name)
    if len(table.find_one(url_suffix = url_suffix)) > 0:
        return True
    return False

def Remove(field, value, db_name, tbl_name):
    '''
    Delete the field == value record from the given database table
    @Return: True if deletion is successful, False otherwise
    '''
    table = _Connect_DB(db_name, tbl_name)
    return table.delete(field=value)

def Add(dict_data, db_name, tbl_name):
    '''
    Inserts the dict_data into the given database and table.
    If the db does't exist, then initialize it.
    '''
    table = _Connect_DB(db_name, tbl_name)
    table.insert(dict_data)
