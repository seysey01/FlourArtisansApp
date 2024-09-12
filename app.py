from flask import Flask, render_template, request, flash, url_for, redirect
from app.route import main

import sqlite3

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    return app



#app.config['SECRET_KEY'] = 'secret!'



if __name__ == "__main__" :
    app = create_app()
    app.run(debug=True)




#-----------------------------------------------------------------------------------------------------#
# create table - after connection..
# include validation too



# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template("index.html") #home.html or index.html or unique name
#
# @app.route('/add', methods=['POST'])
# def add():
#     return render_template("add.html")  #add.html"
#
# @app.route("/view")
# def view():
#     return render_template("view.html")
#
# @app.route("/success")
# def success():
#     return render_template("success.html")
#
# @app.route("/delete")
# def delete():
#     return render_template("delete.html")





# @app.route("/view")
# def view():
#     con = sqlite3.connect("food.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from Food")
#     rows = cur.fetchall()
#     con.close()
#     return render_template("view.html", rows=rows)


#@app.route("/savedetails", methods=["POST", "GET"])
# def save_details():
#     msg = "msg"
#     if request.method == "POST":
#         try:
#             demo_name = request.form["demo_name"]
#             presenters = request.form["presenters"]
#             imdb_team = request.form["imdb_team"]
#             summary = request.form["summary"]
#             demo_date = request.form["demo_date"]
#             time_in_minutes = request.form["time_in_minutes"]
#             broadcast_link = request.form["broadcast_link"]
#             additional_comment = request.form["additional_comment"]
#
#             with sqlite3.connect("people.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT into People (demo_name, presenters, imdb_team, summary, demo_date, time_in_minutes, "
#                             "broadcast_link, additional_comment) values (?,?,?,?,?,?,?,?)", (demo_name, presenters,
#                                                                                              imdb_team, summary, demo_date,
#                                                                                              time_in_minutes, broadcast_link,
#                                                                                              additional_comment))
#                 con.commit()
#                 msg = "Demo Successfully Added"
#         except:
#             con.rollback()
#             msg = "We cannot add the participant to the list"
#
#         finally:
#             return render_template("success.html", msg=msg)
#             con.close()


#
# @app.route("/update_record/<string:id>", methods=["POST", "GET"])
# def update_record(id):
#     con = sqlite3.connect("people.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from People where id=?", (id,))
#     rows = cur.fetchone()
#     con.close()
#
#     if request.method == 'POST':
#         try:
#             demo_name = request.form['demo_name']
#             presenters = request.form['presenters']
#             imdb_team = request.form['imdb_team']
#             summary = request.form['summary']
#             demo_date = request.form['demo_date']
#             time_in_minutes = request.form['time_in_minutes']
#             broadcast_link = request.form['broadcast_link']
#             additional_comment = request.form['additional_comment']
#             con = sqlite3.connect("people.db")
#             cur = con.cursor()
#             cur.execute("UPDATE People SET demo_name=?, presenters=?, imdb_team=?, summary=?, demo_date=?, "
#                         "time_in_minutes=?, broadcast_link=?, additional_comment=? WHERE id = ?", (demo_name, presenters,
#                                                                                                  imdb_team, summary,
#                                                                                                  demo_date,
#                                                                                                  time_in_minutes,
#                                                                                                  broadcast_link,
#                                                                                                  additional_comment, id))
#             con.commit()
#             flash("Updated Successfully", "success")
#         except:
#             flash("Error in Update Operation", "danger")
#         finally:
#             return redirect(url_for("index"))
#             con.close()
#
#     return render_template("update_record.html", rows=rows)
#
# @app.route("/delete")
# def delete():
#     return render_template("delete.html")
#
#
# @app.route("/delete_record", methods=["POST"])
# def delete_record():
#     id = request.form["id"]
#     with sqlite3.connect("people.db") as con:
#         try:
#             cur = con.cursor()
#             cur.execute("delete from People where id = ?", id)
#             msg = "record successfully deleted"
#         except:
#             msg = "can't be deleted"
#
#         finally:
#             return render_template("delete_record.html", msg=msg)
#