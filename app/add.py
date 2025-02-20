#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import funct
import sql
import http.cookies
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'), autoescape=True)
template = env.get_template('add.html')
form = funct.form
serv = form.getvalue('serv')

print('Content-type: text/html\n')
funct.check_login(service=1)
funct.page_for_admin(level=3)

if (
	form.getvalue('mode') is None and
	form.getvalue('new_userlist') is None and
	form.getvalue('peers-name') is None and
	form.getvalue('generateconfig') is None
):
	try:
		user, user_id, role, token, servers, user_services = funct.get_users_params(haproxy=1)
		cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
		group = cookie.get('group')
		user_group = group.value
	except Exception as e:
		print(str(e))

	dir = os.path.dirname(os.getcwd())+"/"+sql.get_setting('lists_path')
	white_dir = os.path.dirname(os.getcwd())+"/"+sql.get_setting('lists_path')+"/"+user_group+"/white"
	black_dir = os.path.dirname(os.getcwd())+"/"+sql.get_setting('lists_path')+"/"+user_group+"/black"

	if not os.path.exists(dir):
		os.makedirs(dir)
	if not os.path.exists(dir+"/"+user_group):
		os.makedirs(dir+"/"+user_group)
	if not os.path.exists(white_dir):
		os.makedirs(white_dir)
	if not os.path.exists(black_dir):
		os.makedirs(black_dir)

	white_lists = funct.get_files(dir=white_dir, format="lst")
	black_lists = funct.get_files(dir=black_dir, format="lst")

	template = template.render(title="Add: ",
								role=role,
								user=user,
								selects=servers,
								add=form.getvalue('add'),
								conf_add=form.getvalue('conf'),
								group=user_group,
								options=sql.select_options(),
								saved_servers=sql.select_saved_servers(),
								white_lists=white_lists,
								black_lists=black_lists,
							   	user_services=user_services,
								token=token)
	print(template)

