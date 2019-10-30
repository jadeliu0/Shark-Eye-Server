shark eye server which runs predictions for the shark-eye model.

TO RUN:
1. create a new directory named `shark_eye`

2. download the code and model weights here: https://drive.google.com/open?id=1jpAMQo7mY6SBjDiIoYo0D0jzszZRbvFJ
   and build the image with `sudo nvidia-docker build ./`

3. run the image and cd to `root/shark_detection` and download the repository for the server from here: https://github.com/jadeliu0/Shark-Eye-Server

4. cd Shark-Eye-Server

5. start the server by run: `python app.py`

