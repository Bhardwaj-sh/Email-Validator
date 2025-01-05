from flask import Flask, request, jsonify, render_template
import dns.resolver
from validate_email_address import validate_email
from disposable_email_domains import blocklist

app = Flask(__name__)

# Spam trap list (expand as needed)
SPAM_TRAP_LIST = [
    "trap@spamtrap.com",
    "fake@spamtrap.com",
    "test@trap.com"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_email_address():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Syntax Validation
    if not validate_email(email):
        return jsonify({"valid": False, "reason": "Invalid email format"}), 200

    # Domain Validation
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'A')  # Check if domain exists
    except dns.resolver.NXDOMAIN:
        return jsonify({"valid": False, "reason": "Invalid domain"}), 200

    # MX Record Validation
    try:
        dns.resolver.resolve(domain, 'MX')  # Check for MX records
    except Exception:
        return jsonify({"valid": False, "reason": "No MX records found"}), 200

    # Disposable Email Detection
    if domain in blocklist:
        return jsonify({"valid": False, "reason": "Disposable email address detected"}), 200

    # Spam Trap Detection
    if email.lower() in [trap.lower() for trap in SPAM_TRAP_LIST]:
        return jsonify({"valid": False, "reason": "Spam trap email detected"}), 200

    # Pattern Matching for Fake Emails
    username = email.split('@')[0]
    if len(username) > 30 or username.isdigit() or any(char in username for char in "!#$%^&*()"):
        return jsonify({"valid": False, "reason": "Potential fake email detected"}), 200

    return jsonify({"valid": True, "reason": "Email is valid"}), 200

if __name__ == '__main__':
    app.run(debug=True)