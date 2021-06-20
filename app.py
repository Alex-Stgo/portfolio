from flask import Flask, render_template, request
import datetime as dt
import numpy as np
# from pymongo import MongoClient
# from dotenv import load_dotenv
import os
import labyrinth as lb

# load_dotenv()

def create_app():
    app=Flask(__name__)
    # client = MongoClient(os.environ.get("MONGODB_URI"))
    # app.db = client.microblog

    # @app.route("/", methods=["GET","POST"])
    @app.route("/")
    def home():
        # print([e for e in app.db.entries.find({})])
        # if request.method=="POST":
        #     entry_content=request.form.get("content")
        #     fdate=dt.datetime.today().strftime("%Y-%m-%d")
        #     app.db.entries.insert({"content": entry_content, "date" : fdate})
        # entries=[(entry["content"],entry["date"]) for entry in app.db.entries.find({})]
        return render_template("index.html")

    @app.route("/projects/swap_calculator/")
    def p_swap():
        return render_template("swap_calculator.html")

    @app.route("/projects/forecasting_report/")
    def p_forecasting():
        return render_template("forecasting.html")
    
    @app.route("/projects/labyrinth_solver/",methods=["GET","POST"])
    def p_labyrinth():
        
        if request.method=="POST":
            letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
            labyrinth= lb.labyrinth(0.75,0.9)
            x = int(request.form.get("start_field"))
            y = int(request.form.get("end_field"))
            text = " -> ".join(labyrinth.get_route(0,x,y))
            start = letters[x]
            end = letters[y]
        else:
            text=""
            start=""
            end=""
        return render_template("Labyrinth.html", start=start,end=end,route=text)
    return app
