import config
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd=config.password,
                     db="gttravel")

cur = db.cursor()

cur.execute("INSERT INTO users(Username, Email, Password, Is_manager) VALUES ('name','filler@gmail.com','password',FALSE)")

cur.execute("SELECT * FROM USERS")
for row in cur.fetchall():
    print row[0]

db.commit()

db.close()
