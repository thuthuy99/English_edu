#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, session, logging,redirect,flash
 
from connectDatabase import connection
app = Flask(__name__)

@app.route('/home')
def trangchu():
    linkDangnhap = url_for("dangnhap")
    return render_template("trangchu.html", linkDangnhap = linkDangnhap)

@app.route('/home/dangnhap')
def dangnhap():
    return render_template("dangnhap.html") 

@app.route('/home/dangnhap/dangki',methods=["GET","POST"])
def dangki():
    if request.method == "POST":
        name_id = request.form.get("name_id")
        username = request.form.get("username")
        phone = request.form.get("phone")
        password_id = request.form.get("password_id")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password_id))

        if password_id == confirm:
            db.execute("INSERT INTO users(name_id, username, phone, password_id) VALUES (:name_id,:username,:phone,:password_id)",
                                         {"name_id":name_id,"username":username,"phone":phone,"password_id":secure_password})
            db.commit()
            return redirect(url_for("dangnhap"))
        else:
            flash("password does not match","danger")
            return render_template("dangki.html")
    return render_template("dangki.html")    

@app.route('/home/study')
def hoctap():
    linktrangchu = url_for("trangchu")
    cursor = connection().cursor()
    query = "SELECT id, ten, mo_ta from doc1"
    cursor.execute(query)
    results = cursor.fetchall()
    reading = []
    for result in results:
        jsonData = {
            "linkRead": url_for("doc", baidoc = result[1]),
            "id": result[0],
            "ten": result[1],
            "mo_ta": result[2]
        }
        reading.append(jsonData)
    cursor = connection().cursor()
    query = "SELECT id, ten, mo_ta from nghe1"
    cursor.execute(query)
    results = cursor.fetchall()
    listening = []
    for result in results:
        jsonData = {
            "linkListen": url_for("nghe", bainghe = result[1]),
            "id": result[0],
            "ten": result[1],
            "mo_ta": result[2]
        }
        listening.append(jsonData)
    connection().close()
    return render_template("tranghoc.html", linktrangchu = linktrangchu, reading = reading, listening = listening)

@app.route('/home/read/<baidoc>')
def doc(baidoc):
    cursor = connection().cursor()
    query = "select * from doc1 where ten = %s"
    cursor.execute(query,(baidoc,))
    results = cursor.fetchall()
    content =[]
    for result in results:
        jsonData = {
            "id": result[0],
            "ten": result[1],
            "linkBT": result[2],
            "linkDA": result[3],            
            "doanvan": result[4],
            "mo_ta": result[5],
            "image": result[6]
        }
        content.append(jsonData)
    connection().close()
    return render_template("doc1.html",content = content)

@app.route('/home/listen/<bainghe>')
def nghe(bainghe):
    cursor = connection().cursor()
    query = "select * from nghe1 where ten = %s"
    cursor.execute(query,(bainghe,))
    results = cursor.fetchall()
    content =[]
    for result in results:
        jsonData = {
            "id": result[0],
            "ten": result[1],
            "doanvan": result[2],
            "audio": result[3],
            "linkBT": result[4],
            "linkDA": result[5],
            "mo_ta": result[6],
            "image": result[7]
        }
        content.append(jsonData)
    connection().close()
    return render_template("nghe1.html",content = content)
  
if __name__ == "__main__":
    app.run(debug=True)
    