import datetime
import json
import logging
import os
import subprocess

import flask
from flask import Response, send_from_directory

app = flask.Flask(__name__)
app.config["INFO"] = True
logging.getLogger().setLevel(logging.INFO)


def read_file_and_check_status():
    f = open('servers.txt')
    servers = f.readlines()
    server_status_list = list()
    for server in servers:
        server_status_list.append(check_single_server(server))
    return {"servers": server_status_list}


def check_single_server(ip):
    ip = ip.replace('\n', '')
    logging.info("Check status for server %s" % ip)
    result = subprocess.run(["ping", "-c", "1", ip])
    status_ip = "OK" if result.returncode == 0 else "ERROR"
    logging.info("Server status for ip %s" % status_ip)
    now = datetime.datetime.now()
    return {"ip": ip, "status": status_ip, "last_update": now.strftime("%Y-%m-%d %H:%M:%S")}


@app.route('/status', methods=['GET'])
def status_servers():
    response = Response(json.dumps(read_file_and_check_status()),
                        status=200,
                        mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def root():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir,'pimon'), 'index.html')


if __name__ == '__main__':
    app.run(port=5002, host='0.0.0.0')
