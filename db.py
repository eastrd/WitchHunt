'''
This module is a collection of all db classes for Incident, Attacker, Counter Attack, and Pot.
'''

def Connect_DB(database_name, table_name):
    '''
    Connects the given database file and return the given table name instance
    '''
    database = dataset.connect("sqlite:///" + str(database_name))
    table = database[str(table_name)]
    return table


def Exist(self, field, value, db_name, tbl_name):
    '''
    Check if the given value already exists in the given field
        of the table in the db.
    @Return True if exists, False otherwise
    '''
    table = Connect_DB(db_name, tbl_name)
    if len(table.find_one(url_suffix = url_suffix)) > 0:
        return True
    return False
