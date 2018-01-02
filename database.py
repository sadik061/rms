from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'demo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id,email,password,role FROM login''')
    rv = cur.fetchall()
    cur.close()
    return (rv)



def register(email,password,role):
    cur = mysql.connection.cursor()	
    cur.execute('''INSERT INTO login(email,passw0rd,role) VALUES(%s,%s,%s)''',(email,password,role))
    mysql.connection.commit()
    cur.close()


def lastrohingaFamily():
     cur = mysql.connection.cursor()
     cur.execute('''SELECT family_id FROM family ORDER BY family_id DESC LIMIT 1''')
     rv = cur.fetchone()
     cur.close()
     return (rv)


def lastrohinga():
     cur = mysql.connection.cursor()
     cur.execute('''SELECT rohinga_id FROM rohinga ORDER BY rohinga_id DESC LIMIT 1''')
     rv = cur.fetchone()
     cur.close()
     return (rv)

def schoolinfo():
     cur = mysql.connection.cursor()
     cur.execute('''SELECT * FROM school''')
     rv = cur.fetchall()
     cur.close()
     return (rv)


def healthevent():
     cur = mysql.connection.cursor()
     cur.execute('''SELECT * FROM events where sector="Health" And checked="1"''')
     rv = cur.fetchall()
     cur.close()
     return (rv)

def pendingevents():
     cur = mysql.connection.cursor()
     cur.execute('''SELECT * FROM events where checked="0"''')
     rv = cur.fetchall()
     cur.close()
     return (rv)


def housingg():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM camps''')
    rv = cur.fetchall()
    cur.close()
    return (rv)


def foods(x):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT SUM(amount) as %s FROM aid where type=%s""",(x,x))
    rv = cur.fetchall()
    print(rv)
    return (rv)


def needfoods(x):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM family''')
    rv = cur.fetchall()
    total=0
    for i in rv:
        total += int(x)*int(i['member_count'])
    print(total)
    return (total)


def itemRecords():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM items""")
    rv = cur.fetchall()
    return (rv)


if __name__ == '__main__':
    app.run(debug=True)
