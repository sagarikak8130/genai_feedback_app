from flask import Blueprint, render_template, request, redirect, send_file
from feedback_utils import infer_intent_urgency_response,generate_response, assign_team, save_to_mongo, get_all_feedback
import pandas as pd
import logging

logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)

@main.route('/')
def home():
    logger.info('Accessing home page')
    return render_template('home.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    feedback = request.form['feedback']
    logger.info(f'Received feedback for analysis: {feedback[:100]}...')
    
    result = infer_intent_urgency_response(feedback)
    intent = result['intent']
    urgency = result['urgency']
    logger.info(f'Analyzed feedback - Intent: {intent}, Urgency: {urgency}')
    
    team = assign_team(intent)
    response = generate_response(intent)
    logger.info(f'Assigned to team: {team}')
    
    save_to_mongo(feedback, intent, response, urgency, team)
    logger.info('Feedback saved to database')

    return render_template('result.html', response=response)

@main.route('/history')
def history():
    logger.info('Accessing feedback history')
    all_feedback = get_all_feedback()
    return render_template('history.html', feedback_list=all_feedback)

@main.route('/download')
def download():
    logger.info('Downloading feedback data as CSV')
    data = get_all_feedback()
    df = pd.DataFrame(data)
    df.drop(columns=['_id'], inplace=True)
    df.to_csv('feedback_log.csv', index=False)
    logger.info('CSV file generated successfully')
    return send_file('feedback_log.csv', as_attachment=True)
