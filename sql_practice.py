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
cursor.execute("""
               CREATE TABLE IF NOT EXISTS payments (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   resident_id INTEGER,
                   amount INTEGER,
                   payment_date TEXT,
                   FOREIGN KEY (resident_id) REFERENCES residents(id)
               )
               """)

payments_data = [
    (1,5000,"2025-01-15"),
    (1,7000,"2025-02-10"),
    (2,10000,"2025-01-20"),
    (3,15000,"2025-03-05"),
    (4,8000,"2025-02-14"),
    (2,6000,"2025-03-18"),
]

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
cursor.execute("DELETE FROM payments")
conn.commit()

cursor.executemany("INSERT INTO residents (name, age, district, income) VALUES (?,?,?,?)", residents_data)
cursor.executemany("INSERT INTO payments (resident_id, amount, payment_date) VALUES (?,?,?)", payments_data)
conn.commit()

cursor.execute("""
               SELECT * 
               FROM residents
               """)
rows = cursor.fetchall()

for row in rows:
    print(row)

### Over 30 years 
# cursor.execute("SELECT name, age FROM residents WHERE age > 30")
# print(cursor.fetchall())

### Average income
# cursor.execute("SELECT AVG(income) FROM residents")
# print(cursor.fetchall())

### AVG income in districts
# cursor.execute("""
#                SELECT district, AVG(income) 
#                FROM residents 
#                GROUP BY district
#                """)
# print(cursor.fetchall())

### Best district by income
# cursor.execute("""
#                SELECT district, AVG(income) as avg_income
#                FROM residents
#                GROUP BY district
#                ORDER BY avg_income DESC LIMIT 1
#                """)
# print(cursor.fetchall())

### Ищем кол-во жителей в районе
# cursor.execute("""
#                SELECT district, COUNT(*) as count
#                FROM residents
#                GROUP BY district
#                ORDER BY count DESC
#                """)
# print(cursor.fetchall())

### Средний доход выше 70000
# cursor.execute("""
#                SELECT district, AVG(income) as avg_income
#                FROM residents
#                GROUP BY district
#                HAVING avg_income > 70000
#                """)
# print(cursor.fetchall())

### человек и сумма его платежей
# cursor.execute("""
#                SELECT r.name, p.amount
#                FROM residents r
#                JOIN payments p ON r.id = p.resident_id
#             """)
# print(cursor.fetchall())

### общая сумма платежей
# cursor.execute("""
#                SELECT r.name, SUM(p.amount) as total_paid
#                FROM residents r
#                JOIN payments p ON r.id=p.resident_id
#                GROUP BY r.name
#                ORDER BY total_paid DESC
#                """)
# print(cursor.fetchall())

### Анализ по месяцам
# cursor.execute("""
#                SELECT 
#                     substr(payment_date,1,7) as month,
#                     SUM(amount) as total_amount
#                FROM payments
#                GROUP BY month
#                ORDER BY month
#                """)
# print(cursor.fetchall())

### Самый прибыльный месяц
# cursor.execute("""
#                SELECT 
#                     substr(payment_date,1,7) as month,
#                     SUM(amount) as total_amount
#                FROM payments
#                GROUP BY month
#                ORDER BY total_amount DESC
#                LIMIT 1
#                """)
# print(cursor.fetchall())

### Сложение дохода
cursor.execute("""
               SELECT 
                    r.district,
                    SUM(p.amount) as total_payments
               FROM residents r
               JOIN payments p ON r.id = p.resident_id
               GROUP BY r.district
               ORDER BY total_payments DESC
               """)
print(cursor.fetchall())

### Кто платил больше всех за все время 
# cursor.execute("""
#                SELECT r.name, SUM(p.amount) as total_paid
#                FROM residents r
#                JOIN payments p ON r.id = p.resident_id
#                GROUP BY r.name
#                ORDER BY total_paid DESC
#                LIMIT 1
#                """)
# print(cursor.fetchall())

### Кто платил больше среднего 
# cursor.execute("""
#                SELECT r.name, SUM(p.amount) as total_paid
#                FROM residents r
#                JOIN payments p ON r.id = p.resident_id
#                GROUP BY r.name
#                HAVING SUM(p.amount) > (
#                    SELECT AVG(total_paid)
#                    FROM (
#                        SELECT SUM(amount) as total_paid
#                        FROM payments
#                        GROUP BY resident_id
#                    )
#                )
#                """)
# print(cursor.fetchall())

### кто больше раз платил
# cursor.execute("""
#                SELECT r.name, COUNT(*) as count
#                FROM residents r
#                JOIN payments p ON r.id = p.resident_id
#                GROUP BY r.name
#                ORDER BY count DESC
#                LIMIT 1
#                """)
# print(cursor.fetchall())

### Район с большим числом жителей и платежами выше среднего
cursor.execute("""
               SELECT r.district, SUM(p.amount) as total_payments
               FROM residents r
               JOIN payments p ON r.id = p.resident_id
               GROUP BY r.district
               HAVING SUM(p.amount) > 20000
               """)
print(cursor.fetchall())

conn.close()