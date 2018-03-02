FROM creatorx/nginx-naxsi

MAINTAINER creatorx jxz <creatorx@163.com>

# update software
RUN apt-get update && \
apt-get upgrade -y

RUN apt-get install -y --no-install-recommends --no-install-suggests --fix-missing python3 python3-pip && \
pip3 install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple && \
apt-get update && \
apt-get autoremove -y && \
apt-get clean && \
apt-get autoclean && \
rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN virtualenv /env && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN export LANG=en_US.UTF-8

EXPOSE 80
EXPOSE 5000

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]

ENTRYPOINT ["/env/bin/python", "/app/main.py"]