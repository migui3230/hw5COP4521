import sqlite3

# Connect to the database
conn = sqlite3.connect('hospital_user.db')

# Create a cursor
c = conn.cursor()

# Select all data from the database
c.execute("SELECT * FROM HospitalUser")

# Fetch all the data
data = c.fetchall()

# Print the data
print(data)

# Close the connection
conn.close()
