import openai
from pymongo import MongoClient
from config import OPENAI_API_KEY, MONGO_URI, DB_NAME, COLLECTION_NAME
import logging

logger = logging.getLogger(__name__)

openai.api_key = OPENAI_API_KEY

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def infer_intent_urgency_response(feedback_text):
    logger.info('Inferring intent and urgency from feedback')
    prompt = f"""
    You are an AI assistant. Given the customer message below, identify:
    1. The intent (Complaint, Suggestion, Routine Inquiry)
    2. The urgency (High, Medium, Low)

    Message: "{feedback_text}"
    Respond in JSON like:
    {{
      "intent": "...",
      "urgency": "..."
    }}
    """

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        result = eval(completion.choices[0].message['content'])
        logger.info(f'Successfully analyzed feedback - Intent: {result["intent"]}, Urgency: {result["urgency"]}')
        return result
    except Exception as e:
        logger.error(f'Error analyzing feedback: {str(e)}')
        raise

def assign_team(intent):
    logger.info(f'Assigning team for intent: {intent}')
    if intent == "Complaint":
        return "Customer Support"
    elif intent == "Suggestion":
        return "Product Management"
    else:
        return "General Support"

def generate_response(intent):
    logger.info(f'Generating response for intent: {intent}')
    if intent == "Complaint":
        return "I apologize for the inconvenience. Let me look into this for you."
    elif intent == "Suggestion":
        return "Thank you for your suggestion. We will consider it."
    else:
        return "Thank you for your message. We will get back to you as soon as possible."

def save_to_mongo(feedback, intent, response, urgency, team):
    logger.info('Saving feedback to MongoDB')
    try:
        entry = {
            "feedback": feedback,
            "intent": intent,
            "urgency": urgency,
            "response": response,
            "assigned_team": team
        }
        collection.insert_one(entry)
        logger.info('Successfully saved feedback to MongoDB')
    except Exception as e:
        logger.error(f'Error saving to MongoDB: {str(e)}')
        raise

def get_all_feedback():
    logger.info('Retrieving all feedback from MongoDB')
    try:
        feedback_list = list(collection.find())
        logger.info(f'Successfully retrieved {len(feedback_list)} feedback entries')
        return feedback_list
    except Exception as e:
        logger.error(f'Error retrieving feedback from MongoDB: {str(e)}')
        raise
