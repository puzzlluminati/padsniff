FROM python:3.6-alpine

ADD requirements.txt .
RUN apk add --no-cache --virtual runtime-deps \
        libffi   \
        libstdc++ \
        openssl    \
    && apk add --no-cache --virtual build-deps \
        g++       \
        libffi-dev \
        openssl-dev \
    && LDFLAGS=-L/lib pip install -r requirements.txt \
    && rm -f requirements.txt \
    && apk del build-deps

WORKDIR /var/padsniff
COPY . .
RUN pip install -e .

EXPOSE 8080
ENTRYPOINT ["padsniff"]
CMD ["--help"]
