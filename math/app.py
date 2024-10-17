from flask import Flask, render_template, request, session, redirect, url_for, jsonify
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
        answer = (num1) - (num2)
    elif operation == 'multiply':
        question = f"{num1} * {num2}"
        answer = num1 * num2
    elif operation == 'divide':
        num1 = num1 * num2  # Ensure division is exact
        question = f"{num1} / {num2}"
        answer = num1 // num2

    answer = str(answer)
    return question, answer

@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
    difficulty = request.args.get('difficulty', 'easy')
    session['question'], session['correct_answer'] = generate_question(difficulty)
    return render_template('index.html', question=session['question'], score=session['score'], difficulty=difficulty)

@app.route('/quiz')
def math():
    if 'score' not in session:
        session['score'] = 0
        
    # Generate the question and answer on the first visit to this route
    difficulty = request.args.get('difficulty', 'easy')
    session['question'], session['correct_answer'] = generate_question(difficulty)
    
    return render_template('quiz.html', question=session['question'], score=session['score'], difficulty=difficulty)

@app.route('/math_videos')
def math_videos():
    return render_template('math_videos.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Receive JSON data from the client (AJAX)
    data = request.get_json()
    user_answer = data.get('answer')
    correct_answer = session.get('correct_answer')
    difficulty = data.get('difficulty')

    result = {"correct": False, "message": "", "score": session['score'], "correct_answer": correct_answer, "question": session['question']}

    # Check if the user's answer is a valid digit and if a correct answer exists
    if user_answer and correct_answer is not None:
        user_answer = str(user_answer)
        correct_answer = str(correct_answer)
        # result["message"] = f"correct_answer: {correct_answer}"
        if user_answer == correct_answer:
            session['score'] += 1
            result["correct"] = True
            result["message"] = "Correct! Your score increased by 1."
        else:
            result["message"] = f"Incorrect. The correct answer was {type(correct_answer)}."
    
    # Generate a new question after submission
    session['question'], session['correct_answer'] = generate_question(difficulty)

    # Add the new question to the result
    result["question"] = session['question']

    # Return the result in JSON format
    return jsonify(result)

xyz = "hola"

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
    # Reset the score to 0
    session['score'] = 0
    # Generate a new question after resetting the score
    difficulty = request.args.get('difficulty', 'easy')  # Get the difficulty from the session or default
    session['question'], session['correct_answer'] = generate_question(difficulty)
    return redirect(url_for('math'))

if __name__ == '__main__':
    app.run(debug=True)
