# Monitoring Webapp with SMS Alerts

This webapp receives alerts from Prometheus/Alertmanager and forwards them as SMS messages using Twilio.

## Setup

1. Sign up for a Twilio account at https://www.twilio.com/try-twilio
2. Get your Twilio credentials:
   - Account SID
   - Auth Token
   - Twilio Phone Number

3. Create a `.env` file in the webapp directory with the following content:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
   ALERT_PHONE_NUMBER=recipient_phone_number_here
   ```

4. Replace the placeholder values with your actual Twilio credentials and the phone number where you want to receive alerts.

## Testing

1. Visit http://localhost:8080 to check if the webapp is running
2. The status page will show if SMS alerts are enabled
3. To test alerts, trigger one of the system alerts:
   - High CPU usage (>30% for 1 minute)
   - High memory usage (<80% free for 1 minute)
   - High disk usage (>50% for 1 minute)
   - High network traffic (>10MB/s for 1 minute)
   - High system load (>2 for 1 minute)

## Monitoring

The webapp exposes the following metrics:
- `sms_alerts_sent_total`: Total number of SMS alerts sent
- `http_requests_total`: Total HTTP requests
- `http_request_duration_seconds`: HTTP request latency
- `http_errors_total`: Total HTTP errors 