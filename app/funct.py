# -*- coding: utf-8 -*-
import cgi
import os
import sys


def is_ip_or_dns(server_from_request: str) -> str:
	import re
	ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
	dns_regex = "^(?!-)[A-Za-z0-9-]+([\\-\\.]{1}[a-z0-9]+)*\\.[A-Za-z]{2,6}$"
	try:
		if server_from_request in ('roxy-wi-checker', 'roxy-wi-keep_alive', 'roxy-wi-keep-alive', 'roxy-wi-metrics',
									'roxy-wi-portscanner', 'roxy-wi-smon', 'roxy-wi-socket', 'fail2ban', 'prometheus',
									'all', 'grafana-server', 'rabbitmq-server'):
			return server_from_request
		if re.match(ip_regex, server_from_request):
			return server_from_request
		else:
			if re.match(dns_regex, server_from_request):
				return server_from_request
			else:
				return ''
	except:
		return ''


form = cgi.FieldStorage()
serv = is_ip_or_dns(form.getvalue('serv'))


def get_config_var(sec, var):
	from configparser import ConfigParser, ExtendedInterpolation
	try:
		path_config = "/var/www/haproxy-wi/app/roxy-wi.cfg"
		config = ConfigParser(interpolation=ExtendedInterpolation())
		config.read(path_config)
	except Exception as e:
		print('error: ' + str(e))
		return

	try:
		return config.get(sec, var)
	except Exception:
		print('Content-type: text/html\n')
		print('<center><div class="alert alert-danger">Check the config file. Presence section %s and parameter %s</div>' % (sec, var))
		return


def get_data(log_type, **kwargs):
	from datetime import datetime, timedelta
	from pytz import timezone
	import sql
	fmt = "%Y-%m-%d.%H:%M:%S"

	if kwargs.get('timedelta'):
		try:
			now_utc = datetime.now(timezone(sql.get_setting('time_zone'))) + timedelta(days=kwargs.get('timedelta'))
		except Exception:
			now_utc = datetime.now(timezone('UTC')) + timedelta(days=kwargs.get('timedelta'))
	elif kwargs.get('timedelta_minus'):
		try:
			now_utc = datetime.now(timezone(sql.get_setting('time_zone'))) - timedelta(days=kwargs.get('timedelta_minus'))
		except Exception:
			now_utc = datetime.now(timezone('UTC')) - timedelta(days=kwargs.get('timedelta_minus'))
	elif kwargs.get('timedelta_minutes'):
		try:
			now_utc = datetime.now(timezone(sql.get_setting('time_zone'))) + timedelta(minutes=kwargs.get('timedelta_minutes'))
		except Exception:
			now_utc = datetime.now(timezone('UTC')) + timedelta(minutes=kwargs.get('timedelta_minutes'))
	elif kwargs.get('timedelta_minutes_minus'):
		try:
			now_utc = datetime.now(timezone(sql.get_setting('time_zone'))) - timedelta(minutes=kwargs.get('timedelta_minutes_minus'))
		except Exception:
			now_utc = datetime.now(timezone('UTC')) - timedelta(minutes=kwargs.get('timedelta_minutes_minus'))
	else:
		try:
			now_utc = datetime.now(timezone(sql.get_setting('time_zone')))
		except Exception:
			now_utc = datetime.now(timezone('UTC'))

	if log_type == 'config':
		fmt = "%Y-%m-%d.%H:%M:%S"
	elif log_type == 'logs':
		fmt = '%Y%m%d'
	elif log_type == "date_in_log":
		fmt = "%b %d %H:%M:%S"
	elif log_type == 'regular':
		fmt = "%Y-%m-%d %H:%M:%S"

	return now_utc.strftime(fmt)


def get_user_group(**kwargs):
	import sql
	import http.cookies
	user_group = ''

	try:
		cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
		user_group_id = cookie.get('group')
		user_group_id1 = user_group_id.value
		groups = sql.select_groups(id=user_group_id1)
		for g in groups:
			if g.group_id == int(user_group_id1):
				if kwargs.get('id'):
					user_group = g.group_id
				else:
					user_group = g.name
	except Exception:
		check_user_group()

	return user_group


def logging(server_ip, action, **kwargs):
	import sql
	import http.cookies
	import distro

	login = ''

	log_path = get_config_var('main', 'log_path')
	try:
		user_group = get_user_group()
	except:
		user_group = ''

	if not os.path.exists(log_path):
		os.makedirs(log_path)

	try:
		ip = cgi.escape(os.environ["REMOTE_ADDR"])
	except Exception:
		ip = ''

	try:
		cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
		user_uuid = cookie.get('uuid')
		login = sql.get_user_name_by_uuid(user_uuid.value)
	except Exception:
		login_name = kwargs.get('login')
		try:
			if len(login_name) > 1:
				login = kwargs.get('login')
		except:
			login = ''

	try:
		if distro.id() == 'ubuntu':
			os.system('sudo chown www-data:www-data -R ' + log_path)
		else:
			os.system('sudo chown apache:apache -R ' + log_path)
	except Exception:
		pass

	if kwargs.get('haproxywi') == 1:
		if kwargs.get('login'):
			mess = get_data('date_in_log') + " from " + ip + " user: " + login + ", group: " + user_group + ", " + \
				action + " for: " + server_ip + "\n"
			if kwargs.get('keep_history'):
				try:
					keep_action_history(kwargs.get('service'), action, server_ip, login, ip)
				except Exception as e:
					print(str(e))
		else:
			mess = get_data('date_in_log') + " " + action + " from " + ip + "\n"
		log = open(log_path + "/roxy-wi-"+get_data('logs')+".log", "a")
	elif kwargs.get('provisioning') == 1:
		mess = get_data('date_in_log') + " from " + ip + " user: " + login + ", group: " + user_group + ", " + \
				action + "\n"
		log = open(log_path + "/provisioning-"+get_data('logs')+".log", "a")
	else:
		mess = get_data('date_in_log') + " from " + ip + " user: " + login + ", group: " + user_group + ", " + \
				action + " for: " + server_ip + "\n"
		log = open(log_path + "/config_edit-"+get_data('logs')+".log", "a")

		if kwargs.get('keep_history'):
			keep_action_history(kwargs.get('service'), action, server_ip, login, ip)

	try:
		log.write(mess)
		log.close()
	except IOError as e:
		print('<center><div class="alert alert-danger">Cannot write log. Please check log_path in config %e</div></center>' % e)


def keep_action_history(service: str, action: str, server_ip: str, login: str, user_ip: str):
	import sql
	try:
		server_id = sql.select_server_id_by_ip(server_ip=server_ip)
		if login != '':
			user_id = sql.get_user_id_by_username(login)
		else:
			user_id = 0
		if user_ip == '':
			user_ip = 'localhost'

		sql.insert_action_history(service, action, server_id, user_id, user_ip)
	except Exception as e:
		logging('localhost', 'Cannot save a history: ' + str(e), haproxywi=1)


def telegram_send_mess(mess, **kwargs):
	import telebot
	from telebot import apihelper
	import sql
	token_bot = ''
	channel_name = ''

	if kwargs.get('telegram_channel_id'):
		telegrams = sql.get_telegram_by_id(kwargs.get('telegram_channel_id'))
	else:
		telegrams = sql.get_telegram_by_ip(kwargs.get('ip'))
		slack_send_mess(mess, ip=kwargs.get('ip'))

	proxy = sql.get_setting('proxy')

	for telegram in telegrams:
		token_bot = telegram.token
		channel_name = telegram.chanel_name

	if token_bot == '' or channel_name == '':
		mess = " Can't send message. Add Telegram channel before use alerting at this servers group"
		print(mess)
		logging('localhost', mess, haproxywi=1)

	if proxy is not None and proxy != '' and proxy != 'None':
		apihelper.proxy = {'https': proxy}
	try:
		bot = telebot.TeleBot(token=token_bot)
		bot.send_message(chat_id=channel_name, text=mess)
	except Exception as e:
		print(str(e))
		logging('localhost', str(e), haproxywi=1)


