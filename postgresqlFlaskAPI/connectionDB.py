import psycopg2 as pg2 #If you don't have this -> pip install psycopg2

#Enter your database settings.
connectionDB = pg2.connect(
    database = "database_name", 
    user = "postgres", 
    password = "postgres_password",
    host = "localhost",
    port = "5433") #By default, postgres assigns port 5432.

cursor = connectionDB.cursor()

sqlCommands = {
    'insertSQL': 'INSERT INTO table_name (name, price) VALUES (%s, %s)',
    'selectAllSQL': 'SELECT * FROM table_name',
    'selectOneByIdSQL': 'SELECT * FROM table_name WHERE _id = %s',
    'updateSQL': 'UPDATE table_name SET name = %s, price = %s WHERE _id = %s',
    'deleteSQL': 'DELETE FROM table_name WHERE _id = %s'   
}