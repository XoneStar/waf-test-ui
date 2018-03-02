import sys
from string import Template

temp = Template("""
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       naxsi_core.rules;
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            include  naxsi.rules; #引用子规则
            proxy_pass  $url;
        }
	
	    #配置拦截后拒绝访问时展示的页面
	    location /RequestDenied { 
            return 403;
        }
    }

}""")


def get_conf():
    result = ''
    with open('/etc/nginx/nginx.conf', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            if 'proxy_pass' in line:
                result = line
                break
            line = f.readline()
    return result.split(" ")[-1].replace(';', '')


def update_conf(url):
    # print(temp.substitute(url=url))
    with open('/etc/nginx/nginx.conf', 'w', encoding='utf-8') as f:
        f.write(temp.substitute(url=url))


def add_rule2file(naxsi_core, naxsi):
    with open('/etc/nginx/naxsi_core.rules', 'w', encoding='utf-8') as f0:
        with open(sys.path[0] + '/conf/naxsi_temp.rules', 'r', encoding='utf-8') as f1:
            f0.write(f1.read() + '\n' + naxsi_core)

    with open('/etc/nginx/naxsi.rules', 'w', encoding='utf-8') as f2:
        with open(sys.path[0] + '/conf/naxsi_tmp.rules', 'r', encoding='utf-8') as f3:
            f2.write(f3.read() + '\n' + naxsi)


if __name__ == '__main__':
    # update_conf('http://192.168.199.224/')
    print(get_conf())