def slack_send_mess(mess, **kwargs):
	import sql
	from slack_sdk import WebClient
	from slack_sdk.errors import SlackApiError
	slack_token = ''
	channel_name = ''

	if kwargs.get('slack_channel_id'):
		slacks = sql.get_slack_by_id(kwargs.get('slack_channel_id'))
	else:
		slacks = sql.get_slack_by_ip(kwargs.get('ip'))

	proxy = sql.get_setting('proxy')

	for slack in slacks:
		slack_token = slack[1]
		channel_name = slack[2]

	if proxy is not None and proxy != '' and proxy != 'None':
		proxies = dict(https=proxy, http=proxy)
		client = WebClient(token=slack_token, proxies=proxies)
	else:
		client = WebClient(token=slack_token)

	try:
		client.chat_postMessage(channel='#'+channel_name, text=mess)
	except SlackApiError as e:
		print('error: ' + str(e))
		logging('localhost', str(e), haproxywi=1)


def check_login(**kwargs):
	import sql
	import http.cookies
	user_uuid = None
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	try:
		user_uuid = cookie.get('uuid')
	except Exception:
		print('<meta http-equiv="refresh" content="0; url=/app/login.py">')
	ref = os.environ.get("REQUEST_URI")

	sql.delete_old_uuid()

	if user_uuid is not None:
		if sql.get_user_name_by_uuid(user_uuid.value) is None:
			print('<meta http-equiv="refresh" content="0; url=login.py?ref=%s">' % ref)
			return False
		if kwargs.get('service'):
			required_service = str(kwargs.get('service'))
			user_id = sql.get_user_id_by_uuid(user_uuid.value)
			user_services = sql.select_user_services(user_id)
			if required_service in user_services:
				return True
			else:
				print('<meta http-equiv="refresh" content="0; url=overview.py">')
				return False

		user, user_uuid, role, token, servers, user_services = get_users_params()
		sql.update_last_act_user(user_uuid.value, token)
	else:
		print('<meta http-equiv="refresh" content="0; url=login.py?ref=%s">' % ref)
		return False


def get_user_id(**kwargs):
	import sql
	if kwargs.get('login'):
		return sql.get_user_id_by_username(kwargs.get('login'))

	import http.cookies
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_uuid = cookie.get('uuid')

	if user_uuid is not None:
		user_id = sql.get_user_id_by_uuid(user_uuid.value)

		return user_id


def is_admin(**kwargs):
	import sql
	import http.cookies
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_id = cookie.get('uuid')
	try:
		role = sql.get_user_role_by_uuid(user_id.value)
	except Exception:
		role = 4
		pass
	level = kwargs.get("level")

	if level is None:
		level = 1

	try:
		return True if role <= level else False
	except Exception:
		return False


def page_for_admin(**kwargs):
	if kwargs.get("level"):
		give_level = kwargs.get("level")
	else:
		give_level = 1

	if not is_admin(level=give_level):
		print('<meta http-equiv="refresh" content="0; url=/">')
		import sys
		sys.exit()


def return_ssh_keys_path(server_ip, **kwargs):
	import sql
	full_path = get_config_var('main', 'fullpath')
	ssh_enable = ''
	ssh_user_name = ''
	ssh_user_password = ''
	ssh_key_name = ''

	if kwargs.get('id'):
		for sshs in sql.select_ssh(id=kwargs.get('id')):
			ssh_enable = sshs.enable
			ssh_user_name = sshs.username
			ssh_user_password = sshs.password
			ssh_key_name = full_path+'/keys/%s.pem' % sshs.name
	else:
		for sshs in sql.select_ssh(serv=server_ip):
			ssh_enable = sshs.enable
			ssh_user_name = sshs.username
			ssh_user_password = sshs.password
			ssh_key_name = full_path+'/keys/%s.pem' % sshs.name

	return ssh_enable, ssh_user_name, ssh_user_password, ssh_key_name


def ssh_connect(server_ip):
	import paramiko
	from paramiko import SSHClient
	import sql

	ssh_enable, ssh_user_name, ssh_user_password, ssh_key_name = return_ssh_keys_path(server_ip)
	servers = sql.select_servers(server=server_ip)
	ssh_port = 22

	for server in servers:
		ssh_port = server[10]

	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		if ssh_enable == 1:
			k = paramiko.pkey.load_private_key_file(ssh_key_name)
			ssh.connect(hostname=server_ip, port=ssh_port, username=ssh_user_name, pkey=k, timeout=11, banner_timeout=200)
		else:
			ssh.connect(hostname=server_ip, port=ssh_port, username=ssh_user_name, password=ssh_user_password, timeout=11, banner_timeout=200)
		return ssh
	except paramiko.AuthenticationException as e:
		logging('localhost', ' ' + str(e), haproxywi=1)
		print('error: Authentication failed, please verify your credentials')
	except paramiko.SSHException as sshException:
		logging('localhost', ' ' + str(sshException), haproxywi=1)
		print('error: Unable to establish SSH connection: %s ') % sshException
	except paramiko.PasswordRequiredException as e:
		logging('localhost', ' ' + str(e), haproxywi=1)
		print('error: %s ') % e
	except paramiko.BadHostKeyException as badHostKeyException:
		logging('localhost', ' ' + str(badHostKeyException), haproxywi=1)
		print('error: Unable to verify server\'s host key: %s ') % badHostKeyException
	except Exception as e:
		logging('localhost', ' ' + str(e), haproxywi=1)
		if e == "No such file or directory":
			print('error: %s. Check SSH key') % e
		elif e == "Invalid argument":
			print('error: Check the IP of the server')
		else:
			print(str(e))


def get_config(server_ip, cfg, **kwargs):
	import sql

	if kwargs.get("keepalived") or kwargs.get("service") == 'keepalived':
		config_path = "/etc/keepalived/keepalived.conf"
	elif (kwargs.get("nginx") or kwargs.get("service") == 'nginx' or
			kwargs.get("apache") or kwargs.get("service") == 'apache'):
		config_path = kwargs.get('config_file_name')
	elif kwargs.get("waf") or kwargs.get("service") == 'waf':
		config_path = sql.get_setting('haproxy_dir') + '/waf/rules/' + kwargs.get("waf_rule_file")
	else:
		config_path = sql.get_setting('haproxy_config_path')

	ssh = ssh_connect(server_ip)
	try:
		sftp = ssh.open_sftp()
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		return

	try:
		sftp.get(config_path, cfg)
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		sftp.close()
		ssh.close()
		return

	try:
		sftp.close()
		ssh.close()
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		return


def diff_config(oldcfg, cfg, **kwargs):
	import http.cookies
	import sql
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	log_path = get_config_var('main', 'log_path')
	user_group = get_user_group()
	diff = ""
	date = get_data('date_in_log')
	cmd = "/bin/diff -ub %s %s" % (oldcfg, cfg)

	try:
		user_uuid = cookie.get('uuid')
		login = sql.get_user_name_by_uuid(user_uuid.value)
	except Exception:
		login = ''

	output, stderr = subprocess_execute(cmd)

	if kwargs.get('return_diff'):
		for line in output:
			diff += line + "\n"
		return diff
	else:
		for line in output:
			diff += date + " user: " + login + ", group: " + user_group + " " + line + "\n"

	try:
		log = open(log_path + "/config_edit-"+get_data('logs')+".log", "a")
		log.write(diff)
		log.close()
	except IOError:
		print('<center><div class="alert alert-danger">Can\'t read write change to log. %s</div></center>' % stderr)
		pass


def get_remote_sections(server_ip: str, service: str) -> str:
	import sql
	remote_dir = service+'_dir'
	config_dir = sql.get_setting(remote_dir)
	config_dir = return_nice_path(config_dir)
	if service == 'nginx':
		section_name = 'server_name'
		commands = [
			'sudo grep {} {}* -R |grep -v \'${}\|#\'|awk \'{{print $1, $3}}\''.format(section_name, config_dir,
																						section_name)]

	elif service == 'apache':
		section_name = 'ServerName'
		commands = [
			'sudo grep {} {}*/*.conf -R |grep -v \'${}\|#\'|awk \'{{print $1, $3}}\''.format(section_name, config_dir,
																							section_name)]

	backends = ssh_command(server_ip, commands)

	return backends


