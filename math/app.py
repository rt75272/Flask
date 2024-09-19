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
        num1 = num1 * num2  # Ensure division is exact
        question = f"{num1} / {num2}"
        answer = num1 // num2

    return question, answer

@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
    difficulty = request.args.get('difficulty', 'easy')
    session['question'], session['correct_answer'] = generate_question(difficulty)
    return render_template('index.html', question=session['question'], score=session['score'], difficulty=difficulty)

@app.route('/math')
def math():
    if 'score' not in session:
        session['score'] = 0
        
    # Generate the question and answer on the first visit to this route
    difficulty = request.args.get('difficulty', 'easy')
    session['question'], session['correct_answer'] = generate_question(difficulty)
    
    return render_template('math.html', question=session['question'], score=session['score'], difficulty=difficulty)



@app.route('/submit', methods=['POST'])
def submit():
    user_answer = request.form['answer']
    correct_answer = session.get('correct_answer', None)
    difficulty = request.form['difficulty']
    result = ""

    if user_answer.isdigit() and correct_answer is not None:
        user_answer = int(user_answer)
        if user_answer == correct_answer:
            session['score'] += 1
            result = "Correct! Your score increased by 1."
        else:
            result = f"Incorrect. The correct answer was {correct_answer}."
    else:
        result = "Invalid input. Please enter a valid number."

    session['question'], session['correct_answer'] = generate_question(difficulty)
    return render_template('index.html', result=result, question=session['question'], score=session['score'], difficulty=difficulty)

# @app.route('/math_resources')
# def math_resources():
#     return render_template('math_resources.html')

@app.route('/science_resources')
def science_resources():
    return render_template('science_resources.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reset_score')
def reset_score():
    session['score'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
