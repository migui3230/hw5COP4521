import sqlite3

# setup database
conn = sqlite3.connect('hospital_user.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE HospitalUser
          (id INTEGER PRIMARY KEY,
          name TEXT,
          age INTEGER,
          phone_number TEXT,
          has_covid BOOLEAN,
          security_role_level INTEGER,
          login_password TEXT)
          ''')

conn.commit()
conn.close()
