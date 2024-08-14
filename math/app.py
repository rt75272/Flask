from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def generate_question(difficulty):
    difficulty_levels = {
        'easy': (1, 10),
        'medium': (10, 100),
        'hard': (100, 1000)
    }
    num_range = difficulty_levels.get(difficulty, (1, 10))
    num1 = random.randint(*num_range)
    num2 = random.randint(*num_range)

    operations = ['add', 'subtract', 'multiply', 'divide']
    operation = random.choice(operations)

    if operation == 'add':
        question = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == 'subtract':
        question = f"{num1} - {num2}"
        answer = num1 - num2
    elif operation == 'multiply':
        question = f"{num1} * {num2}"
        answer = num1 * num2
    elif operation == 'divide':
        # Ensure division is exact and no division by zero
        num1 = num1 * num2  # To ensure the division is exact
        question = f"{num1} / {num2}"
        answer = num1 // num2

    return question, answer

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'score' not in session:
        session['score'] = 0
    if request.method == 'POST':
        try:
            user_answer = int(request.form['answer'])
            correct_answer = session.get('correct_answer', None)
            difficulty = request.form['difficulty']
            
            if correct_answer is not None:
                if user_answer == correct_answer:
                    session['score'] += 1
                    result = "Correct! Your score increased by 1."
                else:
                    # session['score'] -= 1
                    result = f"Incorrect. The correct answer was {correct_answer}."
            else:
                result = "Error: Correct answer not found."

            # Generate a new question for the next round
            session['question'], session['correct_answer'] = generate_question(difficulty)

        except ValueError:
            result = "Invalid input. Please enter a valid number."

        return render_template('index.html', result=result, difficulty=difficulty, score=session['score'], question=session['question'])

    # Initialize a new question if not available
    if 'question' not in session or request.method == 'GET':
        difficulty = request.args.get('difficulty', 'easy')
        session['question'], session['correct_answer'] = generate_question(difficulty)

    return render_template('index.html', result="Answer the question below to get started", question=session['question'], score=session['score'], difficulty=request.args.get('difficulty', 'easy'))

@app.route('/reset_score')
def reset_score():
    session['score'] = 0
    session.pop('question', None)
    session.pop('correct_answer', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
