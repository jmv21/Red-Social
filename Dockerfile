FROM python:3.7-slim

#RUN Step
RUN pip install zmq
COPY . /chord
WORKDIR /chord





EXPOSE 8080
EXPOSE 8081
EXPOSE 8082


#Default running
ENTRYPOINT ["python", "/chord/client.py"] 
