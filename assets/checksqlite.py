import os
import sqlite3
import csv

def sqlite_to_csv(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.sqlite'):
            db_path = os.path.join(directory, filename)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table_name in tables:
                table_name = table_name[0]
                table = cursor.execute(f"SELECT * from {table_name}").fetchall()

                with open(f"{table_name}.csv", 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(table)

            conn.close()

# Replace 'your_directory' with the path to the directory containing your SQLite databases
sqlite_to_csv('C:\\temp')