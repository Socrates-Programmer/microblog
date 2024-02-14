from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods = ["GET", "POST"])
    def home():
        if request.method == "POST":

            entry_content = request.form.get("content")
            name_user = request.form.get("name")

            if not entry_content or not name_user:
                Error = "Unos de los dos formularios tiene esta vacio."
                return render_template("home.html", error=Error)

            fotmatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            app.db.entries.insert_one( {
                "content": entry_content,
                "date": fotmatted_date,
                "name": name_user
                } )
            
        entries_with_date = [ 
            (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b-%d"),
            entry["name"],
            )
            
            for entry in app.db.entries.find({})
            ]            


        return render_template("home.html", entries=entries_with_date)
    
    return app