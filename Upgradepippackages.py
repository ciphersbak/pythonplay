import pip
from subprocess import call

proxies = {
    "http": "http://www-proxy-idc.in.oracle.com:80",
    "https": "https://www-proxy-idc.in.oracle.com:80",
}

for dist in pip.get_installed_distributions():
    #call("pip install --upgrade --proxy @www-proxy-idc.in.oracle.com:80" + dist.project_name, shell=True)
    call("pip install --proxy @www-proxy-idc.in.oracle.com:80 --upgrade " + dist.project_name, shell=True)