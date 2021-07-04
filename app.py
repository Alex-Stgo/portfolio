from flask import Flask, render_template, request
import datetime as dt
import numpy as np
import os
import labyrinth as lb
import swaps as sw
from difflib import get_close_matches as gcm,SequenceMatcher as sm
import book_store
# load_dotenv()

def create_app():
    app=Flask(__name__)
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/projects/swap_calculator/",methods=["GET","POST"])
    def p_swap():
        data={}
        if request.method == "POST":
            data['notional1'] = int(request.form.get("notional1"))
            data['periods1'] = int(request.form.get("periods1"))
            data['notional2'] = int(request.form.get("notional2"))
            data['periods2'] = int(request.form.get("periods2"))
            data['rate2'] = float(request.form.get("rate2"))
            leg1 = sw.leg.VariableMXN(data['notional1'],data['periods1'])
            leg2 = sw.leg.FixedMXN(data['notional2'],data['periods2'],data['rate2']/100)
            swap = sw.swap(leg1,leg2)
            data['calculated'] = True
            data['l1']=leg1.flows
            data['l2']=leg2.flows
            data['spread']=round(swap.spread()*10000,2)
        else:
            data['calculated'] = False
        return render_template("swap_calculator.html",data=data)

    @app.route("/projects/forecasting_report/")
    def p_forecasting():
        return render_template("forecasting.html")

    @app.route("/projects/end_of_month/")
    def p_endofmonth():
        return render_template("endofmonth.html")
    
    @app.route("/projects/web_map/")
    def p_webmap():
        return render_template("webmap.html")

    @app.route("/projects/map/")
    def p_map():
        return render_template("map1.html")
    
    @app.route("/projects/labyrinth_solver/",methods=["GET","POST"])
    def p_labyrinth():
        
        if request.method=="POST":
            letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
            labyrinth= lb.labyrinth(0.75,0.9)
            x = int(request.form.get("start_field"))
            y = int(request.form.get("end_field"))
            result=True
            text = " -> ".join(labyrinth.get_route(0,x,y))
            start = letters[x]
            end = letters[y]
            sn=x
            dn=y
        else:
            text=""
            start=""
            end=""
            result=False
            sn=0
            dn=0
        return render_template("Labyrinth.html", start=start,end=end,route=text,result=result,sn=sn,dn=dn)
    
    @app.route("/projects/book-scrape/",methods=["GET","POST"])
    def p_book_page():
        data={}
        if request.method=="POST":
            if request.form.get("title") == None:
                bsi = book_store.webscrap()
                data["c1"]=True
                data['categories'] = bsi.categories
            else:
                data["c1"]=True
                data["c2"]=True
                data['category'] = request.form.get("category")
                print(data['category'])
                data['title'] = request.form.get("title")
                data['numres'] = int(request.form.get("numres"))
                data['cutoff'] = float(request.form.get("cutoff"))

                bsi = book_store.webscrap()
                data['categories'] = bsi.categories
                all_books = bsi.books_by_cat(data['category'])
                books = gcm(data['title'],all_books,n=data['numres'],cutoff=data['cutoff'])
                selected={k:v for k,v in all_books.items() if k in books}
                data['results'] = {}
                for book in selected.keys():
                    data['results'][book] = bsi.book_info(book)
                    data['results'][book]['Score'] = "{:.2%}".format(sm(None, data['title'],book).ratio())
        else:
            data['c1'] = False
            data['c2'] = False
        return render_template("books_scrap.html",data=data)
    

    return app