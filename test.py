
#import config
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="gttravel")

cur = db.cursor()

cur.execute("SELECT * FROM USERS")
for row in cur.fetchall():
    print row[0]

db.close()