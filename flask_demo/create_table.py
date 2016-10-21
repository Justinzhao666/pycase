
import sqlite3

conn = sqlite3.connect('/home/wwha/script/pyspace/Engine/config/data/db_engine.db')
print "Opened database successfully";

conn.execute('''create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);''')
print "Table created successfully";

conn.close()
