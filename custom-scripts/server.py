#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import BaseHTTPServer
import os
import cpustat


HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>T1 Lab. Sis. Op.</title></head>")

	#Data e hora do sistema;
	datahora = os.popen('date').read()
        s.wfile.write("<body><p> Data e hora do sistema: %s.</p>" % datahora)

	#uptime (tempo de funcionamento sem reinicialização do sistema) em segundos
	uptimeSecs = os.popen('awk \'{print $1}\' /proc/uptime').read() + " segundos"
	s.wfile.write("<body><p> Uptime em segundos: %s.</p>" % uptimeSecs)

	# Modelo do processador e velocidade; MUDEEEEI
	model = os.popen('cat /proc/cpuinfo | grep -m 1 "model name"').read().replace("model name", "")
	s.wfile.write("<body><p> Modelo do processador%s.</p>" % model)
	vel = os.popen('cat /proc/cpuinfo | grep -m 1 "cpu MHz"').read().replace("cpu MHz", "") + "MHz"
	s.wfile.write("<body><p> Velocidade do processador %s.</p>" % vel )

	# Capacidade ocupada do processador (%);
	s.wfile.write("<p>Capacidade ocupada das cpus em percent: %s</p>" % cpustat.GetCpuLoad().getcpuload())

	# Quantidade de memória RAM total e usada (MB); MUDEEEEI
	ramTotal = os.popen('free -m | awk \'NR==2{print $2}\' ').read() + "MB"
	s.wfile.write("<p>Quantidade de RAM total: %s</p>" % ramTotal)
	ramUsada = os.popen('free -m | awk \'NR==2{print $3}\' ').read() + "MB" 
	s.wfile.write("<p>Quantidade da RAM usada: %s</p>" % ramUsada)

	# Versão do sistema;
	sistema = os.popen('cat /etc/os-release |grep "VERSION" | awk \'NR==1{print $0}\'').read().replace("VERSION=","")
	s.wfile.write("<p>Versao do sistema:: %s</p>" % sistema)
	
	# Lista de processos em execução (pid e nome). MUDEEEEEI
	procs = os.popen('ps -o pid -o comm').read()
	s.wfile.write("<p>Processos em execucao %s</p>" % procs)

        s.wfile.write("</body></html>")

if __name__ == '__main__':
    print("Servidor iniciado")
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (" Servidor fechado")
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

