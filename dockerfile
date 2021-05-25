FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV TOKEN=<token>
COPY . .

CMD [ "python","-u", "./run.py" ]