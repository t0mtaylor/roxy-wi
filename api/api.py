#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from bottle import route, run, template, hook, response, request, error
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(sys.path[0], '/var/www/haproxy-wi/app/'))

import api_funct
import json
import sql

_error_auth = '403 Auth before'
_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@hook('before_request')
def check_login(required_service=0):
	return api_funct.check_login(required_service=required_service)


@hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = _allow_origin
	response.headers['Access-Control-Allow-Methods'] = _allow_methods
	response.headers['Access-Control-Allow-Headers'] = _allow_headers

	
@error(500)
def error_handler_500(error):
	return json.dumps({"status": "error", "message": str(error.exception)})
	
	
@route('/', method=['GET', 'POST'])
@route('/help', method=['GET', 'POST'])
def index():
	if not check_login(required_service=1):
		return dict(error=_error_auth)
		
	data = {
		'help': 'show all available endpoints',
		'login': 'get temporarily token. Must be JSON body: login, password and group for which getting token. METHOD: POST',
		'servers':'show info about all servers. METHOD: GET',
		'servers/status':'show status all HAProxyes. METHOD: GET',
		'haproxy/<id,hostname,ip>':'show info about the HAProxy by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/status':'show HAProxy status by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/runtime':'exec HAProxy runtime commands by id or hostname or ip. Must be JSON body: "command". METHOD: POST',
		'haproxy/<id,hostname,ip>/backends':'show backends by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/action/start':'start HAProxy service by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/action/stop':'stop HAProxy service by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/action/restart':'restart HAProxy service by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/config':'get HAProxy config from a server by id or hostname or ip. METHOD: GET',
		'haproxy/<id,hostname,ip>/config':'upload HAProxy config to a server by id or hostname or ip. Headers: action: save/reload/restart. Body must consist a whole HAProxy config. METHOD: POST',
		'haproxy/<id,hostname,ip>/log':'show HAProxy logs by id or hostname or ip. May to have config next Headers: rows(format INT) default: 10 grep, waf(if needs WAF log) default: 0, start_hour(format: 24) default: 00, start_minute, end_hour(format: 24) default: 24, end_minute. METHOD: GET',
		'haproxy/<id,hostname,ip>/section':'show a certain section, headers: section-name. METHOD: GET',
		'haproxy/<id,hostname,ip>/section/add':'add a section to the HAProxy config by id or hostname or ip. Has to have config header with section and action header for action after upload. Section header must consist type: listen, frontend, etc. Action header accepts next value: save, test, reload and restart. Can be empty for just save. METHOD: POST',
		'haproxy/<id,hostname,ip>/section/edit':'edit a section in the HAProxy config by id or hostname or ip. Has to have config header with section, action header for action after upload and body of a new section configuration. Section header must consist type: listen, frontend, etc. Action header accepts next value: save, test, reload and restart. Can be empty for just save. METHOD: POST',
		'haproxy/<id,hostname,ip>/acl':'add an acl to certain section. Must be JSON body: "section-name", "if", "then", "if_value", "then_value" and "action" for action after upload. Action accepts next value: "save", "test", "reload" and "restart". METHOD: POST',
		'haproxy/<id,hostname,ip>/acl':'delete an acl to certain section. Must be JSON body: "section-name", "if", "then", "if_value", "then_value" and "action" for action after upload. Action accepts next value: "save", "test", "reload" and "restart". METHOD: DELETE',
		'nginx/<id,hostname,ip>': 'show info about the NGINX by id or hostname or ip. METHOD: GET',
		'nginx/<id,hostname,ip>/status': 'show NGINX status by id or hostname or ip. METHOD: GET',
		'nginx/<id,hostname,ip>/action/start': 'start NGINX service by id or hostname or ip. METHOD: GET',
		'nginx/<id,hostname,ip>/action/stop': 'stop NGINX service by id or hostname or ip. METHOD: GET',
		'nginx/<id,hostname,ip>/action/restart': 'restart NGINX service by id or hostname or ip. METHOD: GET',
		'nginx/<id,hostname,ip>/config': 'get NGINX config from a server by id or hostname or ip. Headers: The full path to a config file, like: /etc/nginx/conf.d/default.conf. METHOD: GET',
		'nginx/<id,hostname,ip>/config': 'upload NGINX config to a server by id or hostname or ip. Headers: action: save/reload/restart, config-file: the full path to the config, like /etc/nginx/conf.d/example.com.conf. Body must consist a whole HAProxy config. METHOD: POST',
		'apache/<id,hostname,ip>': 'show info about the Apache by id or hostname or ip. METHOD: GET',
		'apache/<id,hostname,ip>/status': 'show Apache status by id or hostname or ip. METHOD: GET',
		'apache/<id,hostname,ip>/action/start': 'start Apache service by id or hostname or ip. METHOD: GET',
		'apache/<id,hostname,ip>/action/stop': 'stop Apache service by id or hostname or ip. METHOD: GET',
		'apache/<id,hostname,ip>/action/restart': 'restart Apache service by id or hostname or ip. METHOD: GET',
		'apache/<id,hostname,ip>/config': 'get Apache config from a server by id or hostname or ip. Headers: The full path to a config file, like: /etc/httpd/conf.d/default.conf. METHOD: GET',
		'apache/<id,hostname,ip>/config': 'upload Apache config to a server by id or hostname or ip. Headers: action: save/reload/restart, config-file: the full path to the config, like /etc/httpd/conf.d/example.com.conf. Body must consist a whole HAProxy config. METHOD: POST',
	}
	return dict(help=data)


