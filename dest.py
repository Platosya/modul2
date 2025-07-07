import sqlite3
connection = sqlite3.connect('db.db')
cursor = connection.cursor()
cursor.execute('SELECT * from post')
post = cursor.fetchall()
print(post)
# cursor.execute('''INSERT into post(title,content) values
#   ('arbuz', 'ya lublu arbuzi'),
#   ('mandarinka','ya lubly mandarinki')''')
# connection.commit()
connection.close()