def get_sections(config, **kwargs):
	return_config = list()
	with open(config, 'r') as f:
		for line in f:
			if kwargs.get('service') == 'keepalived':
				import re
				ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
				find_ip = re.findall(ip_pattern, line)
				if find_ip:
					return_config.append(find_ip[0])
			else:
				if line.startswith(('global',
									'listen',
									'frontend',
									'backend',
									'cache',
									'defaults',
									'#HideBlockStart',
									'#HideBlockEnd',
									'peers',
									'resolvers',
									'userlist',
									'http-errors')):
					line = line.strip()
					return_config.append(line)

	return return_config


def get_section_from_config(config, section):
	record = False
	start_line = ""
	end_line = ""
	return_config = ""
	with open(config, 'r') as f:
		for index, line in enumerate(f):
			if line.startswith(section + '\n'):
				start_line = index
				return_config += line
				record = True
				continue
			if record:
				if line.startswith(('global',
									'listen',
									'frontend',
									'backend',
									'cache',
									'defaults',
									'#HideBlockStart',
									'#HideBlockEnd',
									'peers',
									'resolvers',
									'userlist',
									'http-errors')):
					record = False
					end_line = index
					end_line = end_line - 1
				else:
					return_config += line

	if end_line == "":
		f = open(config, "r")
		line_list = f.readlines()
		end_line = len(line_list)

	return start_line, end_line, return_config


def rewrite_section(start_line, end_line, config, section):
	record = False
	start_line = int(start_line)
	end_line = int(end_line)
	return_config = ""
	with open(config, 'r') as f:
		for index, line in enumerate(f):
			index = int(index)
			if index == start_line:
				record = True
				return_config += section
				return_config += "\n"
				continue
			if index == end_line:
				record = False
				continue
			if record:
				continue

			return_config += line

	return return_config


def get_userlists(config):
	return_config = ''
	with open(config, 'r') as f:
		for line in f:
			if line.startswith('userlist'):
				line = line.strip()
				return_config += line + ','

	return return_config


def get_backends_from_config(server_ip, backends=''):
	configs_dir = get_config_var('configs', 'haproxy_save_configs_dir')
	format_cfg = 'cfg'

	try:
		cfg = configs_dir+get_files(dir=configs_dir, format=format_cfg)[0]
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		try:
			cfg = configs_dir + server_ip + "-" + get_data('config') + '.'+format_cfg
		except Exception:
			logging('localhost', ' Cannot generate cfg path', haproxywi=1)
			return
		try:
			get_config(server_ip, cfg)
		except Exception:
			logging('localhost', ' Cannot download config', haproxywi=1)
			print('error: Cannot get backends')
			sys.exit()

	with open(cfg, 'r') as f:
		for line in f:
			if backends == 'frontend':
				if (line.startswith('listen') or line.startswith('frontend')) and 'stats' not in line:
					line = line.strip()
					print(line.split(' ')[1], end="<br>")


def get_all_stick_table():
	import sql
	hap_sock_p = sql.get_setting('haproxy_sock_port')
	cmd = 'echo "show table"|nc %s %s |awk \'{print $3}\' | tr -d \'\n\' | tr -d \'[:space:]\'' % (serv, hap_sock_p)
	output, stderr = subprocess_execute(cmd)
	return output[0]


def get_stick_table(table):
	import sql
	hap_sock_p = sql.get_setting('haproxy_sock_port')
	cmd = 'echo "show table %s"|nc %s %s |awk -F"#" \'{print $2}\' |head -1 | tr -d \'\n\'' % (table, serv, hap_sock_p)
	output, stderr = subprocess_execute(cmd)
	tables_head = []
	for i in output[0].split(','):
		i = i.split(':')[1]
		tables_head.append(i)

	cmd = 'echo "show table %s"|nc %s %s |grep -v "#"' % (table, serv, hap_sock_p)
	output, stderr = subprocess_execute(cmd)

	return tables_head, output


def show_installation_output(error, output, service):
	if error and "WARNING" not in error:
		logging('localhost', error, haproxywi=1)
		print('error: '+error)
		return False
	else:
		for l in output:
			if "UNREACHABLE" in l:
				print(l + '<br />')
			if "Traceback" in l or "FAILED" in l or "error" in l or "ERROR" in l:
				try:
					print(l)
					break
				except Exception:
					print(output)
					break
		else:
			print('success: ' + service + ' has been installed')
			logging('localhost', error, haproxywi=1, keep_history=1, service=service)
			return True


def install_haproxy(server_ip, **kwargs):
	import sql
	script = "install_haproxy.sh"
	hap_sock_p = str(sql.get_setting('haproxy_sock_port'))
	stats_port = str(sql.get_setting('stats_port'))
	server_state_file = sql.get_setting('server_state_file')
	stats_user = sql.get_setting('stats_user')
	stats_password = sql.get_setting('stats_password')
	proxy = sql.get_setting('proxy')
	haproxy_dir = sql.get_setting('haproxy_dir')
	container_name = sql.get_setting('haproxy_container_name')
	haproxy_ver = kwargs.get('hapver')
	server_for_installing = kwargs.get('server')
	docker = kwargs.get('docker')
	ssh_port = 22
	ssh_enable, ssh_user_name, ssh_user_password, ssh_key_name = return_ssh_keys_path(server_ip)

	if ssh_enable == 0:
		ssh_key_name = ''

	servers = sql.select_servers(server=server_ip)
	for server in servers:
		ssh_port = str(server[10])

	os.system("cp scripts/%s ." % script)

	if haproxy_ver is None:
		haproxy_ver = '2.5.1-1'

	if proxy is not None and proxy != '' and proxy != 'None':
		proxy_serv = proxy
	else:
		proxy_serv = ''

	syn_flood_protect = '1' if kwargs.get('syn_flood') == "1" else ''

	commands = ["chmod +x " + script + " &&  ./" + script + " PROXY=" + proxy_serv +
				" SOCK_PORT=" + hap_sock_p + " STAT_PORT=" + stats_port + " STAT_FILE="+server_state_file + " DOCKER=" + docker +
				" SSH_PORT=" + ssh_port + " STATS_USER=" + stats_user + " CONT_NAME=" + container_name + " HAP_DIR=" + haproxy_dir +
				" STATS_PASS='" + stats_password + "' HAPVER=" + haproxy_ver + " SYN_FLOOD=" + syn_flood_protect +
				" HOST=" + server_ip + " USER=" + ssh_user_name + " PASS='" + ssh_user_password + "' KEY=" + ssh_key_name]

	output, error = subprocess_execute(commands[0])
	if server_for_installing:
		service = server_for_installing + ' HAProxy'
	else:
		service = ' HAProxy'

	if show_installation_output(error, output, service):
		sql.update_haproxy(server_ip)

	if docker == '1':
		server_id = sql.select_server_id_by_ip(server_ip)
		sql.insert_or_update_service_setting(server_id, 'haproxy', 'dockerized', '1')

	os.system("rm -f %s" % script)


def waf_install(server_ip):
	import sql
	script = "waf.sh"
	proxy = sql.get_setting('proxy')
	haproxy_dir = sql.get_setting('haproxy_dir')
	ver = check_haproxy_version(server_ip)
	service = ' WAF'
	ssh_enable, ssh_user_name, ssh_user_password, ssh_key_name = return_ssh_keys_path(server_ip)
	ssh_port = '22'

	if ssh_enable == 0:
		ssh_key_name = ''

	os.system("cp scripts/%s ." % script)

	if proxy is not None and proxy != '' and proxy != 'None':
		proxy_serv = proxy
	else:
		proxy_serv = ''

	commands = ["chmod +x " + script + " &&  ./" + script + " PROXY=" + proxy_serv + " HAPROXY_PATH=" + haproxy_dir +
				" VERSION='" + ver + "' SSH_PORT=" + ssh_port + " HOST=" + server_ip +
				" USER=" + ssh_user_name + " PASS='" + ssh_user_password + "' KEY=" + ssh_key_name]

	output, error = subprocess_execute(commands[0])

	if show_installation_output(error, output, service):
		ssh_command(server_ip, commands, print_out="1")

		sql.insert_waf_metrics_enable(server_ip, "0")
		sql.insert_waf_rules(server_ip)

	os.system("rm -f %s" % script)


