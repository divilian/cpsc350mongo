
from flask import render_template, request, url_for, redirect
from cpsc350mongo import starwars
from pymongo import MongoClient, ASCENDING

@starwars.route("/")
def main():
    mconn = MongoClient("mongodb://localhost:27017")
    db = mconn['219']
    chars = db.starwars.find({}).sort([('name',ASCENDING)])
    if 'msg' in request.args:
        msg = request.args['msg']
    else:
        msg = ''
    return render_template("browse.html", chars=chars, msg=msg)

@starwars.route("/edit", methods=['GET','POST'])
def edit():
    mconn = MongoClient("mongodb://localhost:27017")
    db = mconn['219']
    if request.method == "GET":
        name = request.args['name'] 
        char = db.starwars.find({ 'name':name }, { '_id':0 }).next()
        filtered_char = {}
        for key, val in char.items():
            if type(val) in [ int, str ]:
                filtered_char[key] = val
        return render_template("edit.html", char=filtered_char)
    else:
        name = request.form['name'] 
        for key, val in request.form.items():
            db.starwars.update_one({ 'name':name }, { '$set': { key:val } })
        return redirect(url_for("main", msg=f"{name} updated successfully!"))