elif form.getvalue('mode') is not None:
	haproxy_dir = sql.get_setting('haproxy_dir')
	port = form.getlist('port')
	bind = ""
	ip = ""
	force_close = form.getvalue('force_close')
	balance = ""
	mode = "    mode " + form.getvalue('mode') + "\n"
	maxconn = ""
	options_split = ""
	ssl = ""
	ssl_check = ""
	backend = ""
	acl = ""
	servers_split = ""
	new_listener = form.getvalue('listener')
	new_frontend = form.getvalue('frontend')
	new_backend = form.getvalue('new_backend')

	if form.getvalue('balance') is not None:
		balance = "    balance " + form.getvalue('balance') + "\n"

	if form.getvalue('health_check') is not None:
		health_check = form.getvalue('health_check')
		if health_check == 'option httpchk' and form.getvalue('checks_http_domain') is not None:
			health_check = health_check + ' GET ' + form.getvalue('checks_http_path') + ' "HTTP/1.0\\r\\nHost: ' + form.getvalue('checks_http_domain') + '"'
		balance += "    " + health_check + "\n"

	if form.getvalue('ip') is not None:
		ip = form.getlist('ip')

	if new_listener is not None:
		name = "listen " + new_listener
		end_name = new_listener
	elif new_frontend is not None:
		name = "frontend " + new_frontend
		end_name = new_frontend
	elif new_backend is not None:
		name = "backend " + new_backend
		end_name = new_backend
	else:
		print('error: The name cannot be empty')
		sys.exit()

	if form.getvalue('backends') is not None:
		backend = "    default_backend " + form.getvalue('backends') + "\n"

	if form.getvalue('maxconn'):
		maxconn = "    maxconn " + form.getvalue('maxconn') + "\n"

	if form.getvalue('ssl') == "https" and form.getvalue('mode') != "tcp":
		cert_path = sql.get_setting('cert_path')
		if form.getvalue('cert') is not None:
			ssl = "ssl crt " + cert_path + form.getvalue('cert')
		if form.getvalue('ssl-dis-check') is None:
			if form.getvalue('ssl-check') == "ssl-check":
				ssl_check = " ssl verify none"
			else:
				ssl_check = " ssl verify"

	if ip or port:
		if type(port) is list:
			i = 0
			for p in port:
				if ip[i] == 'IsEmptY':
					if ip[i] == 'IsEmptY' and port[i] == 'IsEmptY':
						i += 1
						continue
					else:
						port_value = port[i]
					bind += "    bind *:" + port_value + " " + ssl + "\n"
				else:
					if port[i] == 'IsEmptY':
						print('error: IP cannot be bind without a port')
						sys.exit()
					else:
						port_value = port[i]
					bind += "    bind " + ip[i] + ":" + port_value + " " + ssl + "\n"
				i += 1

	if form.getvalue('default-check') == "1":
		if form.getvalue('check-servers') == "1":
			check = " check inter " + form.getvalue('inter') + " rise " + form.getvalue('rise') + " fall " + form.getvalue('fall') + ssl_check
		else:
			check = ""
	else:
		if form.getvalue('check-servers') != "1":
			check = ""
		else:
			check = " check" + ssl_check

	if form.getvalue('option') is not None:
		options = form.getvalue('option')
		i = options.split("\n")
		for j in i:
			options_split += "    " + j + "\n"

	if force_close == "1":
		options_split += "    option http-server-close\n"
	elif force_close == "2":
		options_split += "    option forceclose\n"
	elif force_close == "3":
		options_split += "    option http-pretend-keepalive\n"

	if form.getvalue('whitelist') is not None:
		options_split += "    tcp-request connection accept if { src -f " + haproxy_dir + "/white/" + form.getvalue(
			'whitelist') + " }\n"

	if form.getvalue('blacklist') is not None:
		options_split += "    tcp-request connection reject if { src -f " + haproxy_dir + "/black/" + form.getvalue(
			'blacklist') + " }\n"

	if form.getvalue('cookie'):
		cookie = "    cookie "+form.getvalue('cookie_name')
		if form.getvalue('cookie_domain'):
			cookie += " domain "+form.getvalue('cookie_domain')
		if form.getvalue('rewrite'):
			rewrite = form.getvalue('rewrite')
		else:
			rewrite = ""
		if form.getvalue('prefix'):
			prefix = form.getvalue('prefix')
		else:
			prefix = ""
		if form.getvalue('nocache'):
			nocache = form.getvalue('nocache')
		else:
			nocache = ""
		if form.getvalue('postonly'):
			postonly = form.getvalue('postonly')
		else:
			postonly = ""
		if form.getvalue('dynamic'):
			dynamic = form.getvalue('dynamic')
		else:
			dynamic = ""
		cookie += " "+rewrite+" "+prefix+" "+nocache+" "+postonly+" "+dynamic+"\n"
		options_split += cookie
		if form.getvalue('dynamic'):
			options_split += "    dynamic-cookie-key " + form.getvalue('dynamic-cookie-key')+"\n"

	if form.getvalue('acl_if'):
		acl_if = form.getlist('acl_if')
		acl_value = form.getlist('acl_value')
		acl_then = form.getlist('acl_then')
		acl_then_values = form.getlist('acl_then_value')
		i = 0

		for a in acl_if:

			acl_then_value = '' if acl_then_values[i] == 'IsEmptY' else acl_then_values[i]

			try:
				if a == '1':
					acl_if_word = 'hdr_beg(host) -i '
					if form.getvalue('ssl') == "https" and form.getvalue('mode') != "tcp":
						acl_if_word = 'ssl_fc_sni -i '
					if form.getvalue('mode') == "tcp":
						acl_if_word = 'req.ssl_sni -i '
				elif a == '2':
					acl_if_word = 'hdr_end(host) -i '
					if form.getvalue('ssl') == "https" and form.getvalue('mode') != "tcp":
						acl_if_word = 'ssl_fc_sni -i '
					if form.getvalue('mode') == "tcp":
						acl_if_word = 'req.ssl_sni -i '
				elif a == '3':
					acl_if_word = 'path_beg -i '
				elif a == '4':
					acl_if_word = 'path_end -i '
				elif a == '6':
					acl_if_word = 'src ip '
				else:
					acl_if_word = ''

				if acl_then[i] == '5':
					acl += '    use_backend '
				elif acl_then[i] == '2':
					acl += '    http-request redirect location '
				elif acl_then[i] == '3':
					acl += '    http-request allow'
					acl_then_value = ''
				elif acl_then[i] == '4':
					acl += '    http-request deny'
					acl_then_value = ''
				elif acl_then[i] == '6':
					acl += '    return '
				elif acl_then[i] == '7':
					acl += '    set-header '

				acl += acl_then_value + ' if { ' + acl_if_word + acl_value[i] + ' } \n'
			except Exception:
				acl = ''

			i += 1

	if form.getvalue('circuit_breaking') == "1":
		observe = 'observe ' + form.getvalue('circuit_breaking_observe')
		error_limit = ' error-limit ' + form.getvalue('circuit_breaking_error_limit')
		circuit_breaking_on_error = ' on-error ' + form.getvalue('circuit_breaking_on_error')
		default_server = '    default-server ' + observe + error_limit + circuit_breaking_on_error + '\n'
		servers_split += default_server

	if form.getvalue('servers') is not None:
		servers = form.getlist('servers')
		server_port = form.getlist('server_port')
		send_proxy = form.getlist('send_proxy')
		backup = form.getlist('backup')
		server_maxconn = form.getlist('server_maxconn')
		port_check = form.getvalue('port_check')
		i = 0
		for server in servers:
			if form.getvalue('template') is None:
				try:
					if send_proxy[i] == '1':
						send_proxy_param = 'send-proxy'
					else:
						send_proxy_param = ''
				except Exception:
					send_proxy_param = ''

				try:
					if backup[i] == '1':
						backup_param = 'backup'
					else:
						backup_param = ''
				except Exception:
					backup_param = ''

				try:
					maxconn_val = server_maxconn[i]
				except Exception:
					maxconn_val = '200'

				try:
					port_check_val = port_check[i]
				except Exception:
					port_check_val = port

				servers_split += "    server {0} {0}:{1}{2} port {6} maxconn {5} {3} {4} \n".format(server,
																			server_port[i],
																			check,
																			send_proxy_param,
																			backup_param,
																			maxconn_val,
																			port_check_val)
			else:
				servers_split += "    server-template {0} {1} {2}:{3} {4} \n".format(form.getvalue('prefix'),
																						form.getvalue('template-number'),
																						server,
																						server_port[i],
																						check)
			i += 1

	compression = form.getvalue("compression")
	cache = form.getvalue("cache")
	compression_s = ""
	cache_s = ""
	cache_set = ""
	filter_com = ""
	if compression == "1" or cache == "2":
		filter_com = "    filter compression\n"
		if cache == "2":
			cache_s = "    http-request cache-use "+end_name+"\n    http-response cache-store "+end_name+"\n"
			cache_set = "cache "+end_name+"\n    total-max-size 4\n    max-age 240\n"
		if compression == "1":
			compression_s = "    compression algo gzip\n    compression type text/html text/plain text/css\n"

	waf = ""
	if form.getvalue('waf') is not None:
		waf = "    filter spoe engine modsecurity config "+haproxy_dir+"/waf.conf\n"
		waf += "    http-request deny if { var(txn.modsec.code) -m int gt 0 }\n"

	config_add = "\n" + name + "\n" + bind + mode + maxconn + balance + options_split + cache_s + filter_com + compression_s + waf + acl + backend + servers_split + "\n" + cache_set + "\n"

