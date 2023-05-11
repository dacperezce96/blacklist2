FROM alpine:3.14

RUN apk add py3-pip
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app/

ENV TOKEN=token
ENV DATABASE_URL=postgresql://postgres:postgres@blacklist.cfk4eod950co.us-east-1.rds.amazonaws.com:5432/postgres
    
RUN pip install --ignore-installed -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]