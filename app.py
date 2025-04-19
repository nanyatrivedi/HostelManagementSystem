from flask import Flask, render_template, request, redirect, url_for, session, flash
import cx_Oracle
from datetime import datetime

cx_Oracle.init_oracle_client(lib_dir="/Users/mananyatrivedi/Downloads/instantclient_23_3")

app = Flask(__name__)
app.secret_key = "your_secret_key_here" 

import os
conn = cx_Oracle.connect(
    os.environ.get("DB_USER"),
    os.environ.get("DB_PASS"),
    os.environ.get("DB_CONN")
)
cursor = conn.cursor()

@app.context_processor
def inject_now():
    return {'now': lambda: datetime.utcnow()}

def is_admin():
    return ("user" in session) and (session.get("role") == "admin")

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        cursor.execute("SELECT password, role FROM login_users WHERE username = :username", {"username": username})
        user = cursor.fetchone()

        if user is None:
            return render_template("login.html", error="No account found with that username.")

        stored_password = user[0] 
        role = user[1]

        if password != stored_password:
            return render_template("login.html", error="Incorrect password.")

        session["user"] = username
        session["role"] = role
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        reg_id = request.form.get("reg_id")
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template("register.html")

        cursor.execute("SELECT * FROM login_users WHERE username = :u", {"u": username})
        existing = cursor.fetchone()
        if existing:
            flash("Username already taken!", "danger")
            return render_template("register.html")

        try:
            cursor.execute("""
                INSERT INTO login_users (username, reg_id, password, role)
                VALUES (:un, :rid, :pw, :r)
            """, {"un": username, "rid": reg_id, "pw": password, "r": role})
            conn.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(str(e), "danger")
            return render_template("register.html")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session or "role" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    if session["role"] == "admin":
        try:
            cursor.execute("""
                SELECT s.admission_year,
                       s.contact,
                       s.dob,
                       s.email,
                       s.gender,
                       s.guardian_name,
                       s.guardian_phone,
                       s.hostel_block,
                       s.name,
                       s.registration_number,
                       s.room_id,
                       s.room_type,
                       m.meal_plan,
                       m.allergies,
                       m.mess_provider
                  FROM students s
                  LEFT JOIN mess m ON s.registration_number = m.reg_id
              ORDER BY s.registration_number
            """)
            all_students = cursor.fetchall()
        except Exception as e:
            flash(str(e), "danger")
            all_students = []

        try:
            cursor.execute("""
                SELECT fee_id, reg_id, status, amount, due_date, paid_on
                FROM fees
                WHERE status != 'Paid'
                ORDER BY due_date
            """)
            unpaid_fees = cursor.fetchall()
        except Exception as e:
            flash(str(e), "danger")
            unpaid_fees = []

        try:
            cursor.execute("""
                SELECT fee_id, reg_id, status, amount, due_date, paid_on
                FROM fees
                WHERE status = 'Paid'
                ORDER BY paid_on DESC
            """)
            paid_fees = cursor.fetchall()
        except Exception as e:
            flash(str(e), "danger")
            paid_fees = []

        try:
            cursor.execute("""
                SELECT complaint_id, reg_id, issue_type, description, status
                FROM complaints
                WHERE status != 'Resolved'
                ORDER BY complaint_date DESC
            """)
            open_complaints = cursor.fetchall()
        except Exception as e:
            flash(str(e), "danger")
            open_complaints = []

        return render_template(
            "dashboard_admin.html",
            user=session["user"],
            all_students=all_students,
            unpaid_fees=unpaid_fees,
            paid_fees=paid_fees,
            open_complaints=open_complaints
        )

    else:
        username = session["user"]

        cursor.execute("SELECT reg_id FROM login_users WHERE username = :u", {"u": username})
        row = cursor.fetchone()
        reg_id = row[0] if row else None

        cursor.execute("""
            SELECT admission_year, contact, dob, email, gender, guardian_name,
                   guardian_phone, hostel_block, name, registration_number,
                   room_id, room_type
            FROM students
            WHERE registration_number = :r
        """, {"r": reg_id})
        student_info = cursor.fetchone()

        cursor.execute("""
            SELECT meal_plan, allergies, mess_provider
            FROM mess
            WHERE reg_id = :r
        """, {"r": reg_id})
        mess_info = cursor.fetchone()

        cursor.execute("""
            SELECT status, amount, due_date, paid_on
            FROM fees
            WHERE reg_id = :r
        """, {"r": reg_id})
        fee_info = cursor.fetchone()

        cursor.execute("""
            SELECT issue_type, description, status
            FROM complaints
            WHERE reg_id = :r
            ORDER BY complaint_date DESC
        """, {"r": reg_id})
        complaints = cursor.fetchall()

        return render_template(
            "dashboard_student.html",
            user=username,
            reg=reg_id,
            student_info=student_info,
            mess_info=mess_info,
            fee_info=fee_info,
            complaints=complaints
        )

