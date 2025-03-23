import openai
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from groq import Groq
import matplotlib.pyplot as plt
import random
from datetime import datetime
from functions import *
import secrets 

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # Required for flash messages
groq_client = Groq(api_key="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")

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS savings_goals 
                 (id INTEGER PRIMARY KEY, goal_name TEXT, target_amount REAL, saved_amount REAL, target_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Default route (home page)
@app.route('/')
def index():
    return render_template('home.html')

# Explicit home route
@app.route('/home')
def home():
    return render_template('home.html')

# Chat page route
@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    messages = [{"role": "user", "content": user_input}]
    response_text = send_to_groq(messages)
    return jsonify({'reply': response_text})

def send_to_groq(messages, model="llama3-8b-8192"):
    response = groq_client.chat.completions.create(messages=messages, model=model)
    return response.choices[0].message.content

@app.route('/lessons')
def lessons():
    return render_template('lessons.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/budgeting')
def budgeting():
    return render_template('budgeting.html')

@app.route('/progress')
def progress():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM savings_goals')
    goals = c.fetchall()
    conn.close()
    return render_template('progress.html', goals=goals)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        goal_name = request.form['goal_name']
        target_amount = float(request.form['target_amount'])
        saved_amount = float(request.form['saved_amount'])
        target_date = request.form['target_date']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO savings_goals (goal_name, target_amount, saved_amount, target_date) VALUES (?, ?, ?, ?)", 
                  (goal_name, target_amount, saved_amount, target_date))
        conn.commit()
        conn.close()
        
        flash('Savings goal added successfully!')
        return redirect(url_for('progress'))
    return render_template('goal.html')

def generate_progress_graph(target_amount, saved_amount, goal_name):
    if os.path.exists('static/progress.png'):
        os.remove('static/progress.png')

    fig, ax = plt.subplots()
    ax.barh(['Progress'], [saved_amount], color='green', label='Saved')
    ax.barh(['Progress'], [target_amount - saved_amount], left=[saved_amount], color='red', label='Remaining')

    ax.set_xlabel('Amount ($)')
    ax.set_title(f'{goal_name} Savings Progress')
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/progress.png')

@app.route('/progress/<int:goal_id>')
def generate_progress(goal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM savings_goals WHERE id=?', (goal_id,))
    goal = c.fetchone()
    conn.close()

    if goal:
        generate_progress_graph(goal[2], goal[3], goal[1])
        return redirect(url_for('progress'))
    else:
        flash('Goal not found!')
        return redirect(url_for('progress'))

@app.route('/tips/<int:goal_id>')
def tips(goal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM savings_goals WHERE id=?', (goal_id,))
    goal = c.fetchone()
    conn.close()

    if goal:
        tip = get_saving_tips(goal[1], goal[3], goal[2], goal[4])
        return render_template('tips.html', tip=tip, goal=goal)
    else:
        flash('Goal not found!')
        return redirect(url_for('progress'))

def get_saving_tips(goal_name, saved_amount, target_amount, target_date):
    tips = [
        "Consider cutting back on entertainment expenses to save faster.",
        "You might reach your goal quicker by setting aside an extra $20 each week.",
        "Review your monthly subscriptions to see if you can cancel any.",
        "Try meal prepping to reduce food expenses and save more!"
    ]
    return random.choice(tips)

if __name__ == '__main__':
    app.run(debug=True)