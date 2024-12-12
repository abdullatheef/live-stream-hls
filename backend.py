import socket
from flask import Flask, request, send_from_directory
import math
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# UDP Socket to send data to GStreamer on port 5002
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX_UDP_SIZE = 8000

@app.route('/playlist.m3u8')
def stream_playlist():
    return send_from_directory('/tmp', 'playlist.m3u8')

@app.route('/<filename>')
def stream_segment(filename):
    if filename.endswith('.ts'):
        return send_from_directory('/tmp', filename)
    else:
        return "Invalid file format", 400

@app.route('/upload', methods=['POST'])
def upload_video():
    chunk = request.files['chunk'].read()

    # Ensure you're sending a format GStreamer can decode (e.g., raw H264 or MP4)
    num_chunks = math.ceil(len(chunk) / MAX_UDP_SIZE)
    for i in range(num_chunks):
        print(f"Sending chunk {i + 1}/{num_chunks}")
        start = i * MAX_UDP_SIZE
        end = start + MAX_UDP_SIZE
        udp_socket.sendto(chunk[start:end], ('127.0.0.1', 5002))

    return {"status": "received"}

@app.route('/stream')
def stream_video():
    # Placeholder for stream initiation
    return "Streaming started."

if __name__ == '__main__':
    # Make sure the /tmp directory is accessible and writable
    if not os.path.exists('/tmp'):
        os.makedirs('/tmp')
    
    app.run(host='0.0.0.0', port=5001, debug=True)
