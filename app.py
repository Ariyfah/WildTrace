
import os
from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="wildtrace"
    )


@app.route("/", methods=["GET"])
def home():
    animals = []
    search = request.args.get("search", "").strip()

    if search:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM animals WHERE country LIKE %s",
            (f"%{search}%",)
        )

        animals = cursor.fetchall()

        cursor.close()
        db.close()

    return render_template(
        "index.html",
        animals=animals,
        search=search
    )


if __name__ == "__main__":
    app.run(debug=True)
