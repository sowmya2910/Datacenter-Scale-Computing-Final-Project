# Green Taxi Application

All the requirements have been written taking Ubuntu 16.04 as the OS

### Prerequisites
1. Python 3.6
2. Mongo DB

Follow the steps underlined below:

1. Clone the github repository
2. cd into the repository using ```cd final-project-gopal-kapur-muruganandan-ramakrishnan/```


### Virtual Environment setup
1. Install virtualenv by:

    ```python3 -m venv venv/```
2. Activate the virtual environment by:

    ```source venv/bin/activate```

### Installing Dependencies
Run ```pip install -r requirements.txt``` to install dependencies


### Running migrations

1. Download [dump-tar-file](https://drive.google.com/open?id=14YPQHzoQtpeIhkaCW0bDw_4fpAn40aLC) 
2. Extract tar file using command:
```tar -xvzf dump.tar.gz```
3. Dump the database in mongo db:
```mongorestore dump/```
4. Apply migrations:
    1. App migrations ```python manage.py migrate uber```
    2. Kafka-Logpipe migrations ```python manage.py migrate logpipe```

### Kafka Setup
Follow the [guide](https://hevodata.com/blog/how-to-install-kafka-on-ubuntu/) to install kafka on your system.

### Running Django Server
Run ```python manage.py runserver```

### Running Kafka Consumer <TO BE MODIFIED>
Run using ```python manage.py run_kafka_consumer``` to set up Kafka consumer
