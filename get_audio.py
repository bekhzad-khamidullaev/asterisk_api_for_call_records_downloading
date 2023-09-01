from flask import Flask, request, send_file
from flask_httpauth import HTTPBasicAuth
import os
from urllib.parse import quote, unquote

app = Flask(__name__)
auth = HTTPBasicAuth()

# Sample user credentials (replace with your own)
users = {
    "username": "password"
}

# Sample token (replace with your own)
valid_tokens = {
    "G1gd4ueLR9yolqUwAmWhLcqdxOc0Z24Mecezk3vvKckadJkjHu38FtiXVoQzbqKu": "username"  ############ you can generate your own token)
}

audio_dir = "/var/spool/asterisk/monitor/"  # Update this to your audio files directory

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username

@auth.login_required
@app.route('/download', methods=['GET'])
def download_route():
    url_path = request.args.get('url')
    token = request.args.get('token')

    if token in valid_tokens:  # Checking if token is a valid key
        url_path = unquote(url_path)  # Decode URL-encoded path
        return download_file(url_path)
    else:
        return "Unauthorized token", 401

def download_file(url_path):
    year, month, day, filename = extract_parameters(url_path)

    file_path = os.path.join(audio_dir, year, month, day, filename)  # Construct the full file path

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

def extract_parameters(url_path):
    # Assuming the format is /var/spool/asterisk/monitor/YYYY/MM/DD/filename.mp3
    parts = url_path.split('/')
    year, month, day, filename = parts[-4], parts[-3], parts[-2], parts[-1]
    return year, month, day, filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)