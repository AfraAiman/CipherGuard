from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__, template_folder='templates')
CORS(app)

WHOIS_API_KEY = "HF60BRU7QICPdS1cBV3qOg==FHLL6Zbcx014Ogz1"
IPINFO_TOKEN = "8c762131d946af"

def is_valid_ip(ip):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return re.match(pattern, ip) is not None

@app.route("/")
def index():
    return render_template("s.html")  # serve frontend

@app.route("/whois", methods=["POST"])
def whois_lookup():
    domain_or_ip = request.json.get("domain")
    if not domain_or_ip:
        return jsonify({"error": "No domain or IP provided"}), 400

    if is_valid_ip(domain_or_ip):
        try:
            response = requests.get(f"https://ipinfo.io/{domain_or_ip}/json?token={IPINFO_TOKEN}")
            return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        try:
            response = requests.get(
                f"https://api.api-ninjas.com/v1/whois?domain={domain_or_ip}",
                headers={"X-Api-Key": WHOIS_API_KEY}
            )
            return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
