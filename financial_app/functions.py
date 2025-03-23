def get_quiz_data():
    # Sample data for quizzes
    return [
        {'question': 'What is the best way to save money?', 'options': ['Invest in stocks', 'Put it in a savings account', 'Buy cryptocurrency']},
        {'question': 'What should you avoid when using a credit card?', 'options': ['Paying the full balance', 'Carrying a high balance', 'Paying on time']}
    ]

def calculate_score(form_data):
    # Placeholder score calculation logic
    correct_answers = ['Put it in a savings account', 'Carrying a high balance']
    score = 0
    for i, answer in enumerate(form_data.values()):
        if answer == correct_answers[i]:
            score += 1
    return score
