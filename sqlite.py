# This is to create a sqlite database and publish values to it. ( also install sqlite browser to verify )
import sqlite3

# Simply run as python sqlite.py, and you will see a .db file created. Open it up with sqlite browser to verify
 
# These are dummy values. In a real application, you would ask the subscriber to provide these details ( name, mobile, email ) and store in the database through the app.py file. In that case only specify the schema here

with sqlite3.connect("myfirstdb.db") as connection:# connection object
  connection.execute('CREATE TABLE subscriber(mobile text, otp text, name text, email text)')
  connection.execute("""INSERT INTO subscriber VALUES("9999999999","9999","Keshvica","kesh@gmail.com")""")
  connection.execute("""INSERT INTO subscriber VALUES("8888888888","1111","Golu","Golu@gmail.com")""")
  connection.execute("""INSERT INTO subscriber VALUES("7777777777","2222","dev","dev@gmail.com")""")
  connection.execute("""INSERT INTO subscriber VALUES("6666666666","3333","hemant","hemant@gmail.com")""")


with sqlite3.connect("myfirstdb.db") as connection:# connection object
  connection.execute('CREATE TABLE posts(name text, email text)')
  connection.execute("""INSERT INTO posts VALUES("Keshvica","Awsome blog")""")
  connection.execute("""INSERT INTO posts VALUES("Golu","Great :)")""")
  connection.execute("""INSERT INTO posts VALUES("dev","Congrats!!!")""")
  connection.execute("""INSERT INTO posts VALUES("hemant","Going great")""")