@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():
    if "user" in session:
        username = session["user"]
        issue_type = request.form["issue_type"]
        description = request.form["description"]

        cursor.execute("SELECT reg_id FROM login_users WHERE username = :u", {"u": username})
        r = cursor.fetchone()
        if r:
            reg_id = r[0]
            try:
                cursor.execute("""
                    INSERT INTO complaints (reg_id, complaint_date, issue_type, description, status)
                    VALUES (:reg_id, SYSDATE, :issue_type, :description, 'Pending')
                """, {
                    "reg_id": reg_id,
                    "issue_type": issue_type,
                    "description": description
                })
                conn.commit()
            except Exception as e:
                print("Error inserting complaint:", e)
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/mark_fee_paid", methods=["POST"])
def mark_fee_paid():
    if "user" in session and session["role"] == "admin":
        fee_id = request.form.get("fee_id")
        if fee_id:
            try:
                cursor.execute("""
                    UPDATE fees
                    SET status = 'Paid',
                        paid_on = SYSDATE
                    WHERE fee_id = :fid
                """, {"fid": fee_id})
                conn.commit()
            except Exception as e:
                print("Error marking fee as paid:", e)
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/update_complaint", methods=["POST"])
def update_complaint():
    if "user" in session and session["role"] == "admin":
        complaint_id = request.form.get("complaint_id")
        new_status = request.form.get("new_status")
        if complaint_id and new_status:
            try:
                cursor.execute("""
                    UPDATE complaints
                    SET status = :ns
                    WHERE complaint_id = :cid
                """, {"ns": new_status, "cid": complaint_id})
                conn.commit()
            except Exception as e:
                print("Error updating complaint:", e)
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/runquery", methods=["GET", "POST"])
def runquery():
    if "user" in session and session["role"] == "admin":
        query = ""
        result = None
        columns = []
        error = None

        if request.method == "POST":
            query = request.form.get("query", "").strip()
            try:
                if query.lower().startswith("select"):
                    cursor.execute(query)
                    columns = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                else:
                    error = "Only SELECT queries are allowed."
            except Exception as e:
                error = str(e)

        return render_template("runquery.html", query=query, result=result, columns=columns, error=error)

    return redirect(url_for("login"))

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template("reset_password.html", error="Passwords do not match.")

        cursor.execute("SELECT * FROM login_users WHERE username = :username", {"username": username})
        user = cursor.fetchone()

        if not user:
            return render_template("reset_password.html", error="Username not found.")

        cursor.execute("""
            UPDATE login_users SET password = :password WHERE username = :username
        """, {"password": new_password, "username": username})
        conn.commit()

        return redirect(url_for("login"))
    
    return render_template("reset_password.html")

@app.route("/admin/paid_fees")
def admin_paid_fees():
    if "user" in session and session["role"] == "admin":
        cursor.execute("""
            SELECT fee_id, reg_id, status, amount, due_date, paid_on
              FROM fees
             WHERE status = 'Paid'
          ORDER BY paid_on DESC
        """)
        paid_fees = cursor.fetchall()
        return render_template("paid_fees.html", paid_fees=paid_fees, user=session["user"])
    return redirect(url_for("login"))

@app.route("/admin/resolved_complaints")
def admin_resolved_complaints():
    if "user" in session and session["role"] == "admin":
        cursor.execute("""
            SELECT complaint_id, reg_id, issue_type, description, status
            FROM complaints
            WHERE status = 'Resolved'
            ORDER BY complaint_date DESC
        """)
        resolved_complaints = cursor.fetchall()
        return render_template("resolved_complaints.html", complaints=resolved_complaints, user=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=False)
