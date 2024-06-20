// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video_feed');

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (error) {
                console.error('Error accessing the webcam:', error);
            });
    }
});
