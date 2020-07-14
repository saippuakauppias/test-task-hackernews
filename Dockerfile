FROM python:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN pip install -e .

CMD sleep 3 && hackernews init && hackernews parse && hackernews serve --port 80 --host 0.0.0.0
