from flask import Flask
from flask_socketio import SocketIO, send
import ffmpeg
import io

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Streaming Service"

# WebSocket handler for receiving media chunks
@socketio.on('message')
def handle_media(data):
    # Process the incoming data and write it to a file
    # You can use a pipe to FFmpeg or store data in a temporary file for further processing
    try:
        input_stream = io.BytesIO(data)
        process_stream(input_stream)
    except Exception as e:
        print(f"Error handling stream: {e}")

def process_stream(input_stream):
    # FFmpeg processing to convert received media data into an MP4 file
    # For simplicity, this is just a basic setup - you may want to handle frame and audio syncing
    try:
        ffmpeg.input('pipe:0').output('output.mp4').run(input=input_stream)
        print("File saved as output.mp4")
    except Exception as e:
        print(f"FFmpeg error: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001, debug=True)
