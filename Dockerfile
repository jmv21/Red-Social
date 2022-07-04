FROM python:3.7-slim

#RUN Step
RUN pip install grpcio
RUN pip install protobuf
RUN pip install netaddr
RUN pip install apsw==3.38.5.post1
RUN pip install cryptocode==0.1
RUN pip install getmac==0.8.3
RUN pip install peewee==3.15.0
RUN pip install pycryptodome==3.15.0
RUN pip install pycryptodomex==3.15.0
COPY . /sn
WORKDIR /sn
#RUN pip install -r requirements.txt
#RUN apt-get update && apt-get -y upgrade



#Adding files.
#ADD chord_node.py /root/chord_node.py
#ADD utils.py /root/utils.py
#ADD client.py /root/client.py
#ADD client.py /root/storage_node.py


EXPOSE 8080
EXPOSE 8081
EXPOSE 8082


#Default running
ENTRYPOINT ["python", "/sn/run_app_client.py"] 
