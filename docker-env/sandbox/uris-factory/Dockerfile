FROM openjdk:11

# Copy start script
ADD https://bintray.com/herculescrue/backend-sgi/download_file?file_path=es%2Fum%2Fasio%2Furis-generator-1.0.0.jar /opt/app/app.jar
ADD ./start-script /usr/local
RUN chmod a+x /usr/local/start-container.sh
RUN apt-get update && apt-get install -y

ENV JAVA_OPTS="-Xmx512M"

CMD /usr/local/start-container.sh

#COPY app-no.jar /opt/app/app-no.jar
