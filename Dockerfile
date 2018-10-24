FROM hub.arctron.cn/base/alpine-glibc

COPY . .

RUN apk add --no-cache --virtual bdep libffi-dev openssl-dev python3-dev g++ \
    && pip3 install -r ./requirement.txt \
    && apk del bdep \
    && apk add --no-cache python3
