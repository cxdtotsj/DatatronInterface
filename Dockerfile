FROM hub.arctron.cn/base/alpine-glibc

COPY ./requirements.txt .

RUN apk add --no-cache --virtual bdep libffi-dev openssl-dev python3-dev g++ \
    && pip3 install -r ./requirements.txt \
    && apk del bdep \
    && apk add --no-cache python3

COPY entrypoint.sh /entrypoint.sh

RUN apk add git openssh-client \
    && mkdir -p ~/.ssh \
    && ssh-keyscan gitlab.arctron.cn >> ~/.ssh/known_hosts \
    && chmod +x /entrypoint.sh

ENTRYPOINT /entrypoint.sh

