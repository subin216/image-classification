# Image Classification with Tensorflow
The overall goal of the project is image classification with Tensorflow (Inception-v3 model was used). If a user uploads an image file through the web page, the image file will be sent to the Inception-v3 model through the Spring server. Then, the Spring server will return the result from the python module to let the user know what the Inception-v3 model thinks the picture looks like.

### Languages
I used JavaScript, Java and Python.
* Java was used for implementing the web server with the SpringBoot framework.
* Python was used for Tensorflow for the calculation to classify the given image.
* JavaScript was used for implementing the frontend web page which gets the image file from the user as input

### Methods used to communicate between languages
* Between JavaScript and Java, communication is done through REST API.
* Between Java and Python, communication is done with ProcessBuilder API from Java. ProcessBuilder API allows the Java program to execute the Python program and receive results such as print statements on the streambuffer.

### How to run the project
Since I uploaded the .jar file, you just need to type "docker-compose build && docker-compose up" on the terminal.
Then, please wait. it takes around ~5 minutes. (Sorry, Tensorflow library is so big)
And, if you see "Started WebApplication in … seconds (JVM running for ...)" message or “Creating web ... done Attaching to web web    | WARNING: no logs are available with the 'syslog' log driver (Csil gave me this message)” on the terminal, please open the web page and go to "http://localhost:8080/" Then you'll see the web page for the project there. I also uploaded some test image files and they are in the "test-image-files" folder. You can test my project with them by uploading and checking the results. Doing the calculations on the image can take several seconds, so, please be patient. I also uploaded an image for how the website should look in the /demo-image folder just for reference.