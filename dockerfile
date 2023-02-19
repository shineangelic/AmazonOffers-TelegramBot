#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="shine.angelic"


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY paapi5-python-sdk ./
COPY amazon_api.py ./
COPY bot.py ./
COPY consts.py ./
COPY create_messages.py ./
COPY response_parser.py ./
# Now the structure looks like this '/usr/app/src/test.py'
COPY requirements.txt ./
RUN pip install -r requirements.txt
#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./bot.py"]