def install_nginx(server_ip, **kwargs):
	import sql
	script = "install_nginx.sh"
	stats_user = sql.get_setting('nginx_stats_user')
	stats_password = sql.get_setting('nginx_stats_password')
	stats_port = str(sql.get_setting('nginx_stats_port'))
	stats_page = sql.get_setting('nginx_stats_page')
	config_path = sql.get_setting('nginx_config_path')
	nginx_dir = sql.get_setting('nginx_dir')
	server_for_installing = kwargs.get('server')
	proxy = sql.get_setting('proxy')
	docker = kwargs.get('docker')
	container_name = sql.get_setting('nginx_container_name')
	ssh_enable, ssh_user_name, ssh_user_password, ssh_key_name = return_ssh_keys_path(server_ip)
	ssh_port = '22'

	if ssh_enable == 0:
		ssh_key_name = ''

	os.system("cp scripts/%s ." % script)

	if proxy is not None and proxy != '' and proxy != 'None':
		proxy_serv = proxy
	else:
		proxy_serv = ''

	servers = sql.select_servers(server=server_ip)
	for server in servers:
		ssh_port = str(server[10])

	syn_flood_protect = '1' if form.getvalue('syn_flood') == "1" else ''

	commands = ["chmod +x " + script + " &&  ./" + script + " PROXY=" + proxy_serv + " STATS_USER=" + stats_user +
				" STATS_PASS='" + stats_password + "' SSH_PORT=" + ssh_port + " CONFIG_PATH=" + config_path + " CONT_NAME=" + container_name +
				" STAT_PORT=" + stats_port + " STAT_PAGE=" + stats_page+" SYN_FLOOD=" + syn_flood_protect + " DOCKER=" + docker + " nginx_dir=" + nginx_dir +
				" HOST=" + server_ip + " USER=" + ssh_user_name + " PASS='" + ssh_user_password + "' KEY=" + ssh_key_name]

	output, error = subprocess_execute(commands[0])
	if server_for_installing:
		service = server_for_installing + ' Nginx'
	else:
		service = ' Nginx'
	if show_installation_output(error, output, service):
		sql.update_nginx(server_ip)

	if docker == '1':
		server_id = sql.select_server_id_by_ip(server_ip)
		sql.insert_or_update_service_setting(server_id, 'nginx', 'dockerized', '1')

	os.system("rm -f %s" % script)


def update_haproxy_wi(service):
	import distro
	restart_service = ''

	if distro.id() == 'ubuntu':
		try:
			if service == 'roxy-wi-keep_alive':
				service = 'roxy-wi-keep-alive'
		except Exception:
			pass

		if service != 'roxy-wi':
			restart_service = ' && sudo systemctl restart ' + service

		cmd = 'sudo -S apt-get update && sudo apt-get install ' + service + restart_service
	else:
		if service != 'roxy-wi':
			restart_service = ' && sudo systemctl restart ' + service
		cmd = 'sudo -S yum -y update ' + service + restart_service

	output, stderr = subprocess_execute(cmd)
	print(output)
	print(stderr)


def check_haproxy_version(server_ip):
	import sql
	hap_sock_p = sql.get_setting('haproxy_sock_port')
	ver = ""
	cmd = "echo 'show info' |nc %s %s |grep Version |awk '{print $2}'" % (server_ip, hap_sock_p)
	output, stderr = subprocess_execute(cmd)
	for line in output:
		ver = line

	return ver


def upload(server_ip, path, file, **kwargs):
	full_path = path + file
	if kwargs.get('dir') == "fullpath":
		full_path = path

	try:
		ssh = ssh_connect(server_ip)
	except Exception as e:
		error = str(e.args)
		logging('localhost', error, haproxywi=1)
		print(' Cannot upload '+file+' to '+full_path+' to server: '+server_ip+' error: ' + error)
		return error

	try:
		sftp = ssh.open_sftp()
	except Exception as e:
		error = str(e.args)
		logging('localhost', error, haproxywi=1)
		print('Cannot upload '+file+' to '+full_path+' to server: '+server_ip+' error: ' + error)
		return error

	try:
		file = sftp.put(file, full_path)
	except Exception as e:
		error = str(e.args)
		print('Cannot upload ' + file + ' to ' + full_path + ' to server: ' + server_ip + ' error: ' + error)
		logging('localhost', ' Cannot upload ' + file + ' to ' + full_path + ' to server: ' + server_ip + ' Error: ' + error, haproxywi=1)
		return error

	try:
		sftp.close()
		ssh.close()
	except Exception as e:
		error = str(e.args)
		logging('localhost', error, haproxywi=1)
		print('Cannot upload ' + file + ' to ' + full_path + ' to server: ' + server_ip + ' error: ' + error)
		return error


def upload_and_restart(server_ip, cfg, **kwargs):
	import sql
	error = ''
	service_name = ''
	container_name = ''
	reload_or_restart_command = ''
	server_id = sql.select_server_id_by_ip(server_ip=server_ip)

	if kwargs.get("nginx"):
		service = 'nginx'
		config_path = kwargs.get('config_file_name')
		tmp_file = sql.get_setting('tmp_config_path') + "/" + get_data('config') + ".conf"
	elif kwargs.get("apache"):
		service = 'apache'
		config_path = kwargs.get('config_file_name')
		tmp_file = sql.get_setting('tmp_config_path') + "/" + get_data('config') + ".conf"
	elif kwargs.get("keepalived"):
		service = 'keepalived'
		config_path = "/etc/keepalived/keepalived.conf"
		tmp_file = sql.get_setting('tmp_config_path') + "/" + get_data('config') + ".cfg"
	else:
		service = 'haproxy'
		config_path = sql.get_setting('haproxy_config_path')
		tmp_file = sql.get_setting('tmp_config_path') + "/" + get_data('config') + ".cfg"

	is_docker = sql.select_service_setting(server_id, service, 'dockerized')
	if is_docker == '1':
		service_cont_name = service + '_container_name'
		container_name = sql.get_setting(service_cont_name)
		reload_command = " && sudo docker kill -s HUP  " + container_name
		restart_command = " && sudo docker restart " + container_name
	else:
		service_name = service
		if service == 'haproxy':
			haproxy_enterprise = sql.select_service_setting(server_id, 'haproxy', 'haproxy_enterprise')
			if haproxy_enterprise == '1':
				service_name = "hapee-2.0-lb"
		if service == 'apache':
			service_name = get_correct_apache_service_name(server_ip, 0)

		reload_command = " && sudo systemctl reload " + service_name
		restart_command = " && sudo systemctl restart " + service_name

	if kwargs.get("just_save") == 'save':
		action = 'save'
	elif kwargs.get("just_save") == 'test':
		action = 'test'
	elif kwargs.get("just_save") == 'reload':
		action = 'reload'
		reload_or_restart_command = reload_command
	else:
		action = 'restart'
		reload_or_restart_command = restart_command

	if kwargs.get('login'):
		login = kwargs.get('login')
	else:
		login = 1

	try:
		os.system("dos2unix "+cfg)
	except OSError:
		return 'Please install dos2unix'

	if service == "keepalived":
		move_config = "sudo mv -f " + tmp_file + " " + config_path
		if action == "save":
			commands = [move_config]
		else:
			commands = [move_config + reload_or_restart_command]
	elif service == "nginx":
		if is_docker == '1':
			check_config = "sudo docker exec -it exec " + container_name + " nginx -t -q "
		else:
			check_config = "sudo nginx -t -q "
		check_and_move = "sudo mv -f " + tmp_file + " " + config_path + " && " + check_config
		if action == "test":
			commands = [check_config + " && sudo rm -f " + tmp_file]
		elif action == "save":
			commands = [check_and_move]
		else:
			commands = [check_and_move + reload_or_restart_command]
		if sql.return_firewall(server_ip):
			commands[0] += open_port_firewalld(cfg, server_ip=server_ip, service='nginx')
	elif service == "apache":
		if is_docker == '1':
			check_config = "sudo docker exec -it exec " + container_name + " nginx -t -q "
		else:
			check_config = "sudo apachectl configtest "
		check_and_move = "sudo mv -f " + tmp_file + " " + config_path  # + " && " + check_config
		if action == "test":
			commands = [check_config + " && sudo rm -f " + tmp_file]
		elif action == "save":
			commands = [check_and_move]
		else:
			commands = [check_and_move + reload_or_restart_command]
		# if sql.return_firewall(server_ip):
		# 	commands[0] += open_port_firewalld(cfg, server_ip=server_ip, service='nginx')
	else:
		if is_docker == '1':
			check_config = "sudo docker exec -it " + container_name + " haproxy -q -c -f " + tmp_file
		else:
			check_config = "sudo " + service_name + " -c -f " + tmp_file
		move_config = " && sudo mv -f " + tmp_file + " " + config_path

		if action == "test":
			commands = [check_config + " && sudo rm -f " + tmp_file]
		elif action == "save":
			commands = [check_config + move_config]
		else:
			commands = [check_config + move_config + reload_or_restart_command]
		if sql.return_firewall(server_ip):
			commands[0] += open_port_firewalld(cfg, server_ip=server_ip)

	try:
		upload(server_ip, tmp_file, cfg, dir='fullpath')
		try:
			if action != 'test':
				logging(server_ip, 'A new config file has been uploaded', login=login, keep_history=1, service=service)
		except Exception as e:
			logging('localhost', str(e), haproxywi=1)
		# If master then save version of config in a new way

		if not kwargs.get('slave'):
			diff = ''
			old_cfg = kwargs.get('oldcfg')
			if old_cfg is None:
				old_cfg = tmp_file + '.old'
				try:
					get_config(server_ip, old_cfg, service=service, config_file_name=config_path)
				except Exception:
					logging('localhost', ' Cannot download config', haproxywi=1)
			try:
				diff = diff_config(old_cfg, cfg, return_diff=1)
			except Exception as e:
				logging('localhost', str(e), haproxywi=1)

			try:
				user_id = get_user_id(login=kwargs.get('login'))
				sql.insert_config_version(server_id, user_id, service, cfg, config_path, diff)
			except Exception as e:
				logging('localhost', str(e), haproxywi=1)
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		return error

	try:
		error = ssh_command(server_ip, commands)
		try:
			if action == 'reload' or action == 'restart':
				logging(server_ip, 'Service has been ' + action + 'ed', login=login, keep_history=1, service=service)
		except Exception as e:
			logging('localhost', str(e), haproxywi=1)
	except Exception as e:
		logging('localhost', str(e), haproxywi=1)
		return e

	if error.strip() != 'haproxy' and error.strip() != 'nginx':
		return error.strip()


