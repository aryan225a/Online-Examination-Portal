from database import get_connection

class Admin:
    def __init__(self, username):
        self.username = username

    def add_question(self):
        conn = get_connection()
        cursor = conn.cursor()

        question = input("Enter Question: ")
        options = [input(f"Option {opt}: ") for opt in ['A','B','C','D']]
        correct = input("Enter correct option (A/B/C/D): ").upper()

        cursor.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (question, *options, correct))

        conn.commit()
        conn.close()
        print("✅ Question added successfully.")

    def view_questions(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        rows = cursor.fetchall()

        for r in rows:
            print(f"\nQ{r[0]}. {r[1]}")
            print(f"A) {r[2]}  B) {r[3]}  C) {r[4]}  D) {r[5]}")
            print(f"Correct: {r[6]}")
        conn.close()
