FROM python:3.8-alpine

# change timezone
RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

WORKDIR /usr/src/app
COPY src ./
COPY requirements.txt ./
RUN  pip install -r requirements.txt

CMD ["python", "main.py"]