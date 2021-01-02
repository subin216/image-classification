# For SpringBoot
# Start with a base image containing Java runtime
FROM openjdk:11-jre

# Add Author information
LABEL maintainer="subinb@sfu.ca"

# Make port 8080 available
EXPOSE 8080

# The application's jar file
ADD web web/
RUN chmod -R 777 /web
ARG JAR_FILE=/web/web-0.0.1-SNAPSHOT.jar

# Add the application's jar to the container
ADD ${JAR_FILE} cmpt383-project.jar

# Add the directory for tensorflow
ADD tensor tensor/
RUN chmod -R 777 /tensor

# Run the jar file
ENTRYPOINT ["java","-jar","/cmpt383-project.jar"]

# For Python
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip

# For Tensorflow (takes long time)
RUN pip3 install tensorflow