rom database import get_connection

class Student:
    def __init__(self, username):
        self.username = username

    def take_exam(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()

        score = 0
        for q in questions:
            print(f"\nQ{q[0]}. {q[1]}")
            print(f"A) {q[2]}  B) {q[3]}  C) {q[4]}  D) {q[5]}")
            ans = input("Enter your answer (A/B/C/D): ").upper()
            if ans == q[6]:
                score += 1

        print(f"\n✅ Exam Completed! Your score: {score}/{len(questions)}")
        cursor.execute("INSERT INTO results (username, score) VALUES (?, ?)", (self.username, score))
        conn.commit()
        conn.close()