def master_slave_upload_and_restart(server_ip, cfg, just_save, **kwargs):
	import sql
	masters = sql.is_master(server_ip)
	for master in masters:
		if master[0] is not None:
			error = upload_and_restart(master[0],
										cfg,
										just_save=just_save,
										nginx=kwargs.get('nginx'),
										apache=kwargs.get('apache'),
										config_file_name=kwargs.get('config_file_name'),
										slave=1)

	if kwargs.get('login'):
		login = kwargs.get('login')
	else:
		login = ''
	error = upload_and_restart(server_ip,
								cfg,
								just_save=just_save,
								nginx=kwargs.get('nginx'),
								apache=kwargs.get('apache'),
								config_file_name=kwargs.get('config_file_name'),
								oldcfg=kwargs.get('oldcfg'),
								login=login)

	return error


def open_port_firewalld(cfg, server_ip, **kwargs):
	try:
		conf = open(cfg, "r")
	except IOError:
		print('<div class="alert alert-danger">Cannot read exported config file</div>')
		return

	firewalld_commands = ' &&'
	ports = ''

	for line in conf:
		if kwargs.get('service') == 'nginx':
			if "listen " in line and '#' not in line:
				try:
					listen = ' '.join(line.split())
					listen = listen.split(" ")[1]
					listen = listen.split(";")[0]
					try:
						listen = int(listen)
						ports += str(listen)+' '
						firewalld_commands += ' sudo firewall-cmd --zone=public --add-port=%s/tcp --permanent -q &&' % str(listen)
					except Exception:
						pass
				except Exception:
					pass
		else:
			if "bind" in line:
				try:
					bind = line.split(":")
					bind[1] = bind[1].strip(' ')
					bind = bind[1].split("ssl")
					bind = bind[0].strip(' \t\n\r')
					try:
						bind = int(bind)
						firewalld_commands += ' sudo firewall-cmd --zone=public --add-port=%s/tcp --permanent -q &&' % str(bind)
						ports += str(bind)+' '
					except Exception:
						pass
				except Exception:
					pass

	firewalld_commands += 'sudo firewall-cmd --reload -q'
	logging(server_ip, ' Next ports have been opened: ' + ports)
	return firewalld_commands


def check_haproxy_config(server_ip):
	import sql
	server_id = sql.select_server_id_by_ip(server_ip=server_ip)
	is_docker = sql.select_service_setting(server_id, 'haproxy', 'dockerized')
	config_path = sql.get_setting('haproxy_config_path')

	if is_docker == '1':
		container_name = sql.get_setting('haproxy_container_name')
		commands = ["sudo docker exec -it " + container_name + " haproxy -q -c -f " + config_path]
	else:
		commands = ["haproxy  -q -c -f %s" % config_path]

	ssh = ssh_connect(server_ip)
	for command in commands:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		if not stderr.read():
			return True
		else:
			return False
	ssh.close()


def check_nginx_config(server_ip):
	import sql
	commands = ["nginx -q -t -p {}".format(sql.get_setting('nginx_dir'))]
	ssh = ssh_connect(server_ip)
	for command in commands:
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		if not stderr.read():
			return True
		else:
			return False
	ssh.close()


def show_log(stdout, **kwargs):
	i = 0
	out = ''
	grep = ''

	if kwargs.get('grep'):
		import re
		grep = kwargs.get('grep')
		grep = re.sub(r'[?|$|.|!|^|*|\]|\[|,| |]', r'', grep)

	for line in stdout:
		if kwargs.get("html") != 0:
			i = i + 1
			if kwargs.get('grep'):
				line = line.replace(grep, '<span style="color: red; font-weight: bold;">'+grep+'</span>')
			line_class = "line3" if i % 2 == 0 else "line"
			out += '<div class="'+line_class+'">' + line + '</div>'
		else:
			out += line

	return out


def show_finding_in_config(stdout: str, **kwargs) -> str:
	i = 0
	out = ''
	grep = ''
	line_class = 'line'

	if kwargs.get('grep'):
		import re
		grep = kwargs.get('grep')
		grep = re.sub(r'[?|$|!|^|*|\]|\[|,| |]', r'', grep)

	out += '<div class="line">--</div>'
	for line in stdout:
		i = i + 1
		if kwargs.get('grep'):
			line = line.replace(grep, '<span style="color: red; font-weight: bold;">'+grep+'</span>')
			line_class = "line" if '--' in line else "line3"
		out += '<div class="'+line_class+'">' + line + '</div>'

	out += '<div class="line">--</div>'

	return out


