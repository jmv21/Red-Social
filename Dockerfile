FROM python:3.7-slim

#RUN Step
RUN pip install grpcio
RUN pip install protobuf
RUN pip install netaddr
COPY . /chord
WORKDIR /chord


#Adding files.
#ADD chord_node.py /root/chord_node.py
#ADD utils.py /root/utils.py
#ADD client.py /root/client.py
#ADD client.py /root/storage_node.py


EXPOSE 8080
EXPOSE 8081
EXPOSE 8082


#Default running
ENTRYPOINT ["python", "/chord/client.py"] 
