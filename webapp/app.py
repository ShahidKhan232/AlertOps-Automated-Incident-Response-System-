from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
import time
import random
from collections import deque
from datetime import datetime
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP errors', ['method', 'endpoint', 'error_type'])
SMS_ALERTS_SENT = Counter('sms_alerts_sent_total', 'Total SMS alerts sent')

# Store alerts in memory (last 100 alerts)
alerts = deque(maxlen=100)

# Initialize Twilio client
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
alert_phone_number = os.getenv('ALERT_PHONE_NUMBER')

twilio_client = None
if twilio_account_sid and twilio_auth_token and twilio_phone_number and alert_phone_number:
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
    app.logger.info(f"Twilio client initialized with account SID: {twilio_account_sid[:5]}...")
else:
    app.logger.warning("Twilio client not initialized. Missing environment variables.")

def send_sms_alert(alert_data):
    """Send SMS alert using Twilio"""
    if not twilio_client:
        app.logger.warning("Twilio client not initialized. Check your environment variables.")
        return False
    
    try:
        # Format the alert message
        alert_name = alert_data.get('labels', {}).get('alertname', 'Unknown Alert')
        severity = alert_data.get('labels', {}).get('severity', 'unknown')
        summary = alert_data.get('annotations', {}).get('summary', 'No summary available')
        description = alert_data.get('annotations', {}).get('description', 'No description available')
        
        message = f"ALERT: {alert_name} ({severity})\n{summary}\n{description}"
        
        # Send the SMS
        twilio_client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=alert_phone_number
        )
        
        # Increment the counter
        SMS_ALERTS_SENT.inc()
        app.logger.info(f"SMS alert sent for {alert_name}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to send SMS alert: {str(e)}")
        return False

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.endpoint
    ).observe(time.time() - request.start_time)
    
    return response

@app.route('/')
def home():
    # Get the latest alert if any
    latest_alert = alerts[-1] if alerts else None
    
    # Simulate random errors for testing
    if random.random() < 0.1:  # 10% chance of error
        ERROR_COUNT.labels(
            method='GET',
            endpoint='home',
            error_type='random_error'
        ).inc()
        return jsonify({'error': 'Random error occurred'}), 500
    
    return jsonify({
        'status': 'healthy',
        'latest_alert': latest_alert,
        'sms_alerts_enabled': twilio_client is not None,
        'twilio_config': {
            'account_sid': twilio_account_sid[:5] + '...' if twilio_account_sid else None,
            'phone_number': twilio_phone_number,
            'alert_phone': alert_phone_number
        }
    })

@app.route('/alerts', methods=['POST'])
def receive_alert():
    alert_data = request.json
    # Add timestamp to alert
    alert_data['received_at'] = datetime.now().isoformat()
    alerts.append(alert_data)
    
    # Send SMS alert
    send_sms_alert(alert_data)
    
    return jsonify({'status': 'success', 'message': 'Alert received'})

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(list(alerts))

@app.route('/test-sms', methods=['GET'])
def test_sms():
    """Test endpoint to manually trigger an SMS alert"""
    test_alert = {
        'labels': {
            'alertname': 'TestAlert',
            'severity': 'info'
        },
        'annotations': {
            'summary': 'Test SMS Alert',
            'description': 'This is a test SMS alert sent from the monitoring system.'
        }
    }
    
    success = send_sms_alert(test_alert)
    
    return jsonify({
        'status': 'success' if success else 'failed',
        'message': 'Test SMS alert sent' if success else 'Failed to send test SMS alert',
        'alert': test_alert
    })

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 