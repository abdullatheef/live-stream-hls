const WebSocket = require('ws');
const fs = require('fs');
const ffmpeg = require('fluent-ffmpeg');
const { Writable } = require('stream');

// Create WebSocket server
const wss = new WebSocket.Server({ port: 3000 });

wss.on('connection', (ws) => {
  console.log('Client connected');

  // Create a writable stream to pass data to FFmpeg
  const inputStream = new Writable({
    write(chunk, encoding, callback) {
      // Forward the data to FFmpeg for processing
      ffmpegProcess.write(chunk);
      callback();
    },
  });

  // Create an FFmpeg process to create the MP4 file
  const ffmpegProcess = ffmpeg()
    .input(inputStream)
    .inputFormat('webm')  // Adjust according to the format you're sending
    .audioCodec('aac')
    .videoCodec('libx264')
    .outputOptions([
      '-f mp4',
      '-y',
    ])
    .output('output.mp4')  // Output file name
    .on('start', () => {
      console.log('FFmpeg process started');
    })
    .on('end', () => {
      console.log('FFmpeg process ended');
    })
    .on('error', (err) => {
      console.log('FFmpeg error: ' + err.message);
    });

  // Start the FFmpeg process
  ffmpegProcess.run();

  // Handle incoming media data from the client
  ws.on('message', (data) => {
    console.log('Received media data');
    inputStream.write(data);  // Pipe the data into the FFmpeg process
  });

  ws.on('close', () => {
    console.log('Client disconnected');
    ffmpegProcess.end();
  });
});

console.log('WebSocket server listening on ws://localhost:3000');
