const ws = new WebSocket('ws://localhost:5000/socket.io/?EIO=3&transport=websocket');

ws.onopen = () => console.log('WebSocket connection established');
ws.onclose = () => console.log('WebSocket connection closed');
ws.onerror = (error) => console.error('WebSocket error:', error);

ws.onmessage = (event) => {
    const img = new Image();
    img.src = URL.createObjectURL(event.data);
    img.onload = () => {
        processed.src = img.src;
    };
};

function sendFrame() {
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        ws.send(blob);
    }, 'image/jpeg');
}

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        webcam.srcObject = stream;
    })
    .catch(error => console.error('Error accessing media devices.', error));

setInterval(sendFrame, 1000); // Send a frame every second