@route('/login', method=['POST'])
def get_token():
	token = api_funct.get_token()
	return dict(token=token)


@route('/servers', method=['GET'])
def get_servers():
	if not check_login():
		return dict(error=_error_auth)
	data = {}
	try:
		token = request.headers.get('token')
		login, group_id = sql.get_username_groupid_from_api_token(token)
		servers = sql.get_dick_permit(username=login, group_id=group_id, token=token)

		for s in servers:
			data[s[0]] = {
				'server_id':s[0],
				'hostname':s[1],
				'ip':s[2],
				'group':s[3],
				'virt':s[4],
				'enable':s[5],
				'is_master':s[6],
				'creds':s[7],
				'alert':s[8],
				'metrics':s[9]
			}
	except:
		pass

	return dict(servers=data)


@route('/servers/status', method=['GET'])
def callback():
	if not check_login():
		return dict(error=_error_auth)
	return api_funct.get_all_statuses()


@route('/haproxy/<haproxy_id>/runtime', method=['POST'])
@route('/haproxy/<haproxy_id:int>/runtime', method=['POST'])
def callback(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.runtime(haproxy_id)


@route('/haproxy/<haproxy_id>/backends', method=['GET'])
@route('/haproxy/<haproxy_id:int>/backends', method=['GET'])
def callback(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.show_backends(haproxy_id)


@route('/haproxy/<haproxy_id>/log', method=['GET'])
@route('/haproxy/<haproxy_id:int>/log', method=['GET'])
def callback(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.show_log(haproxy_id)


@route('/haproxy/<haproxy_id>/section', method=['GET'])
def get_section(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	print(str(request.headers.get('section-name')))
	return api_funct.get_section(haproxy_id)


@route('/haproxy/<haproxy_id>/section/add', method=['POST'])
@route('/haproxy/<haproxy_id:int>/section/add', method=['POST'])
def callback(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.add_to_config(haproxy_id)


@route('/haproxy/<haproxy_id>/section/edit', method=['POST'])
@route('/haproxy/<haproxy_id:int>/section/edit', method=['POST'])
def callback(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.edit_section(haproxy_id)


@route('/haproxy/<haproxy_id>/acl', method=['POST'])
def add_acl(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.add_acl(haproxy_id)


@route('/haproxy/<haproxy_id>/acl', method=['DELETE'])
def add_acl(haproxy_id):
	if not check_login(required_service=1):
		return dict(error=_error_auth)
	return api_funct.del_acl(haproxy_id)


@route('/<service>/<server_id>', method=['GET'])
@route('/<service>/<server_id:int>', method=['GET'])
def callback(server_id, service):
	required_service = api_funct.return_requred_serivce(service)
	if not check_login(required_service=required_service):
		return dict(error=_error_auth)
	return api_funct.get_server(server_id, service)


@route('/<service>/<server_id>/status', method=['GET'])
@route('/<service>/<server_id:int>/status', method=['GET'])
def callback(server_id, service):
	required_service = api_funct.return_requred_serivce(service)
	if not check_login(required_service=required_service):
		return dict(error=_error_auth)
	return api_funct.get_status(server_id, service)


@route('/<service>/<server_id>/action/<action:re:[a-z]+>', method=['GET'])
@route('/<service>/<server_id:int>/action/<action:re:[a-z]+>', method=['GET'])
def callback(server_id, action, service):
	required_service = api_funct.return_requred_serivce(service)
	if not check_login(required_service=required_service):
		return dict(error=_error_auth)
	return api_funct.actions(server_id, action, service)


@route('/<service>/<server_id>/config', method=['GET'])
@route('/<service>/<server_id:int>/config', method=['GET'])
def callback(server_id, service):
	required_service = api_funct.return_requred_serivce(service)
	if not check_login(required_service=required_service):
		return dict(error=_error_auth)
	config_path = request.headers.get('config-file')
	return api_funct.get_config(server_id, service=service, config_path=config_path)


@route('/<service>/<server_id>/config', method=['POST'])
@route('/<service>/<server_id:int>/config', method=['POST'])
def callback(server_id, service):
	required_service = api_funct.return_requred_serivce(service)
	if not check_login(required_service=required_service):
		return dict(error=_error_auth)
	config_path = request.headers.get('config-file')
	return api_funct.upload_config(server_id, service=service, config_path=config_path)


if __name__ == '__main__':
	print(sys.path)
	port = int(os.environ.get('PORT', 8080))
	run(host='0.0.0.0', port=port, debug=True)
