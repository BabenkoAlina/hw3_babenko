import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__, template_folder=".")

def create_tables():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS administrator (administrator_id INT PRIMARY KEY, admin_name VARCHAR(255))"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS location (location_id INT PRIMARY KEY, location_name VARCHAR(255), room_id INT, address VARCHAR(255), FOREIGN KEY (room_id) REFERENCES room(room_id))"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS lecture (lecture_id INT PRIMARY KEY, topic VARCHAR(255), date DATE)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS student (student_id INT PRIMARY KEY, student_name VARCHAR(255), average_mark DOUBLE)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS course (course_id INT PRIMARY KEY, location_id INT, FOREIGN KEY (location_id) REFERENCES location(location_id))"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS lecture_stats (lecture_id INT PRIMARY KEY, num_of_students INT, FOREIGN KEY (lecture_id) REFERENCES lecture(lecture_id))"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS room (room_id INT PRIMARY KEY, building VARCHAR(255), class INT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS teacher (teacher_id INT PRIMARY KEY, teacher_name VARCHAR(255), email VARCHAR(255), phone VARCHAR(255))"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS assistant (assistant_id INT PRIMARY KEY, assistant_name VARCHAR(255))"""
    )
    conn.commit()
    conn.close()

def save_data_to_database(data, table_name):
    conn = sqlite3.connect("hw2.db")
    cursor = conn.cursor()
    for item in data:
        cursor.execute(f"INSERT INTO {table_name} VALUES {item}")
    conn.commit()
    conn.close()

def get_data_from_table(table_name):
    conn = sqlite3.connect("hw2.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        administrator_id = request.form.get("administrator_id")
        admin_name = request.form.get("admin_name")
        save_data_to_database([(administrator_id, admin_name)], "administrator")
        return "Administrator data saved to database successfully!"

    return render_template("hw3.html")

@app.route("/retrieve", methods=["GET"])
def retrieve():
    table_name = request.args.get("table_name")
    data = get_data_from_table(table_name)
    if data:
        return f"Data from {table_name}: {data}"
    else:
        return "Table does not exist or no data found."

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)