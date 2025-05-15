from flask import Flask
from routes import main
import logging
import os
from logging.handlers import RotatingFileHandler

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(debug=True)