if form.getvalue('new_userlist') is not None:
	name = "userlist "+form.getvalue('new_userlist') + "\n"

	new_userlist_groups = ""
	if form.getvalue('userlist-group') is not None:
		groups = form.getlist('userlist-group')
		for group in groups:
			new_userlist_groups += "    group " + group + "\n"

	new_users_list = ""
	if form.getvalue('userlist-user') is not None:
		users = form.getlist('userlist-user')
		passwords = form.getlist('userlist-password')
		userlist_user_group = form.getlist('userlist-user-group')
		i = 0

		for user in users:
			try:
				group = ' groups '+userlist_user_group[i]
			except Exception:
				group = ''
			new_users_list += "    user "+user+" insecure-password " + passwords[i] + group + "\n"
			i += 1

	config_add = "\n" + name + new_userlist_groups + new_users_list

if form.getvalue('peers-name') is not None:
	name = "peers " + form.getvalue('peers-name') + "\n"
	servers_split = ''

	if form.getvalue('servers') is not None:
		servers = form.getlist('servers')
		server_port = form.getlist('server_port')
		servers_name = form.getlist('servers_name')
		i = 0
		for server in servers:
			servers_split += "    peer {0} {1}:{2} \n".format(servers_name[i], server, server_port[i])

			i += 1

		config_add = "\n" + name + servers_split

if form.getvalue('generateconfig') is None:
	try:
		funct.check_is_server_in_group(serv)
		if config_add:
			hap_configs_dir = funct.get_config_var('configs', 'haproxy_save_configs_dir')
			cfg = hap_configs_dir + serv + "-" + funct.get_data('config') + ".cfg"

			funct.get_config(serv, cfg)
			try:
				with open(cfg, "a") as conf:
					conf.write(config_add)
			except IOError:
				print("error: Can't read import config file")

			funct.logging(serv, "add.py add new %s" % name)

			MASTERS = sql.is_master(serv)
			for master in MASTERS:
				if master[0] is not None:
					funct.upload_and_restart(master[0], cfg)

			stderr = funct.upload_and_restart(serv, cfg, just_save="save")
			if stderr:
				print(stderr)
			else:
				print(name)

	except Exception:
		pass
else:
	print(config_add)