def show_haproxy_log(serv, rows=10, waf='0', grep=None, hour='00', minut='00', hour1='24', minut1='00', service='haproxy', **kwargs):
	import sql
	exgrep = form.getvalue('exgrep')
	log_file = form.getvalue('file')
	date = hour+':'+minut
	date1 = hour1+':'+minut1
	cmd = ''

	if grep is not None:
		grep_act = '|egrep "%s"' % grep
	else:
		grep_act = ''

	if exgrep is not None:
		exgrep_act = '|egrep -v "%s"' % exgrep
	else:
		exgrep_act = ''

	if service == 'nginx' or service == 'haproxy' or service == 'apache':
		syslog_server_enable = sql.get_setting('syslog_server_enable')
		if syslog_server_enable is None or syslog_server_enable == 0:
			if service == 'nginx':
				local_path_logs = sql.get_setting('nginx_path_logs')
				commands = ["sudo cat %s/%s |tail -%s %s %s" % (local_path_logs, log_file, rows, grep_act, exgrep_act)]
			elif service == 'apache':
				local_path_logs = sql.get_setting('apache_path_logs')
				commands = ["sudo cat %s/%s| awk -F\"/|:\" '$3>\"%s:00\" && $3<\"%s:00\"' |tail -%s %s %s" % (local_path_logs, log_file, date, date1, rows, grep_act, exgrep_act)]
			else:
				local_path_logs = sql.get_setting('haproxy_path_logs')
				commands = ["sudo cat %s/%s| awk '$3>\"%s:00\" && $3<\"%s:00\"' |tail -%s %s %s" % (local_path_logs, log_file, date, date1, rows, grep_act, exgrep_act)]
			syslog_server = serv
		else:
			commands = ["sudo cat /var/log/%s/syslog.log | sed '/ %s:00/,/ %s:00/! d' |tail -%s %s %s %s" % (serv, date, date1, rows, grep_act, grep, exgrep_act)]
			syslog_server = sql.get_setting('syslog_server')

		if waf == "1":
			local_path_logs = '/var/log/waf.log'
			commands = ["sudo cat %s |tail -%s %s %s" % (local_path_logs, rows, grep_act, exgrep_act)]

		if kwargs.get('html') == 0:
			a = ssh_command(syslog_server, commands)
			return show_log(a, html=0, grep=grep)
		else:
			return ssh_command(syslog_server, commands, show_log='1', grep=grep)
	elif service == 'apache_internal':
		apache_log_path = sql.get_setting('apache_log_path')

		if serv == 'roxy-wi.access.log':
			cmd = "sudo cat {}| awk -F\"/|:\" '$3>\"{}:00\" && $3<\"{}:00\"' |tail -{} {} {}".format(apache_log_path+"/"+serv, date, date1, rows, grep_act, exgrep_act)
		elif serv == 'roxy-wi.error.log':
			cmd = "sudo cat {}| awk '$4>\"{}:00\" && $4<\"{}:00\"' |tail -{} {} {}".format(apache_log_path+"/"+serv, date, date1, rows, grep_act, exgrep_act)
		elif serv == 'fail2ban.log':
			cmd = "sudo cat {}| awk -F\"/|:\" '$3>\"{}:00\" && $3<\"{}:00\"' |tail -{} {} {}".format("/var/log/"+serv, date, date1, rows, grep_act, exgrep_act)

		output, stderr = subprocess_execute(cmd)

		return show_log(output, grep=grep)
	elif service == 'internal':
		user_group = get_user_group()

		if user_group != '' and user_group != 'Default':
			user_grep = "|grep 'group: " + user_group + "'"
		else:
			user_grep = ''

		log_path = get_config_var('main', 'log_path')
		logs_files = get_files(log_path, format="log")

		for key, value in logs_files:
			if int(serv) == key:
				serv = value
				break
		else:
			print('Haha')
			sys.exit()

		if serv == 'backup.log':
			cmd = "cat %s| awk '$2>\"%s:00\" && $2<\"%s:00\"' %s %s %s |tail -%s" % (log_path + serv, date, date1, user_grep, grep_act, exgrep_act, rows)
		else:
			cmd = "cat %s| awk '$3>\"%s:00\" && $3<\"%s:00\"' %s %s %s |tail -%s" % (log_path + serv, date, date1, user_grep, grep_act, exgrep_act, rows)

		output, stderr = subprocess_execute(cmd)

		return show_log(output, grep=grep)


def haproxy_wi_log(**kwargs):
	log_path = get_config_var('main', 'log_path')

	if kwargs.get('log_id'):
		selects = get_files(log_path, format="log")
		for key, value in selects:
			if kwargs.get('with_date'):
				log_file = kwargs.get('file')+get_data('logs')+".log"
			else:
				log_file = kwargs.get('file')+".log"
			if log_file == value:
				return key
	else:
		user_group_id = get_user_group(id=1)
		if user_group_id != 1:
			user_group = get_user_group()
			group_grep = '|grep "group: ' + user_group + '"'
		else:
			group_grep = ''
		cmd = "find "+log_path+"/roxy-wi-* -type f -exec stat --format '%Y :%y %n' '{}' \; | sort -nr | cut -d: -f2- | head -1 |awk '{print $4}' |xargs tail"+group_grep+"|sort -r"
		try:
			output, stderr = subprocess_execute(cmd)
			return output
		except:
			return ''


def show_ip(stdout):
	for line in stdout:
		if "Permission denied" in line:
			print('error: '+line)
		else:
			print(line)


def server_status(stdout):
	proc_count = ""

	for line in stdout:
		if "Ncat: " not in line:
			for k in line:
				try:
					proc_count = k.split(":")[1]
				except Exception:
					proc_count = 1
		else:
			proc_count = 0
	return proc_count


def ssh_command(server_ip, commands, **kwargs):
	ssh = ssh_connect(server_ip)

	for command in commands:
		try:
			stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
		except Exception as e:
			logging('localhost', ' ' + str(e), haproxywi=1)
			ssh.close()
			return str(e)

		if kwargs.get('raw'):
			return stdout
		try:
			if kwargs.get("ip") == "1":
				show_ip(stdout)
			elif kwargs.get("show_log") == "1":
				return show_log(stdout, grep=kwargs.get("grep"))
			elif kwargs.get("server_status") == "1":
				server_status(stdout)
			elif kwargs.get('print_out'):
				print(stdout.read().decode(encoding='UTF-8'))
				return stdout.read().decode(encoding='UTF-8')
			elif kwargs.get('return_err') == 1:
				return stderr.read().decode(encoding='UTF-8')
			else:
				return stdout.read().decode(encoding='UTF-8')
		except Exception as e:
			logging('localhost', str(e), haproxywi=1)
		finally:
			ssh.close()

		for line in stderr.read().decode(encoding='UTF-8'):
			if line:
				print("<div class='alert alert-warning'>"+line+"</div>")
				logging('localhost', ' '+line, haproxywi=1)


def subprocess_execute(cmd):
	import subprocess
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
	stdout, stderr = p.communicate()
	output = stdout.splitlines()

	return output, stderr


def show_backends(server_ip, **kwargs):
	import json
	import sql
	hap_sock_p = sql.get_setting('haproxy_sock_port')
	cmd = 'echo "show backend" |nc %s %s' % (server_ip, hap_sock_p)
	output, stderr = subprocess_execute(cmd)
	if stderr:
		logging('localhost', ' '+stderr, haproxywi=1)
	if kwargs.get('ret'):
		ret = list()
	else:
		ret = ""
	for line in output:
		if "#" in line or "stats" in line or "MASTER" in line:
			continue
		if len(line) > 1:
			back = json.dumps(line).split("\"")
			if kwargs.get('ret'):
				ret.append(back[1])
			else:
				print(back[1], end="<br>")

	if kwargs.get('ret'):
		return ret


def get_files(dir=get_config_var('configs', 'haproxy_save_configs_dir'), format='cfg'):
	import glob
	if format == 'log':
		file = []
	else:
		file = set()
	return_files = set()
	i = 0
	for files in sorted(glob.glob(os.path.join(dir, '*.'+format+'*'))):
		if format == 'log':
			file += [(i, files.split('/')[5])]
		else:
			file.add(files.split('/')[-1])
		i += 1
	files = file
	if format == 'cfg' or format == 'conf':
		for file in files:
			ip = file.split("-")
			if serv == ip[0]:
				return_files.add(file)
		return sorted(return_files, reverse=True)
	else:
		return file


def get_remote_files(server_ip: str, config_dir: str, file_format: str):
	config_dir = return_nice_path(config_dir)
	if file_format == 'conf':
		commands = ['sudo ls ' + config_dir + '*/*.' + file_format]
	else:
		commands = ['sudo ls ' + config_dir + '|grep ' + file_format + '$']
	config_files = ssh_command(server_ip, commands)

	return config_files


def return_nice_path(return_path: str) -> str:
	if ('nginx' not in return_path and
			'haproxy' not in return_path and
			'apache2' not in return_path and
			'httpd' not in return_path):
		return 'error: The path must contain the name of the service. Check it in Roxy-WI settings'
	if return_path[-1] != '/':
		return_path += '/'

	return return_path


def get_key(item):
	return item[0]


def check_ver():
	import sql
	return sql.get_ver()


