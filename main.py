from flask import Flask,render_template,url_for,request,flash,redirect
import os
import sqlite3 as sq
import parser
import Database

app=Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"]="djsenrbbrvrjsiskssnbeehrhejsn" 
@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/account/")
def account():
    return render_template("account.html")

@app.route("/account/create/",methods=["POST","GET"])
def account_create():
    secret_phrase=parser.phrase()
    adress=parser.address()
    if request.method=="POST":
       Database.create_account(adress,secret_phrase,request.form["password"])
       a=Database.authorization_account(secret_phrase,request.form["password"])[0]

       return redirect("/account/authorization/")
    return render_template("account_create.html",secret_phrase=secret_phrase,adress=adress)

@app.route("/account/authorization/",methods=["POST","GET"])
def account_authorization():
    if request.method=="POST":
        if Database.authorization_account(request.form["secret"],request.form["password"]):
            a=Database.authorization_account(request.form["secret"],request.form["password"])[0]
            return render_template("account_entrance.html",adress=a[1],balance=a[4],secret=a[2],transactions=Database.transactions_select(a[1]))
        else:
             return "Неправильно,потробуйте ещё раз"
    return render_template("account_authorization.html")
    
       
       
       
@app.route("/account/send/<secret>",methods=["POST","GET"])
def account_secret(secret):
    if request.method=="POST":
        
        Database.send_account(request.form["adress"],secret+" ",request.form["sum"])
        
        return Database.send_account(request.form["adress"],secret+" ",request.form["sum"])
        
    
    return  render_template("account_send.html")

@app.route("/blockchain/",methods=["POST","GET"])
def blockchain():
    return render_template("blockchain.html",transactions=Database.blockchain())

@app.route("/promocode/create/<secret>",methods=["POST","GET"])
def promocode_create(secret):
    if request.method=="POST":
     a=Database.select_account(secret+" ")[0]
     Database.create_promo_cod(request.form["author"],request.form["sum"],request.form["users"],a[1])
     return render_template("success.html")
    

    return render_template("promocode_create.html")




@app.route("/promocode/activate/<secret>",methods=["POST","GET"])
def promocode_activate(secret):
    if request.method=="POST":
        
        return Database.activate_promo_cod(secret+" ",request.form["cod"])
        
    return render_template("promocode_activate.html")
    
@app.route("/chest/<secret>",methods=["POST","GET"])
def chest(secret):
    if request.method=="POST":
        a=Database.check(int(request.form["sum"]))
        Database.transfer(secret+" ",a)
        return f"Вы выиграли:"+str(a)
        

    t=Database.select_account(secret+" ")[0]
    return render_template("chest.html", balance=t[4])
    


@app.route("/support_center/",methods=["POST","GET"])
def support_center():
    return render_template("support_center.html")
    





@app.route("/news/",methods=["POST","GET"])
def news():
    return render_template("Доллар_подешевел.html")
    


if __name__=="__main__":
    app.run(debug=True)