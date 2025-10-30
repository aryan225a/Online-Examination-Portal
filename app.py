from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import init_db, get_connection

app = Flask(__name__)
app.secret_key = "exam_secret_key"
init_db()

@app.route("/")
def home():
    if "username" in session:
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            flash("Registration successful!", "success")
        except:
            flash("Username already exists!", "danger")
        finally:
            conn.close()
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["username"] = username
        session["role"] = user[0]
        if user[0] == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))
    else:
        flash("Invalid credentials!", "danger")
        return redirect(url_for("home"))

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("home"))
    return render_template("admin_dashboard.html")

@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    if request.method == "POST":
        q = request.form["question"]
        a = request.form["option_a"]
        b = request.form["option_b"]
        c = request.form["option_c"]
        d = request.form["option_d"]
        correct = request.form["correct_option"].upper()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (q, a, b, c, d, correct))
        conn.commit()
        conn.close()
        flash("Question added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_question.html")

@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("home"))
    return render_template("student_dashboard.html")

@app.route("/exam", methods=["GET", "POST"])
def exam():
    if session.get("role") != "student":
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(str(q[0]))
            if selected == q[6]
                score += 1

        cursor.execute("INSERT INTO results (username, score) VALUES (?, ?)", (session["username"], score))
        conn.commit()
        conn.close()
        return render_template("result.html", score=score, total=len(questions))

    conn.close()
    return render_template("exam.html", questions=questions)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