def check_new_version(**kwargs):
	import requests
	import sql
	current_ver = check_ver()
	proxy = sql.get_setting('proxy')
	res = ''

	if kwargs.get('service'):
		last_ver = '_'+kwargs.get('service')
	else:
		last_ver = ''

	user_name = sql.select_user_name()

	try:
		if proxy is not None and proxy != '' and proxy != 'None':
			proxy_dict = {"https": proxy, "http": proxy}
			response = requests.get('https://roxy-wi.org/update.py?last_ver'+last_ver+'=1', timeout=1,  proxies=proxy_dict)
			requests.get('https://roxy-wi.org/update.py?ver_send='+current_ver, timeout=1,  proxies=proxy_dict)
			response_status = requests.get('https://roxy-wi.org/update.py?user_name='+user_name, timeout=1,  proxies=proxy_dict)
		else:
			response = requests.get('https://roxy-wi.org/update.py?last_ver'+last_ver+'=1', timeout=1)
			requests.get('https://roxy-wi.org/update.py?ver_send='+current_ver, timeout=1)
			response_status = requests.get('https://roxy-wi.org/update.py?user_name=' + user_name, timeout=1)

		res = response.content.decode(encoding='UTF-8')
		try:
			status = response_status.content.decode(encoding='UTF-8')
			status = status.split(' ')
			sql.update_user_status(status[0], status[1].strip(), status[2].strip())
		except:
			pass
	except requests.exceptions.RequestException as e:
		logging('localhost', ' '+str(e), haproxywi=1)

	return res


def versions():
	try:
		current_ver = check_ver()
		current_ver_without_dots = current_ver.split('.')
		current_ver_without_dots = ''.join(current_ver_without_dots)
		current_ver_without_dots = current_ver_without_dots.replace('\n', '')
		if len(current_ver_without_dots) == 2:
			current_ver_without_dots += '00'
		if len(current_ver_without_dots) == 3:
			current_ver_without_dots += '0'
		current_ver_without_dots = int(current_ver_without_dots)
	except Exception:
		current_ver = "Sorry cannot get current version"
		current_ver_without_dots = 0

	try:
		new_ver = check_new_version()
		new_ver_without_dots = new_ver.split('.')
		new_ver_without_dots = ''.join(new_ver_without_dots)
		new_ver_without_dots = new_ver_without_dots.replace('\n', '')
		if len(new_ver_without_dots) == 2:
			new_ver_without_dots += '00'
		if len(new_ver_without_dots) == 3:
			new_ver_without_dots += '0'
		new_ver_without_dots = int(new_ver_without_dots)
	except Exception:
		new_ver = "Cannot get a new version"
		new_ver_without_dots = 0

	return current_ver, new_ver, current_ver_without_dots, new_ver_without_dots


def get_hash(value):
	if value is None:
		return value
	import hashlib
	h = hashlib.md5(value.encode('utf-8'))
	p = h.hexdigest()
	return p


def get_users_params(**kwargs):
	import http.cookies
	import sql
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))

	try:
		user_uuid = cookie.get('uuid')
		user = sql.get_user_name_by_uuid(user_uuid.value)
		role = sql.get_user_role_by_uuid(user_uuid.value)
		user_id = sql.get_user_id_by_uuid(user_uuid.value)
		user_services = sql.select_user_services(user_id)
		token = sql.get_token(user_uuid.value)
	except:
		print('<meta http-equiv="refresh" content="0; url=/app/login.py">')

	if kwargs.get('virt') and kwargs.get('haproxy'):
		servers = sql.get_dick_permit(virt=1, haproxy=1)
	elif kwargs.get('virt'):
		servers = sql.get_dick_permit(virt=1)
	elif kwargs.get('disable'):
		servers = sql.get_dick_permit(disable=0)
	elif kwargs.get('haproxy'):
		servers = sql.get_dick_permit(haproxy=1)
	else:
		servers = sql.get_dick_permit()

	return user, user_uuid, role, token, servers, user_services


def check_user_group(**kwargs):
	if kwargs.get('token') is not None:
		return True

	import sql
	if kwargs.get('user_uuid'):
		group_id = kwargs.get('user_group_id')
		user_uuid = kwargs.get('user_uuid')
		user_id = sql.get_user_id_by_uuid(user_uuid)
	else:
		import http.cookies
		import os
		cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
		user_uuid = cookie.get('uuid')
		group = cookie.get('group')
		group_id = group.value
		user_id = sql.get_user_id_by_uuid(user_uuid.value)

	if sql.check_user_group(user_id, group_id):
		return True
	else:
		logging('localhost', ' has tried to actions in not his group ', haproxywi=1, login=1)
		print('Atata!')


def check_is_server_in_group(server_ip):
	import sql
	group_id = get_user_group(id=1)
	servers = sql.select_servers(server=server_ip)
	for s in servers:
		if (s[2] == server_ip and int(s[3]) == int(group_id)) or group_id == 1:
			return True
		else:
			logging('localhost', ' has tried to actions in not his group server ', haproxywi=1, login=1)
			print('Atata!')
			sys.exit()


def check_service(server_ip, service_name):
	server_ip = is_ip_or_dns(server_ip)
	commands = ["systemctl is-active "+service_name]
	return ssh_command(server_ip, commands)


def get_service_version(server_ip, service_name):
	server_ip = is_ip_or_dns(server_ip)
	if service_name == 'haproxy_exporter':
		commands = ["/opt/prometheus/exporters/haproxy_exporter --version 2>&1 |head -1|awk '{print $3}'"]
	elif service_name == 'nginx_exporter':
		commands = ["/opt/prometheus/exporters/nginx_exporter 2>&1 |head -1 |awk -F\"=\" '{print $2}'|awk '{print $1}'"]
	elif service_name == 'node_exporter':
		commands = ["node_exporter --version 2>&1 |head -1|awk '{print $3}'"]

	ver = ssh_command(server_ip, commands)

	if ver != '':
		return ver
	else:
		return 'no'


def get_services_status():
	import distro
	services = []
	is_in_docker = is_docker()
	services_name = {'roxy-wi-checker': 'Checker backends master service',
						'roxy-wi-keep_alive': 'Auto start service',
						'roxy-wi-metrics': 'Metrics master service',
						'roxy-wi-portscanner': 'Port scanner service',
						'roxy-wi-smon': 'Simple monitoring network ports',
						'roxy-wi-socket': 'Socket service',
						'prometheus': 'Prometheus service',
						'grafana-server': 'Grafana service',
						'fail2ban': 'Fail2ban service',
						'rabbitmq-server': 'Message broker service'}
	for s, v in services_name.items():
		if is_in_docker:
			cmd = "sudo supervisorctl status " + s + "|awk '{print $2}'"
		else:
			cmd = "systemctl is-active %s" % s
		status, stderr = subprocess_execute(cmd)
		if s != 'roxy-wi-keep_alive':
			service_name = s.split('_')[0]
			if s == 'grafana-server':
				service_name = 'grafana'
		elif s == 'roxy-wi-keep_alive' and distro.id() == 'ubuntu':
			service_name = 'roxy-wi-keep-alive'
		else:
			service_name = s

		if service_name == 'prometheus':
			cmd = "prometheus --version 2>&1 |grep prometheus|awk '{print $3}'"
		else:
			if distro.id() == 'ubuntu':
				cmd = "apt list --installed 2>&1 |grep " + service_name + "|awk '{print $2}'|sed 's/-/./'"
			else:
				cmd = "rpm -q " + service_name + "|awk -F\"" + service_name + "\" '{print $2}' |awk -F\".noa\" '{print $1}' |sed 's/-//1' |sed 's/-/./'"
		service_ver, stderr = subprocess_execute(cmd)

		try:
			if service_ver[0] == 'command' or service_ver[0] == 'prometheus:':
				service_ver[0] = ''
		except Exception:
			pass

		try:
			services.append([s, status, v, service_ver[0]])
		except Exception:
			services.append([s, status, v, ''])

	return services


def is_file_exists(server_ip: str, file: str):
	cmd = ['[ -f ' + file + ' ] && echo yes || echo no']

	out = ssh_command(server_ip, cmd)
	return True if 'yes' in out else False


def is_service_active(server_ip: str, service_name: str):
	cmd = ['systemctl is-active ' + service_name]

	out = ssh_command(server_ip, cmd)
	out = out.strip()
	return True if 'active' == out else False


