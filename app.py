from flask import Flask, render_template, request, redirect, flash

import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# إنشاء قاعدة البيانات أو الاتصال بها
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# إنشاء جدول المستخدمين إذا لم يكن موجودًا
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL
)
""")

# تأكيد التغييرات
conn.commit()

# غلق الاتصال بقاعدة البيانات
conn.close()
# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("home.html")

# عرض المستخدمين
@app.route("/users")
def users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users_data)

# نموذج إضافة مستخدم
@app.route("/form")
def form():
    return render_template("form.html")

# إضافة مستخدم إلى قاعدة البيانات
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    age = request.form["age"]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
        conn.commit()
        conn.close()

        flash("تم تسجيل المستخدم بنجاح!", "success")
        return redirect("/users")
    except sqlite3.IntegrityError:
        flash("البريد الإلكتروني مسجل بالفعل!", "danger")
        return redirect("/form")

# تعديل بيانات المستخدم
@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        cursor.execute("UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?", (name, email, age, user_id))
        conn.commit()
        conn.close()
        flash("تم تحديث بيانات المستخدم بنجاح!", "success")
        return redirect("/users")

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        flash("المستخدم غير موجود", "danger")
        return redirect("/users")
    return render_template("edit_user.html", user=user)

# حذف المستخدم
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("تم حذف المستخدم بنجاح!", "success")
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)
