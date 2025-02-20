#!/usr/bin/env python3
import funct
import sql
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'), autoescape=True)
template = env.get_template('logs.html')
form = funct.form

if form.getvalue('grep') is None:
	grep = ""
else:
	grep = form.getvalue('grep')
	

exgrep = form.getvalue('exgrep') if form.getvalue('exgrep') else ''
	
if form.getvalue('rows') is None:
	rows = 10
else:
	if form.getvalue('rows1') is not None:
		rows = form.getvalue('rows1')
	else:
		rows = form.getvalue('rows')
	
hour = form.getvalue('hour')
hour1 = form.getvalue('hour1')
minut = form.getvalue('minut')
minut1 = form.getvalue('minut1')
waf = form.getvalue('waf')
service = form.getvalue('service')
	
print('Content-type: text/html\n')
funct.check_login()

try:
	user, user_id, role, token, servers, user_services = funct.get_users_params()
except Exception:
	pass

if service == 'nginx':
	if funct.check_login(service=2):
		title = "NGINX`s logs"
		servers = sql.get_dick_permit(nginx=1)
elif service == 'apache':
	if funct.check_login(service=4):
		title = "Apache's logs"
		servers = sql.get_dick_permit(apache=1)
elif waf == '1':
	if funct.check_login(service=1):
		title = "WAF logs"
		servers = sql.get_dick_permit(haproxy=1)
else:
	if funct.check_login(service=1):
		title = "HAProxy`s logs"
		servers = sql.get_dick_permit(haproxy=1)

template = template.render(h2=1,
							autorefresh=1,
							title=title,
							role=role,
							user=user,
							select_id="serv",
							selects=servers,
							serv=form.getvalue('serv'),
							rows=rows,
							grep=grep,
							exgrep=exgrep,
							hour=hour,
							hour1=hour1,
							minut=minut,
							minut1=minut1,
							waf=waf,
							service=service,
							user_services=user_services,
							token=token)
print(template)
