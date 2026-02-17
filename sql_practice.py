import sqlite3

conn = sqlite3.connect("city.db")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                district TEXT,
                income INTEGER
               )
               """)

residents_data = [
    ("Alex", 25, "Leninsky", 60000),
    ("Maria", 40, "Sormovsky", 85000),
    ("Ivan",34,"Avtozavodsky",72000),
    ("Olga",29,"Leninsky",65000),
    ("Sergey",50,"Sormovsky",90000),
    ("Anna",22,"Prioksky",50000)
]

cursor.execute("DELETE FROM residents")
conn.commit()

cursor.executemany("INSERT INTO residents (name, age, district, income) VALUES (?,?,?,?)", residents_data)
conn.commit()

cursor.execute("SELECT * FROM residents")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Over 30 yers 
cursor.execute("SELECT name, age FROM residents WHERE age > 30")
print(cursor.fetchall())

# Average income
cursor.execute("SELECT AVG(income) FROM residents")
print(cursor.fetchall())

# AVG income in districts
cursor.execute("""
               SELECT district, AVG(income) 
               FROM residents 
               GROUP BY district
               """)
print(cursor.fetchall())

# Best district by income
cursor.execute("""
               SELECT district, AVG(income) as avg_income
               FROM residents
               GROUP BY district
               ORDER BY avg_income DESC LIMIT 1
               """)
print(cursor.fetchall())

# Ищем кол-во жителей в районе
cursor.execute("""
               SELECT district, COUNT(*) as count
               FROM residents
               GROUP BY district
               ORDER BY count DESC
               """)
print(cursor.fetchall())

# Средний доход выше 70000
cursor.execute("""
               SELECT district, AVG(income) as avg_income
               FROM residents
               GROUP BY district
               HAVING avg_income > 70000
               """)
print(cursor.fetchall())

conn.close()