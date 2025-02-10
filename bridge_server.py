from flask import Flask, request, Response
import socket
import os
import sys

# Add the path to log.py if it's not in the same directory
sys.path.append(os.path.join(os.path.expanduser("~"), "Documents", "CTI-CRM-Bridge"))

from log import log_message

app = Flask(__name__)

# Amdocs Connection Port
HOST = "127.0.0.1"
PORT = 1024

# Timeout 
TIMEOUT = 10

# Send Information to Socket Server
def send_to_socket_server(message):
    """Send a message to the socket server."""
    s = None
    try:
        s = socket.create_connection((HOST, PORT), timeout=TIMEOUT)
        log_message("Connection established with socket server.")
        s.sendall(message.encode('utf-8'))
        log_message(f"Message sent to socket server: {message}")
    finally:
        if s:
            s.close()
            log_message("Socket connection closed.")

# Receive Information from Incoming Server
@app.route('/incoming-call')
def incoming_call():
    call_data = request.args.get('data', '')
    log_message(f"Received call data: {call_data}")

    # Split the parameters
    params = call_data.split(",")
    if len(params) >= 6:
        call_id, ctid, phone_number, reason1, reason2, call_type = params[:6]
        log_message(f"Parsed parameters: {call_id}, {ctid}, {phone_number}, {reason1}, {reason2}, {call_type}")

        # Validate call ID and phone number
        if not call_id:
            log_message("Invalid query format: Call ID is required")
            return "Invalid query format: Call ID is required", 400

    else:
        log_message("Invalid query format")
        return "Invalid query format", 400

    # Send data to the socket server
    send_to_socket_server(call_data)
    log_message(f"Call processed successfully: {call_id}, {ctid}, {phone_number}, {reason1}, {reason2}, {call_type}")
    return f"✅ Call processed: {call_id}, {ctid}, {phone_number}, {reason1}, {reason2}, {call_type}"

# Remove false replies
@app.route('/favicon.ico')
def favicon():
    # Return a 204 No Content response for favicon requests
    return Response(status=204)

# Runtime
if __name__ == '__main__':
    # Start the Flask server
    app.run(host='localhost', port=28888)
