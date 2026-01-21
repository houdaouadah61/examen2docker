import os
import sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"data","database.db")
def init_db():
    data_dir = os.path.join(BASE_DIR,"data")
    os.makedirs(data_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
@app.route("/")
def index():
    return "API OK"
#CREATE 
@app.route("/users",methods=["POST"])
def create_user():
    data=request.get_json()
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
                   (data["username"],data["password"]))
    conn.commit()
    conn.close()
    return jsonify({"message":"user created succ"}),201
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@app.route("/users/<int:user_id> ", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ? ",
        (data["username"], data["password"], user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message ":"user updated"}), 200
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,)
                   )
    conn.commit()
    conn.close()

    return jsonify({"message": "user deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