def get_system_info(server_ip: str) -> bool:
	import json
	import sql
	server_ip = is_ip_or_dns(server_ip)
	if server_ip == '':
		return False

	server_id = sql.select_server_id_by_ip(server_ip)

	command = ["sudo lshw -quiet -json"]
	sys_info_returned = ssh_command(server_ip, command)
	command = ['sudo hostnamectl |grep "Operating System"|awk -F":" \'{print $2}\'']
	os_info = ssh_command(server_ip, command)
	os_info = os_info.strip()
	system_info = json.loads(sys_info_returned)

	sys_info = {'hostname': system_info['id'], 'family': ''}
	cpu = {'cpu_model': '', 'cpu_core': 0, 'cpu_thread': 0, 'hz': 0}
	network = {}
	ram = {'slots': 0, 'size': 0}
	disks = {}

	try:
		sys_info['family'] = system_info['configuration']['family']
	except Exception:
		pass

	for i in system_info['children']:
		if i['class'] == 'network':
			try:
				ip = i['configuration']['ip']
			except Exception:
				ip = ''
			network[i['logicalname']] = {'description': i['description'],
											'mac': i['serial'],
											'ip': ip}
		for k, j in i.items():
			if isinstance(j, list):
				for b in j:
					try:
						if b['class'] == 'processor':
							cpu['cpu_model'] = b['product']
							cpu['cpu_core'] += 1
							cpu['hz'] = round(int(b['capacity']) / 1000000)
							try:
								cpu['cpu_thread'] += int(b['configuration']['threads'])
							except Exception:
								cpu['cpu_thread'] = 1
					except Exception:
						pass

					try:
						if b['id'] == 'memory':
							ram['size'] = round(b['size'] / 1073741824)
							for memory in b['children']:
								ram['slots'] += 1
					except Exception:
						pass

					try:
						if b['class'] == 'storage':
							for p, pval in b.items():
								if isinstance(pval, list):
									for disks_info in pval:
										for volume_info in disks_info['children']:
											if isinstance(volume_info['logicalname'], list):
												volume_name = volume_info['logicalname'][0]
												mount_point = volume_info['logicalname'][1]
												size = round(volume_info['capacity'] / 1073741824)
												size = str(size) + 'Gb'
												fs = volume_info['configuration']['mount.fstype']
												state = volume_info['configuration']['state']
												disks[volume_name] = {'mount_point': mount_point,
																		'size': size,
																		'fs': fs,
																		'state': state}
					except Exception:
						pass

					try:
						if b['class'] == 'bridge':
							if 'children' in b:
								for s in b['children']:
									if s['class'] == 'network':
										if 'children' in s:
											for net in s['children']:
												network[net['logicalname']] = {'description': net['description'],
																				'mac': net['serial']}
									if s['class'] == 'storage':
										for p, pval in s.items():
											if isinstance(pval, list):
												for disks_info in pval:
													if 'children' in disks_info:
														for volume_info in disks_info['children']:
															if isinstance(volume_info['logicalname'], dict):
																volume_name = volume_info['logicalname'][0]
																mount_point = volume_info['logicalname'][1]
																size = round(volume_info['size'] / 1073741824)
																size = str(size) + 'Gb'
																fs = volume_info['configuration']['mount.fstype']
																state = volume_info['configuration']['state']
																disks[volume_name] = {'mount_point': mount_point,
																						'size': size,
																						'fs': fs,
																						'state': state}
									for z, n in s.items():
										if isinstance(n, list):
											for y in n:
												if y['class'] == 'network':
													try:
														for q in y['children']:
															try:
																ip = q['configuration']['ip']
															except Exception:
																ip = ''
															network[q['logicalname']] = {
																'description': q['description'],
																'mac': q['serial'],
																'ip': ip}
													except Exception:
														try:
															network[y['logicalname']] = {
																'description': y['description'],
																'mac': y['serial'],
																'ip': y['configuration']['ip']}
														except Exception:
															pass
												if y['class'] == 'disk':
													try:
														for q in y['children']:
															try:
																if isinstance(q['logicalname'], list):
																	volume_name = q['logicalname'][0]
																	mount_point = q['logicalname'][1]
																	size = round(q['capacity'] / 1073741824)
																	size = str(size) + 'Gb'
																	fs = q['configuration']['mount.fstype']
																	state = q['configuration']['state']
																	disks[volume_name] = {'mount_point': mount_point,
																							'size': size,
																							'fs': fs,
																							'state': state}
															except Exception as e:
																print(e)
													except Exception:
														pass
												if y['class'] == 'storage' or y['class'] == 'generic':
													try:
														for q in y['children']:
															for o in q['children']:
																try:
																	volume_name = o['logicalname']
																	mount_point = ''
																	size = round(o['size'] / 1073741824)
																	size = str(size) + 'Gb'
																	fs = ''
																	state = ''
																	disks[volume_name] = {
																		'mount_point': mount_point,
																		'size': size,
																		'fs': fs,
																		'state': state}
																except Exception:
																	pass
																for w in o['children']:
																	try:
																		if isinstance(w['logicalname'], list):
																			volume_name = w['logicalname'][0]
																			mount_point = w['logicalname'][1]
																			size = round(w['size'] / 1073741824)
																			size = str(size) + 'Gb'
																			fs = w['configuration']['mount.fstype']
																			state = w['configuration']['state']
																			disks[volume_name] = {
																				'mount_point': mount_point,
																				'size': size,
																				'fs': fs,
																				'state': state}
																	except Exception:
																		pass
													except Exception:
														pass
													try:
														for q, qval in y.items():
															if isinstance(qval, list):
																for o in qval:
																	for w in o['children']:
																		if isinstance(w['logicalname'], list):
																			volume_name = w['logicalname'][0]
																			mount_point = w['logicalname'][1]
																			size = round(w['size'] / 1073741824)
																			size = str(size) + 'Gb'
																			fs = w['configuration']['mount.fstype']
																			state = w['configuration']['state']
																			disks[volume_name] = {
																				'mount_point': mount_point,
																				'size': size,
																				'fs': fs,
																				'state': state}
													except Exception:
														pass
					except Exception:
						pass

	if sql.insert_system_info(server_id, os_info, sys_info, cpu, ram, network, disks):
		return True
	else:
		return False


def string_to_dict(dict_string) -> dict:
	from ast import literal_eval
	return literal_eval(dict_string)


def send_message_to_rabbit(message: str, **kwargs) -> None:
	import pika
	import sql
	rabbit_user = sql.get_setting('rabbitmq_user')
	rabbit_password = sql.get_setting('rabbitmq_password')
	rabbit_host = sql.get_setting('rabbitmq_host')
	rabbit_port = sql.get_setting('rabbitmq_port')
	rabbit_vhost = sql.get_setting('rabbitmq_vhost')
	if kwargs.get('rabbit_queue'):
		rabbit_queue = kwargs.get('rabbit_queue')
	else:
		rabbit_queue = sql.get_setting('rabbitmq_queue')

	credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
	parameters = pika.ConnectionParameters(rabbit_host,
											rabbit_port,
											rabbit_vhost,
											credentials)

	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_declare(queue=rabbit_queue)
	channel.basic_publish(exchange='', routing_key=rabbit_queue, body=message)

	connection.close()


def is_restarted(server_ip, action):
	import sql
	import http.cookies

	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_uuid = cookie.get('uuid')
	user_role = sql.get_user_role_by_uuid(user_uuid.value)

	if sql.is_serv_protected(server_ip) and int(user_role) > 2:
		print('error: This server is protected. You cannot ' + action + ' it')
		sys.exit()


def return_user_status():
	import sql

	user_status = sql.select_user_status()
	user_plan = sql.select_user_plan()

	return user_status, user_plan


def get_correct_apache_service_name(server_ip=0, server_id=0) -> str:
	import sql

	if server_id == 0:
		server_id = sql.select_server_id_by_ip(server_ip)

	os_info = sql.select_os_info(server_id)

	if "CentOS" in os_info or "Redhat" in os_info:
		return 'httpd'
	else:
		return 'apache2'


def is_docker() -> bool:
	import os
	import re

	path = "/proc/self/cgroup"
	if not os.path.isfile(path):
		return False
	with open(path) as f:
		for line in f:
			if re.match("\d+:[\w=]+:/docker(-[ce]e)?/\w+", line):
				return True
		return False
