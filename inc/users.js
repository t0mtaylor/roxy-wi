var awesome = "/inc/fontawesome.min.js"

$( function() {
	$( "#backup_tabs" ).tabs();
	$( "#interface" ).autocomplete({
		source: function( request, response ) {
			$.ajax( {
				url: "options.py",
				data: {
					showif:1,
					serv: $("#master").val(),
					token: $('#token').val()
				},
				success: function( data ) {
					data = data.replace(/\s+/g,' ');
					if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
						toastr.error(data);
					} else {
						response(data.split(" "));
					}
				}
			} );
		},
		autoFocus: true,
		minLength: -1
	});
	$( "#interface-add" ).autocomplete({
		source: function( request, response ) {
			$.ajax( {
				url: "options.py",
				data: {
					showif:1,
					serv: $("#master-add").val(),
					token: $('#token').val()
				},
				success: function( data ) {
					data = data.replace(/\s+/g,' ');
					if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
						toastr.error(data);
					} else {
						response(data.split(" "));
					}
				}
			} );
		},
		autoFocus: true,
		minLength: -1
	});
	$('#install').click(function() {
		$("#ajax").html('')
		var syn_flood = 0;
		var docker = 0;
		if ($('#syn_flood').is(':checked')) {
			syn_flood = '1';
		}
		if ($('#haproxy_docker').is(':checked')) {
			docker = '1';
		}
		if ($('#haproxyaddserv').val() == '------' || $('#haproxyaddserv').val() === null) {
			toastr.warning('Select a server');
			return false
		}
		$("#ajax").html(wait_mess);
		$.ajax( {
			url: "options.py",
			data: {
				haproxyaddserv: $('#haproxyaddserv').val(),
				syn_flood: syn_flood,
				hapver: $('#hapver option:selected' ).val(),
				docker: docker,
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
			data = data.replace(/\s+/g,' ');
				$("#ajax").html('')
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1') {
					toastr.error(data);
				} else if (data.indexOf('success') != '-1' ){
					toastr.remove();
					toastr.success(data);
					$( "#haproxyaddserv" ).trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.remove();
					toastr.info(data);
				} else {
					toastr.remove();
					toastr.info(data);
				}
			}
		} );
	});
	$('#nginx_install').click(function() {
		$("#ajax").html('')
		var syn_flood = 0;
		var docker = 0;
		if ($('#nginx_syn_flood').is(':checked')) {
			syn_flood = '1';
		}
		if ($('#nginx_docker').is(':checked')) {
			docker = '1';
		}
		if ($('#nginxaddserv').val() == '------') {
			toastr.warning('Select a server');
			return false
		}
		$("#ajax").html(wait_mess);
		$.ajax( {
			url: "options.py",
			data: {
				install_nginx: $('#nginxaddserv').val(),
				syn_flood: syn_flood,
				docker: docker,
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				$("#ajax").html('')
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if (data.indexOf('success') != '-1' ){
					toastr.clear();
					toastr.success(data);
					$("#nginxaddserv").trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$('#grafna_install').click(function() {
		$("#ajaxmon").html('');
		$("#ajaxmon").html(wait_mess);
		$.ajax( {
			url: "options.py",
			data: {
				install_grafana: '1',
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
			data = data.replace(/\s+/g,' ');
				$("#ajaxmon").html('');
				if (data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1' || data.indexOf('ERROR') != '-1') {
					toastr.clear();
					toastr.error(data);;
				} else if (data.indexOf('success') != '-1' ){
					toastr.clear();
					toastr.success(data);
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$('#haproxy_exp_install').click(function() {
		$("#ajaxmon").html('')
		$("#ajaxmon").html(wait_mess);
		var ext_prom = 0;
		if ($('#haproxy_ext_prom').is(':checked')) {
			ext_prom = '1';
		}
		$.ajax( {
			url: "options.py",
			data: {
				haproxy_exp_install: $('#haproxy_exp_addserv').val(),
				exporter_v: $('#hapexpver').val(),
				ext_prom: ext_prom,
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
			data = data.replace(/\s+/g,' ');
				$("#ajaxmon").html('');
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if (data.indexOf('success') != '-1' ){
					toastr.clear();
					toastr.success(data);
					$('#cur_haproxy_exp_ver').text('HAProxy exporter is installed');
					$("#haproxy_exp_addserv").trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$('#nginx_exp_install').click(function() {
		$("#ajaxmon").html('')
		$("#ajaxmon").html(wait_mess);
		var ext_prom = 0;
		if ($('#nginx_ext_prom').is(':checked')) {
			ext_prom = '1';
		}
		$.ajax( {
			url: "options.py",
			data: {
				nginx_exp_install: $('#nginx_exp_addserv').val(),
				exporter_v: $('#nginxexpver').val(),
				ext_prom: ext_prom,
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
			data = data.replace(/\s+/g,' ');
				$("#ajaxmon").html('');
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1') {
					toastr.error(data);
				} else if (data.indexOf('success') != '-1' ){
					toastr.clear();
					toastr.success(data);
					$('#cur_nginx_exp_ver').text('Nginx exporter is installed');
					$("#nginx_exp_addserv").trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$('#node_exp_install').click(function() {
		$("#ajaxmon").html('')
		$("#ajaxmon").html(wait_mess);
		var ext_prom = 0;
		if ($('#node_ext_prom').is(':checked')) {
			ext_prom = '1';
		}
		$.ajax( {
			url: "options.py",
			data: {
				node_exp_install: $('#node_exp_addserv').val(),
				exporter_v: $('#nodeexpver').val(),
				ext_prom: ext_prom,
				token: $('#token').val()
				},
			type: "POST",
			success: function( data ) {
			data = data.replace(/\s+/g,' ');
				$("#ajaxmon").html('');
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1' || data.indexOf('UNREACHABLE') != '-1') {
					toastr.error(data);
				} else if (data.indexOf('success') != '-1' ){
					toastr.clear();
					toastr.success(data);
					$('#cur_node_exp_ver').text('Node exporter is installed');
					$("#node_exp_addserv").trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$( "#haproxyaddserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				get_hap_v: 1,
				serv: $('#haproxyaddserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if(data != '') {
					data = data+'-1';
					$('#cur_hap_ver').text(data);
					$('#cur_hap_ver').css('font-weight', 'bold');
					$('#install').text('Update');
					$('#install').attr('title', 'Update HAProxy');
				} else {
					$('#cur_hap_ver').text('HAProxy has not installed');
					$('#install').text('Install');
					$('#install').attr('title', 'Install HAProxy');
				}
			}
		} );
	});
	$( "#nginxaddserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				get_nginx_v: 1,
				serv: $('#nginxaddserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if(data.indexOf('bash') != '-1' || data.indexOf('such') != '-1' || data.indexOf('command not found') != '-1') {
					$('#cur_nginx_ver').text('Nginx has not installed');
					$('#nginx_install').text('Install');
					$('#nginx_install').attr('title', 'Install Nginx');
				} else {
					$('#cur_nginx_ver').text(data);
					$('#cur_nginx_ver').css('font-weight', 'bold');
					$('#nginx_install').text('Update');
					$('#nginx_install').attr('title', 'Update Nginx');
				}
			}
		} );
	});
	$( "#haproxy_exp_addserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				get_exporter_v: 'haproxy_exporter',
				serv: $('#haproxy_exp_addserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if (data.indexOf('error:') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if(data == 'no' || data == '') {
					$('#cur_haproxy_exp_ver').text('HAProxy exporter has been not installed');
				} else {
					$('#cur_haproxy_exp_ver').text(data);
					$('#cur_haproxy_exp_ver').css('font-weight', 'bold');
				}
			}
		} );
	});
	$( "#nginx_exp_addserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				get_exporter_v: 'nginx_exporter',
				serv: $('#nginx_exp_addserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if (data.indexOf('error:') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if(data == 'no' || data == '') {
					$('#cur_nginx_exp_ver').text('Nginx exporter has not been installed');
				} else {
					$('#cur_nginx_exp_ver').text(data);
					$('#cur_nginx_exp_ver').css('font-weight', 'bold');
				}
			}
		} );
	});
	$( "#node_exp_addserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				get_exporter_v: 'node_exporter',
				serv: $('#node_exp_addserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if (data.indexOf('error:') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if(data == 'no' || data.indexOf('command') != '-1' || data == '') {
					$('#cur_node_exp_ver').text('Node exporter has not been installed');
				} else {
					$('#cur_node_exp_ver').text(data);
					$('#cur_node_exp_ver').css('font-weight', 'bold');
				}
			}
		} );
	});
	$('#add-group-button').click(function() {
		addGroupDialog.dialog('open');
	});
	var addGroupDialog = $( "#group-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Add a new group",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function() {
				addGroup(this);
			},
			Cancel: function() {
				$( this ).dialog( "close" );
				clearTips();
			}
		}
	});
	$('#add-user-button').click(function() {
		addUserDialog.dialog('open');
	});
	var addUserDialog = $( "#user-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Add a new user",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addUser(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#add-server-button').click(function() {
		addServerDialog.dialog('open');
	});
	var addServerDialog = $( "#server-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Add a new server",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addServer(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#add-ssh-button').click(function() {
		addCredsDialog.dialog('open');
	});
	var addCredsDialog = $( "#ssh-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Add a new SSH credentials",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addCreds(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#add-telegram-button').click(function() {
		addTelegramDialog.dialog('open');
	});
	$('#add-slack-button').click(function() {
		addSlackDialog.dialog('open');
	});
	var addTelegramDialog = $( "#telegram-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Create a new Telegram channel",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addTelegram(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	var addSlackDialog = $( "#slack-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Create a new Slack channel",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addSlack(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#add-backup-button').click(function() {
		addBackupDialog.dialog('open');
	});
	var addBackupDialog = $( "#backup-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Create a new backup job",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addBackup(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#add-git-button').click(function() {
		addGitDialog.dialog('open');
	});
	var addGitDialog = $( "#git-add-table" ).dialog({
		autoOpen: false,
		resizable: false,
		height: "auto",
		width: 600,
		modal: true,
		title: "Create a new git job",
		show: {
			effect: "fade",
			duration: 200
		},
		hide: {
			effect: "fade",
			duration: 200
		},
		buttons: {
			"Add": function () {
				addGit(this);
			},
			Cancel: function () {
				$(this).dialog("close");
				clearTips();
			}
		}
	});
	$('#git-init').click(function() {
		if ($('#git-init').is(':checked')) {
			$('.git-init-params').show();
		} else {
			$('.git-init-params').hide();
		}
	});
	$( "#ajax-users input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateUser(id[1])
	});
	$( "#ajax-users select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateUser(id[1])
	});
	$( "#ajax-group input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateGroup(id[1])
	});
	$( "#ajax-servers input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateServer(id[1])
	});
	$( "#ajax-servers select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateServer(id[1])
	});
	$( "#ssh_enable_table input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateSSH(id[1])
		sshKeyEnableShow(id[1])
	});
	$( "#ssh_enable_table select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateSSH(id[1])
		sshKeyEnableShow(id[1])
	});
	$( "#settings input" ).change(function() {
		var id = $(this).attr('id');
		var val = $(this).val();
		updateSettings(id, val);
	});
	$('#new-ssh_enable').click(function() {
		if ($('#new-ssh_enable').is(':checked')) {
			$('#ssh_pass').css('display', 'none');
		} else {
			$('#ssh_pass').css('display', 'block');
		}
	});
	if ($('#new-ssh_enable').is(':checked')) {
		$('#ssh_pass').css('display', 'none');
	} else {
		$('#ssh_pass').css('display', 'block');
	}
   $( "#checker_table input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateTelegram(id[2])
	});
	$( "#checker_table select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateTelegram(id[1])
	});
   $( "#checker_slack_table input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateSlack(id[2])
	});
	$( "#checker_slack_table select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateSlack(id[1])
	});
	$( "#ajax-backup-table input" ).change(function() {
		var id = $(this).attr('id').split('-');
		updateBackup(id[2])
	});
	$( "#ajax-backup-table select" ).on('selectmenuchange',function() {
		var id = $(this).attr('id').split('-');
		updateBackup(id[2])
	});
	$( "#scan_server" ).change(function() {
		if ($('#scan_server').is(':checked')) {
			$('.services_for_scan').hide();
		} else {
			$('.services_for_scan').show();
		}
	});
	$('#search_ldap_user').click(function() {
		var valid = true;
		toastr.clear();
		allFields = $( [] ).add( $('#new-username') );
		allFields.removeClass( "ui-state-error" );
		valid = valid && checkLength( $('#new-username'), "user name", 1 );
		user = $('#new-username').val()
		if (valid) {
			$.ajax( {
				url: "options.py",
				data: {
					get_ldap_email: $('#new-username').val(),
					token: $('#token').val()
				},
				type: "POST",
				success: function( data ) {
					data = data.replace(/\s+/g,' ');
					if (data.indexOf('error:') != '-1') {
						toastr.error(data);
						$('#new-email').val('');
						$('#new-password').attr('readonly', false);
						$('#new-password').val('');
					} else {
						var json = $.parseJSON(data);
						toastr.clear();
						$('#new-email').val(json[0]);
						$('#new-username').val(user+'@'+json[1]);
						$('#new-password').val('aduser');
						$('#new-password').attr('readonly', true);
					}
				}
			} );
			clearTips();
		}
	});
	$('#show_country_codes').click(function() {
		$('#hide_country_codes').show();
		$('#geoip_country_codes').show();
		$('#show_country_codes').hide();
	});
	$('#hide_country_codes').click(function() {
		$('#show_country_codes').show();
		$('#geoip_country_codes').hide();
		$('#hide_country_codes').hide();
	});
	$( "#geoipserv" ).on('selectmenuchange',function() {
		$.ajax( {
			url: "options.py",
			data: {
				geoipserv: $('#geoipserv option:selected').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				if(data.indexOf('No such file or directory') != '-1') {
					$('#cur_geoip').text('GeoLite2 has not installed');
					$('#geoip_install').show();
				} else {
					$('#cur_geoip').text('GeoLite2 has already installed');
					$('#geoip_install').hide();
				}
			}
		} );
	});
	$( "#geoip_install" ).click(function() {
		var updating_geoip = 0;
		if ($('#updating_geoip').is(':checked')) {
			updating_geoip = '1';
		}
		$("#ajax-geoip").html(wait_mess);
		$.ajax( {
			url: "options.py",
			data: {
				geoip_install: $('#geoipserv option:selected').val(),
				geoip_update: updating_geoip,
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/^\s+|\s+$/g,'');
				$("#ajax-geoip").html('')
				if (data.indexOf('error:') != '-1' || data.indexOf('FAILED') != '-1') {
					toastr.clear();
					toastr.error(data);
				} else if (data.indexOf('success:') != '-1' ){
					toastr.clear();
					toastr.success(data);
					$( "#geoipserv" ).trigger( "selectmenuchange" );
				} else if (data.indexOf('Info') != '-1' ){
					toastr.clear();
					toastr.info(data);
				} else {
					toastr.clear();
					toastr.info(data);
				}
			}
		} );
	});
	$("#tabs ul li").click(function() {
		var activeTab = $(this).find("a").attr("href");

		if (activeTab == '#services') {
			loadServices();
		} else if (activeTab == '#updatehapwi') {
			loadupdatehapwi();
		} else if (activeTab == '#checker'){
			loadchecker();
		} else if (activeTab == '#openvpn'){
			loadopenvpn();
		}
	});
	$('#nginx-section-head').click(function () {
		hideAndShowSettings('nginx');
	});
	$('#main-section-head').click(function () {
		hideAndShowSettings('main');
	});
	$('#monitoring-section-head').click(function () {
		hideAndShowSettings('monitoring');
	});
	$('#haproxy-section-head').click(function () {
		hideAndShowSettings('haproxy');
	});
	$('#ldap-section-head').click(function () {
		hideAndShowSettings('ldap');
	});
	$('#logs-section-head').click(function () {
		hideAndShowSettings('logs');
	});
	$('#rabbitmq-section-head').click(function () {
		hideAndShowSettings('rabbitmq');
	});
	$('#apache-section-head').click(function () {
		hideAndShowSettings('apache');
	});
} );
function hideAndShowSettings(section) {
	var ElemId = $('#' + section + '-section-h3');
	if(ElemId.attr('class') == 'plus-after') {
		$('.' + section + '-section').show();
		ElemId.removeClass('plus-after');
		ElemId.addClass('minus-after');
		$.getScript(awesome);
	} else {
		$('.' + section + '-section').hide();
		ElemId.removeClass('minus-after');
		ElemId.addClass('plus-after');
		$.getScript(awesome);
	}
}
window.onload = function() {
	$('#tabs').tabs();
	var activeTabIdx = $('#tabs').tabs('option','active')
	if (cur_url[0].split('#')[0] == 'users.py') {
		if (activeTabIdx == 7) {
			loadServices();
		} else if (activeTabIdx == 8) {
			loadupdatehapwi();
		} else if (activeTabIdx == 4) {
			loadchecker();
		} else if (activeTabIdx == 5) {
			loadopenvpn();
		}
	} else if (cur_url[0].split('#')[0] == 'servers.py') {
		if (activeTabIdx == 3) {
			loadchecker();
		}
	}
}
function common_ajax_action_after_success(dialog_id, new_group, ajax_append_id, data) {
	toastr.clear();
	$("#"+ajax_append_id).append(data);
	$( "."+new_group ).addClass( "update", 1000);
	$.getScript(awesome);
	clearTips();
	$( dialog_id ).dialog("close" );
	setTimeout(function() {
		$( "."+new_group ).removeClass( "update" );
	}, 2500 );
}
function addUser(dialog_id) {
	var valid = true;
	toastr.clear();
	allFields = $( [] ).add( $('#new-username') ).add( $('#new-password') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#new-username'), "user name", 1 );
	valid = valid && checkLength( $('#new-password'), "password", 1 );
	var activeuser = 0;
	if ($('#activeuser').is(':checked')) {
		activeuser = '1';
	}
	if (valid) {
		$.ajax( {
			url: "options.py",
			data: {
				newuser: "1",
				newusername: $('#new-username').val(),
				newpassword: $('#new-password').val(),
				newemail: $('#new-email').val(),
				newrole: $('#new-role').val(),
				activeuser: activeuser,
				page: cur_url[0].split('#')[0],
				newgroupuser: $('#new-group').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					var getId = new RegExp('[0-9]+');
					var id = data.match(getId);
					addUserGroup(id[0]);
					common_ajax_action_after_success(dialog_id, 'user-'+id, 'ajax-users', data);
				}
			}
		} );
	}
}
function addGroup(dialog_id) {
	toastr.clear();
	var valid = true;
	allFields = $( [] ).add( $('#new-group-add') );
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#new-group-add'), "new group name", 1 );
	if(valid) {
		$.ajax( {
			url: "options.py",
			data: {
				newgroup: "1",
				groupname: $('#new-group-add').val(),
				newdesc: $('#new-desc').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					var getId = new RegExp('[0-9]+');
					var id = data.match(getId);
					$('select:regex(id, group)').append('<option value='+id+'>'+$('#new-group-add').val()+'</option>').selectmenu("refresh");
					common_ajax_action_after_success(dialog_id, 'newgroup', 'ajax-group', data);
				}
			}
		} );
	}
}
function addServer(dialog_id) {
	toastr.clear()
	var valid = true;
	var servername = $('#new-server-add').val();
	var newip = $('#new-ip').val();
	var newservergroup = $('#new-server-group-add').val();
	var cred = $('#credentials').val();
	var scan_server = 0;
	var typeip = 0;
	var enable = 0;
	var haproxy = 0;
	var nginx = 0;
	var apache = 0;
	var firewall = 0;
	if ($('#scan_server').is(':checked')) {
		scan_server = '1';
	}
	if ($('#typeip').is(':checked')) {
		typeip = '1';
	}
	if ($('#enable').is(':checked')) {
		enable = '1';
	}
	if ($('#haproxy').is(':checked')) {
		haproxy = '1';
	}
	if ($('#nginx').is(':checked')) {
		nginx = '1';
	}
	if ($('#apache').is(':checked')) {
		apache = '1';
	}
	if ($('#firewall').is(':checked')) {
		firewall = '1';
	}
	allFields = $( [] ).add( $('#new-server-add') ).add( $('#new-ip') ).add( $('#new-port') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#new-server-add'), "Hostname", 1 );
	valid = valid && checkLength( $('#new-ip'), "IP", 1 );
	valid = valid && checkLength( $('#new-port'), "Port", 1 );
	console.log(cred)
	if (cred == null) {
		toastr.error('First select credentials');
		return false;
	}
	if (newservergroup == null) {
		toastr.error('First select a group');
		return false;
	}
	if (valid) {
		$.ajax( {
			url: "options.py",
			data: {
				newserver: "1",
				servername: servername,
				newip: newip,
				newport: $('#new-port').val(),
				newservergroup: newservergroup,
				scan_server: scan_server,
				typeip: typeip,
				haproxy: haproxy,
				nginx: nginx,
				apache: apache,
				firewall: firewall,
				enable: enable,
				slave: $('#slavefor' ).val(),
				cred: cred,
				page: cur_url[0].split('#')[0],
				desc: $('#desc').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					common_ajax_action_after_success(dialog_id, 'newserver', 'ajax-servers', data);
					$( "input[type=submit], button" ).button();
					$( "input[type=checkbox]" ).checkboxradio();
					$( ".controlgroup" ).controlgroup();
					$( "select" ).selectmenu();
					var getId = new RegExp('server-[0-9]+');
					var id = data.match(getId) + '';
					id = id.split('-').pop();
					$('select:regex(id, git-server)').append('<option value=' + id + '>' + $('#hostname-'+id).val() + '</option>').selectmenu("refresh");
					$('select:regex(id, backup-server)').append('<option value=' + $('#ip-'+id).text() + '>' + $('#hostname-'+id).val() + '</option>').selectmenu("refresh");
					$('select:regex(id, haproxy_exp_addserv)').append('<option value=' + $('#ip-'+id).text() + '>' + $('#hostname-'+id).val() + '</option>').selectmenu("refresh");
					$('select:regex(id, nginx_exp_addserv)').append('<option value=' + $('#ip-'+id).text() + '>' + $('#hostname-'+id).val() + '</option>').selectmenu("refresh");
					$('select:regex(id, node_exp_addserv)').append('<option value=' + $('#ip-'+id).text() + '>' + $('#hostname-'+id).val() + '</option>').selectmenu("refresh");
				}
			}
		} );
	}
}
function addCreds(dialog_id) {
	toastr.clear();
	var ssh_enable = 0;
	if ($('#new-ssh_enable').is(':checked')) {
		ssh_enable = '1';
	}
	var valid = true;
	allFields = $( [] ).add( $('#new-ssh-add') ).add( $('#ssh_user') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#new-ssh-add'), "Name", 1 );
	valid = valid && checkLength( $('#ssh_user'), "Credentials", 1 );
	if(valid) {
		$.ajax({
			url: "options.py",
			data: {
				new_ssh: $('#new-ssh-add').val(),
				new_group: $('#new-sshgroup').val(),
				ssh_user: $('#ssh_user').val(),
				ssh_pass: $('#ssh_pass').val(),
				ssh_enable: ssh_enable,
				page: cur_url[0].split('#')[0],
				token: $('#token').val()
			},
			type: "POST",
			success: function (data) {
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					var group_name = getGroupNameById($('#new-sshgroup').val());
					var getId = new RegExp('ssh-table-[0-9]+');
					var id = data.match(getId) + '';
					id = id.split('-').pop();
					common_ajax_action_after_success(dialog_id, 'ssh-table-'+id, 'ssh_enable_table', data);
					$('select:regex(id, credentials)').append('<option value=' + id + '>' + $('#new-ssh-add').val() + '</option>').selectmenu("refresh");
					$('select:regex(id, ssh-key-name)').append('<option value=' + $('#new-ssh-add').val() + '_'+group_name+'>' + $('#new-ssh-add').val() + '_'+group_name+'</option>').selectmenu("refresh");
					$("input[type=submit], button").button();
					$("input[type=checkbox]").checkboxradio();
					$("select").selectmenu();
				}
			}
		});
	}
}
function getGroupNameById(group_id) {
	var group_name = ''
	$.ajax({
		url: "options.py",
		async: false,
		data: {
			get_group_name_by_id: group_id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			if (data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				group_name = data;
			}
		}
	});
	return group_name;
}
function addTelegram(dialog_id) {
	var valid = true;
	toastr.clear();
	allFields = $( [] ).add( $('#telegram-token-add') ).add( $('#telegram-chanel-add') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#telegram-token-add'), "token", 1 );
	valid = valid && checkLength( $('#telegram-chanel-add'), "channel name", 1 );
	if(valid) {
		toastr.clear();
		$.ajax( {
			url: "options.py",
			data: {
				newtelegram: $('#telegram-token-add').val(),
				chanel: $('#telegram-chanel-add').val(),
				telegramgroup: $('#new-telegram-group-add').val(),
				page: cur_url[0].split('#')[0],
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					common_ajax_action_after_success(dialog_id, 'newgroup', 'checker_table', data);
					$( "input[type=submit], button" ).button();
					$( "input[type=checkbox]" ).checkboxradio();
					$( "select" ).selectmenu();
				}
			}
		} );
	}
}
function addSlack(dialog_id) {
	var valid = true;
	toastr.clear();
	allFields = $( [] ).add( $('#slack-token-add') ).add( $('#slack-chanel-add') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#slack-token-add'), "token", 1 );
	valid = valid && checkLength( $('#slack-chanel-add'), "channel name", 1 );
	if(valid) {
		toastr.clear();
		$.ajax( {
			url: "options.py",
			data: {
				newslack: $('#slack-token-add').val(),
				chanel: $('#slack-chanel-add').val(),
				slackgroup: $('#new-slack-group-add').val(),
				page: cur_url[0].split('#')[0],
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					common_ajax_action_after_success(dialog_id, 'newgroup', 'checker_slack_table', data);
					$( "input[type=submit], button" ).button();
					$( "input[type=checkbox]" ).checkboxradio();
					$( "select" ).selectmenu();
				}
			}
		} );
	}
}
function addBackup(dialog_id) {
	var valid = true;
	toastr.clear();
	allFields = $( [] ).add( $('#backup-server') ).add( $('#rserver') ).add( $('#rpath') ).add( $('#backup-time') ).add( $('#backup-credentials') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#backup-server'), "backup server ", 1 );
	valid = valid && checkLength( $('#rserver'), "remote server", 1 );
	valid = valid && checkLength( $('#rpath'), "remote path", 1 );
	valid = valid && checkLength( $('#backup-time'), "backup time", 1 );
	valid = valid && checkLength( $('#backup-credentials'), "backup credentials", 1 );
	if (valid) {
		$.ajax( {
			url: "options.py",
			data: {
				backup: '1',
				server: $('#backup-server').val(),
				rserver: $('#rserver').val(),
				rpath: $('#rpath').val(),
				type: $('#backup-type').val(),
				time: $('#backup-time').val(),
				cred: $('#backup-credentials').val(),
				description: $('#backup-description').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else if (data.indexOf('success: ') != '-1') {
					common_ajax_action_after_success(dialog_id, 'newbackup', 'ajax-backup-table', data);
					$( "select" ).selectmenu();
				} else if (data.indexOf('info: ') != '-1') {
					toastr.clear();
					toastr.info(data);
				} else if (data.indexOf('warning: ') != '-1') {
					toastr.clear();
					toastr.warning(data);
				}
			}
		} );
	}
}
function addGit(dialog_id) {
	var valid = true;
	toastr.clear();
	allFields = $( [] ).add( $('#git-server') ).add( $('#git-service') ).add( $('#git-time')).add( $('#git-credentials') ).add( $('#git-branch') )
	allFields.removeClass( "ui-state-error" );
	valid = valid && checkLength( $('#git-server'), "Server ", 1 );
	valid = valid && checkLength( $('#git-service'), "Service", 1 );
	valid = valid && checkLength( $('#git-credentials'), "Credentials", 1 );
	valid = valid && checkLength( $('#git-branch'), "Branch name", 1 );
	var git_init = 0;
	if ($('#git-init').is(':checked')) {
			git_init = '1';
		}
	if (valid) {
		$.ajax( {
			url: "options.py",
			data: {
				git_backup: '1',
				server: $('#git-server').val(),
				git_service: $('#git-service').val(),
				git_init: git_init,
				git_repo: $('#git-repo').val(),
				git_branch: $('#git-branch').val(),
				time: $('#git-time').val(),
				cred: $('#git-credentials').val(),
				description: $('#git-description').val(),
				git_deljob: 0,
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else if (data.indexOf('success: ') != '-1') {
					common_ajax_action_after_success(dialog_id, 'newgit', 'ajax-git-table', data);
					$( "select" ).selectmenu();
				} else if (data.indexOf('info: ') != '-1') {
					toastr.clear();
					toastr.info(data);
				} else if (data.indexOf('warning: ') != '-1') {
					toastr.clear();
					toastr.warning(data);
				}
			}
		} );
	}
}
function updateSettings(param, val) {
	toastr.clear();
	$.ajax( {
		url: "options.py",
		data: {
			updatesettings: param,
			val: val,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#"+param).parent().parent().addClass( "update", 1000 );
			setTimeout(function() {
				$( "#"+param ).parent().parent().removeClass( "update" );
			}, 2500 );
			}
		}
	} );
}
function sshKeyEnableShow(id) {
	$('#ssh_enable-'+id).click(function() {
		if ($('#ssh_enable-'+id).is(':checked')) {
			$('#ssh_pass-'+id).css('display', 'none');
		} else {
			$('#ssh_pass-'+id).css('display', 'block');
		}
	});
	if ($('#ssh_enable-'+id).is(':checked')) {
		$('#ssh_pass-'+id).css('display', 'none');
	} else {
		$('#ssh_pass-'+id).css('display', 'block');
	}
}

function confirmDeleteUser(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#login-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeUser(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteGroup(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#name-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeGroup(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteServer(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#hostname-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeServer(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteSsh(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#ssh_name-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeSsh(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteTelegram(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#telegram-chanel-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeTelegram(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteSlack(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete " +$('#slack-chanel-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeSlack(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteBackup(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete job for " +$('#backup-server-'+id).val() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeBackup(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function confirmDeleteGit(id) {
	 $( "#dialog-confirm" ).dialog({
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
	  title: "Are you sure you want to delete job for " +$('#git-server-'+id).text() + "?",
      buttons: {
        "Delete": function() {
			$( this ).dialog( "close" );
			removeGit(id);
        },
        Cancel: function() {
			$( this ).dialog( "close" );
        }
      }
    });
}
function cloneServer(id) {
	$( "#add-server-button" ).trigger( "click" );
	if ($('#enable-'+id).is(':checked')) {
		$('#enable').prop('checked', true)
	} else {
		$('#enable').prop('checked', false)
	}
	if ($('#typeip-'+id).is(':checked')) {
		$('#typeip').prop('checked', true)
	} else {
		$('#typeip').prop('checked', false)
	}
	if ($('#haproxy-'+id).is(':checked')) {
		$('#haproxy').prop('checked', true)
	} else {
		$('#haproxy').prop('checked', false)
	}
	if ($('#nginx-'+id).is(':checked')) {
		$('#nginx').prop('checked', true)
	} else {
		$('#nginx').prop('checked', false)
	}
	$('#enable').checkboxradio("refresh");
	$('#typeip').checkboxradio("refresh");
	$('#haproxy').checkboxradio("refresh");
	$('#nginx').checkboxradio("refresh");
	$('#new-server-add').val($('#hostname-'+id).val())
	$('#new-ip').val($('#ip-'+id).val())
	$('#new-port').val($('#port-'+id).val())
	$('#desc').val($('#desc-'+id).val())
	$('#slavefor').val($('#slavefor-'+id+' option:selected').val()).change()
	$('#slavefor').selectmenu("refresh");
	$('#credentials').val($('#credentials-'+id+' option:selected').val()).change()
	$('#credentials').selectmenu("refresh");
	cur_url = cur_url[0].split('#')[0]
	if (cur_url == 'users.py') {
		$('#new-server-group-add').val($('#servergroup-'+id+' option:selected').val()).change()
		$('#new-server-group-add').selectmenu("refresh");
	}
}
function cloneUser(id) {
	$( "#add-user-button" ).trigger( "click" );
	if ($('#activeuser-'+id).is(':checked')) {
		$('#activeuser').prop('checked', true)
	} else {
		$('#activeuser').prop('checked', false)
	}
	$('#activeuser').checkboxradio("refresh");
	$('#new-role').val($('#role-'+id+' option:selected').val()).change()
	$('#new-role').selectmenu("refresh");
	cur_url = cur_url[0].split('#')[0]
	if (cur_url == 'users.py') {
		$('#new-group').val($('#usergroup-'+id+' option:selected').val()).change();
		$('#new-group').selectmenu("refresh");
	}
}
function cloneTelegram(id) {
	$( "#add-telegram-button" ).trigger( "click" );
	$('#telegram-token-add').val($('#telegram-token-'+id).val())
	$('#telegram-chanel-add').val($('#telegram-chanel-'+id).val())
}
function cloneSlack(id) {
	$( "#slack" ).trigger( "click" );
	$('#slack').val($('#slack-token-'+id).val())
	$('#slack').val($('#slack-chanel-'+id).val())
}
function cloneBackup(id) {
	$( "#add-backup-button" ).trigger( "click" );
	$('#rserver').val($('#backup-rserver-'+id).val())
	$('#rpath').val($('#backup-rpath-'+id).val())
	$('#backup-type').val($('#backup-type-'+id+' option:selected').val()).change()
	$('#backup-type').selectmenu("refresh");
	$('#backup-time').val($('#backup-time-'+id+' option:selected').val()).change()
	$('#backup-time').selectmenu("refresh");
	$('#backup-credentials').val($('#backup-credentials-'+id+' option:selected').val()).change()
	$('#backup-credentials').selectmenu("refresh");
}
function removeUser(id) {
	$("#user-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			userdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#user-"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeServer(id) {
	$("#server-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			serverdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#server-"+id).remove();
			} else if (data.indexOf('error: ') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else if (data.indexOf('warning: ') != '-1') {
				toastr.clear();
				toastr.warning(data);
			}
		}
	} );
}
function removeGroup(id) {
	$("#group-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			groupdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#group-"+id).remove();
				$('select:regex(id, group) option[value='+id+']').remove();
				$('select:regex(id, group)').selectmenu("refresh");
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeSsh(id) {
	$("#ssh-table-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			sshdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#ssh-table-"+id).remove();
				$('select:regex(id, credentials) option[value='+id+']').remove();
				$('select:regex(id, credentials)').selectmenu("refresh");
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeTelegram(id) {
	$("#telegram-table-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			telegramdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#telegram-table-"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeSlack(id) {
	$("#slack-table-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			slackdel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#slack-table-"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeBackup(id) {
	$("#backup-table-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			deljob: id,
			cred: $('#backup-credentials-'+id).val(),
			server: $('#backup-server-'+id).text(),
			rserver: $('#backup-rserver-'+id).val(),
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data.indexOf('Ok') != '-1') {
				$("#backup-table-"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function removeGit(id) {
	$("#git-table-"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			git_backup: id,
			git_deljob: 1,
			git_init: 0,
			repo: 0,
			branch: 0,
			time: 0,
			cred: $('#git-credentials-id-'+id).text(),
			server: $('#git-server-id-'+id).text(),
			git_service: $('#git-service-id-'+id).text(),
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data.indexOf('Ok') != '-1') {
				$("#git-table-"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function updateUser(id) {
	toastr.remove();
	cur_url[0] = cur_url[0].split('#')[0]
	var usergroup = Cookies.get('group');
	var role = $('#role-'+id).val();
	var activeuser = 0;
	if ($('#activeuser-'+id).is(':checked')) {
		activeuser = '1';
	}
	if (role == null){
		toastr.warning('Please edit this user only on the Admin area');
		return false;
	}
	toastr.remove();
	$.ajax( {
		url: "options.py",
		data: {
			updateuser: $('#login-'+id).val(),
			email: $('#email-'+id).val(),
			role: role,
			usergroup: usergroup,
			activeuser: activeuser,
			id: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.remove();
				$("#user-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#user-"+id ).removeClass( "update" );
				}, 2500 );
			}
		}
	} );
}
function updateGroup(id) {
	toastr.clear();
	$.ajax( {
		url: "options.py",
		data: {
			updategroup: $('#name-'+id).val(),
			descript: $('#descript-'+id).val(),
			id: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#group-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#group-"+id ).removeClass( "update" );
				}, 2500 );
				$('select:regex(id, group) option[value='+id+']').remove();
				$('select:regex(id, group)').append('<option value='+id+'>'+$('#name-'+id).val()+'</option>').selectmenu("refresh");
			}
		}
	} );
}
function updateServer(id) {
	toastr.clear();
	let typeip = 0;
	let enable = 0;
	let haproxy = 0;
	let nginx = 0;
	let apache = 0;
	let firewall = 0;
	let protected_serv = 0;
	if ($('#typeip-'+id).is(':checked')) {
		typeip = '1';
	}
	if ($('#haproxy-'+id).is(':checked')) {
		haproxy = '1';
	}
	if ($('#nginx-'+id).is(':checked')) {
		nginx = '1';
	}
	if ($('#apache-'+id).is(':checked')) {
		apache = '1';
	}
	if ($('#enable-'+id).is(':checked')) {
		enable = '1';
	}
	if ($('#firewall-'+id).is(':checked')) {
		firewall = '1';
	}
	if ($('#protected-'+id).is(':checked')) {
		protected_serv = '1';
	}
	var servergroup = $('#servergroup-'+id+' option:selected' ).val();
	if (cur_url[0].split('#')[0] == "servers.py") {
		 servergroup = $('#new-server-group-add').val();
	}
	$.ajax( {
		url: "options.py",
		data: {
			updateserver: $('#hostname-'+id).val(),
			port: $('#port-'+id).val(),
			servergroup: servergroup,
			typeip: typeip,
			haproxy: haproxy,
			nginx: nginx,
			apache: apache,
			firewall: firewall,
			enable: enable,
			slave: $('#slavefor-'+id+' option:selected' ).val(),
			cred: $('#credentials-'+id+' option:selected').val(),
			id: id,
			desc: $('#desc-'+id).val(),
			protected: protected_serv,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#server-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#server-"+id ).removeClass( "update" );
				}, 2500 );
			}
		}
	} );
}
function uploadSsh() {
	toastr.clear();
	if ($( "#ssh-key-name option:selected" ).val() == "Choose server" || $('#ssh_cert').val() == '') {
		toastr.error('All fields must be completed');
	} else {
		$.ajax( {
			url: "options.py",
			data: {
				ssh_cert: $('#ssh_cert').val(),
				name: $('#ssh-key-name').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1')  {
						toastr.error(data);
					} else if (data.indexOf('success') != '-1') {
						toastr.clear();
						toastr.success(data)
					} else {
						toastr.error('Something wrong, check and try again');
					}
			}
		} );
	}
}
function updateSSH(id) {
	toastr.clear();
	var ssh_enable = 0;
	if ($('#ssh_enable-'+id).is(':checked')) {
		ssh_enable = '1';
	}
	var group = $('#sshgroup-'+id).val();
	if (cur_url[0].split('#')[0] == "servers.py") {
		 group = $('#new-server-group-add').val();
	}
	$.ajax( {
		url: "options.py",
		data: {
			updatessh: 1,
			name: $('#ssh_name-'+id).val(),
			group: group,
			ssh_enable: ssh_enable,
			ssh_user: $('#ssh_user-'+id).val(),
			ssh_pass: $('#ssh_pass-'+id).val(),
			id: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#ssh-table-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#ssh-table-"+id ).removeClass( "update" );
				}, 2500 );
				$('select:regex(id, credentials) option[value='+id+']').remove();
				$('select:regex(id, ssh-key-name) option[value='+$('#ssh_name-'+id).val()+']').remove();
				$('select:regex(id, credentials)').append('<option value='+id+'>'+$('#ssh_name-'+id).val()+'</option>').selectmenu("refresh");
				$('select:regex(id, ssh-key-name)').append('<option value='+$('#ssh_name-'+id).val()+'>'+$('#ssh_name-'+id).val()+'</option>').selectmenu("refresh");
			}
		}
	} );
}
function updateTelegram(id) {
	toastr.clear();
	$.ajax( {
		url: "options.py",
		data: {
			updatetoken: $('#telegram-token-'+id).val(),
			updategchanel: $('#telegram-chanel-'+id).val(),
			updatetelegramgroup: $('#telegramgroup-'+id).val(),
			id: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#telegram-table-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#telegram-table-"+id ).removeClass( "update" );
				}, 2500 );
			}
		}
	} );
}
function updateSlack(id) {
	toastr.clear();
	$.ajax( {
		url: "options.py",
		data: {
			update_slack_token: $('#slack-token-'+id).val(),
			updategchanel: $('#slack-chanel-'+id).val(),
			updateslackgroup: $('#slackgroup-'+id).val(),
			id: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#slack-table-"+id).addClass( "update", 1000 );
				setTimeout(function() {
					$( "#slack-table-"+id ).removeClass( "update" );
				}, 2500 );
			}
		}
	} );
}
function updateBackup(id) {
	toastr.clear();
	if ($( "#backup-type-"+id+" option:selected" ).val() == "Choose server" || $('#backup-rserver-'+id).val() == '' || $('#backup-rpath-'+id).val() == '') {
		toastr.error('All fields must be completed');
	} else {
		$.ajax( {
			url: "options.py",
			data: {
				backupupdate: id,
				server: $('#backup-server-'+id).text(),
				rserver: $('#backup-rserver-'+id).val(),
				rpath: $('#backup-rpath-'+id).val(),
				type: $('#backup-type-'+id).val(),
				time: $('#backup-time-'+id).val(),
				cred: $('#backup-credentials-'+id).val(),
				description: $('#backup-description-'+id).val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
					toastr.error(data);
				} else {
					toastr.clear();
					$("#backup-table-"+id).addClass( "update", 1000 );
					setTimeout(function() {
						$( "#backup-table-"+id ).removeClass( "update" );
					}, 2500 );
				}
			}
		} );
	}
}
function showApacheLog(serv) {
	var rows = $('#rows').val()
	var grep = $('#grep').val()
	var exgrep = $('#exgrep').val()
	var hour = $('#time_range_out_hour').val()
	var minut = $('#time_range_out_minut').val()
	var hour1 = $('#time_range_out_hour1').val()
	var minut1 = $('#time_range_out_minut1').val()
	$.ajax( {
		url: "options.py",
		data: {
			rows1: rows,
			serv: serv,
			grep: grep,
			exgrep: exgrep,
			hour: hour,
			minut:minut,
			hour1: hour1,
			minut1: minut1,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			$("#ajax").html(data);
			window.history.pushState("Logs", "Logs", cur_url[0] + "?serv=" + serv + "&rows1=" + rows + "&grep=" + grep +
					'&exgrep=' + exgrep +
					'&hour=' + hour +
					'&minut=' + minut +
					'&hour1=' + hour1 +
					'&minut1=' + minut1);
		}
	} );
}
function checkSshConnect(ip) {
	$.ajax( {
		url: "options.py",
		data: {
			checkSshConnect: 1,
			serv: ip,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('error:') != '-1') {
				toastr.error(data)
			} else if(data.indexOf('failed') != '-1') {
				toastr.error(data)
			} else if(data.indexOf('Errno') != '-1') {
				toastr.error(data)
			} else {
				toastr.clear();
				toastr.success('Connect is accepted');
			}
		}
	} );
}
function openChangeUserPasswordDialog(id) {
	changeUserPasswordDialog(id);
}
function openChangeUserGroupDialog(id) {
	changeUserGroupDialog(id);
}
function openChangeUserServiceDialog(id) {
	changeUserServiceDialog(id);
}
function changeUserPasswordDialog(id) {
	$( "#user-change-password-table" ).dialog({
			autoOpen: true,
			resizable: false,
			height: "auto",
			width: 600,
			modal: true,
			title: "Change "+$('#login-'+id).val()+" password",
			show: {
				effect: "fade",
				duration: 200
			},
			hide: {
				effect: "fade",
				duration: 200
			},
			buttons: {
				"Change": function() {
					changeUserPassword(id, $(this));
				},
				Cancel: function() {
					$( this ).dialog( "close" );
					$('#missmatchpass').hide();
				}
			}
		});
}
function changeUserPassword(id, d) {
	var pass = $('#change-password').val();
	var pass2 = $('#change2-password').val();
	if(pass != pass2) {
		$('#missmatchpass').show();
	} else {
		$('#missmatchpass').hide();
		toastr.clear();
		$.ajax( {
			url: "options.py",
			data: {
				updatepassowrd: pass,
				id: id,
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('error:') != '-1') {
					toastr.error(data);
				} else {
					toastr.clear();
					$("#user-"+id).addClass( "update", 1000 );
					setTimeout(function() {
						$( "#user-"+id ).removeClass( "update" );
					}, 2500 );
					d.dialog( "close" );
				}
			}
		} );
	}
}
function changeUserGroupDialog(id) {
	$.ajax( {
		url: "options.py",
		data: {
			getusergroups: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('danger') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$('#change-user-groups-form').html(data);
				$( "#change-user-groups-dialog" ).dialog({
					resizable: false,
					height: "auto",
					width: 450,
					modal: true,
					title: "Change "+$('#login-'+id).val()+" groups",
					buttons: {
						"Save": function() {
							$( this ).dialog( "close" );
							changeUserGroup(id);
						},
						Cancel: function() {
							$( this ).dialog( "close" );
						}
					  }
				});
			}
		}
	} );
}
function changeUserServiceDialog(id) {
	$.ajax( {
		url: "options.py",
		data: {
			getuserservices: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('danger') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$('#change-user-service-form').html(data);
				$( "#change-user-service-dialog" ).dialog({
					resizable: false,
					height: "auto",
					width: 450,
					modal: true,
					title: "Manage "+$('#login-'+id).val()+" services",
					buttons: {
						"Save": function() {
							$( this ).dialog( "close" );
							changeUserServices(id);
						},
						Cancel: function() {
							$( this ).dialog( "close" );
						}
					  }
				});
			}
		}
	} );
}
function changeUserGroup(id) {
	var groups = $('#usergroup-'+id).val().toString();
	$.ajax( {
		url: "options.py",
		data: {
			changeUserGroupId: id,
			changeUserGroups: groups,
			changeUserGroupsUser: $('#login-'+id).val(),
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
				toastr.error(data);
			} else {
				$("#user-" + id).addClass("update", 1000);
				setTimeout(function () {
					$("#user-" + id).removeClass("update");
				}, 2500);
			}
		}
	} );
}
function changeUserServices(id) {
	var services = $('#userservice-'+id).val().toString();
	$.ajax( {
		url: "options.py",
		data: {
			changeUserServicesId: id,
			changeUserServices: services,
			changeUserServicesUser: $('#login-'+id).val(),
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
				toastr.error(data);
			} else {
				$("#user-" + id).addClass("update", 1000);
				setTimeout(function () {
					$("#user-" + id).removeClass("update");
				}, 2500);
			}
		}
	} );
}
function addUserGroup(id) {
	$.ajax( {
		url: "options.py",
		data: {
			changeUserGroupId: id,
			changeUserGroups: $('#new-group').val(),
			changeUserGroupsUser: 'new',
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function confirmAjaxServiceAction(action, service) {
	$( "#dialog-confirm-services" ).dialog({
		resizable: false,
		height: "auto",
		width: 400,
		modal: true,
		title: "Are you sure you want to "+ action + " " + service+"?",
		buttons: {
			"Sure": function() {
				$( this ).dialog( "close" );
				ajaxActionServies(action, service)
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
}
function ajaxActionServies(action, service) {
	$.ajax( {
		url: "options.py",
		data: {
			action_service: action,
			serv: service,
			token: $('#token').val()
		},
		success: function( data ) {
			if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
				toastr.error(data);
			} else if (data.indexOf('warning: ') != '-1') {
				toastr.warning(data);
			} else {
				window.history.pushState("services", "services", cur_url[0].split("#")[0] + "#services");
				toastr.success('The ' + service + ' has been ' + action +'ed');
				loadServices();
			}
		},
		error: function(){
			alert(w.data_error);
		}
	} );
}
function updateService(service) {
	$("#ajax-update").html('')
	$("#ajax-update").html(wait_mess);
	$.ajax( {
		url: "options.py",
		data: {
			update_haproxy_wi: 1,
			service: service,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('Failed') != '-1') {
				toastr.error(data);
			} else if (data.indexOf('Complete!') != '-1'){
				toastr.clear();
				toastr.success(service + ' has been updated');
			} else if (data.indexOf('Unauthorized') != '-1') {
				toastr.clear();
				toastr.error('It seems like Unauthorized in the Roxy-WI repository. How to get Roxy-WI auth you can read <b><a href="https://haproxy-wi.org/installation.py" title="How to get Roxy-WI auth">hear</a></b>');
			} else if (data.indexOf('but not installed') != '-1') {
				toastr.clear();
				toastr.error('There is settings for Roxy-WI repository, but Roxy-WI is installed without repository. Please reinstall with yum');
			} else if (data.indexOf('No Match for argument') != '-1') {
				toastr.clear();
				toastr.error('It seems like Roxy-WI repository is not set. Please read docs for <b><a href="https://haproxy-wi.org/updates.py">detail</a></b>');
			} else if (data.indexOf('password for') != '-1') {
				toastr.clear();
				toastr.error('It seems like apache user needs to be add to sudoers. Please read docs for <b><a href="https://haproxy-wi.org/updates.py">detail</a></b>');
			} else if (data.indexOf('No packages marked for update') != '-1') {
				toastr.clear();
				toastr.info('It seems like the lastest version Roxy-WI is installed');
			} else if (data.indexOf('Connection timed out') != '-1') {
				toastr.clear();
				toastr.error('Cannot connect to Roxy-WI repository. Connection timed out');
			} else if (data.indexOf('--disable') != '-1') {
				toastr.clear();
				toastr.error('It seems like there is a problem with repositories');
			} else if (data.indexOf('Error: Package') != '-1') {
				toastr.clear();
				toastr.error(data);
			} else if (data.indexOf('conflicts with file from') != '-1') {
				toastr.clear();
				toastr.error(data);
			}
			$("#ajax-update").html('');
			loadupdatehapwi();
		}
	} );
}
function confirmDeleteOpenVpnProfile(id) {
	$( "#dialog-confirm" ).dialog({
		resizable: false,
		height: "auto",
		width: 400,
		modal: true,
		title: "Are you sure you want to delete profile " +id+ "?",
		buttons: {
			"Delete": function() {
				$( this ).dialog( "close" );
				removeOpenVpnProfile(id);
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
}

function removeOpenVpnProfile(id) {
	$("#"+id).css("background-color", "#f2dede");
	$.ajax( {
		url: "options.py",
		data: {
			openvpndel: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function( data ) {
			data = data.replace(/\s+/g,' ');
			if(data == "Ok ") {
				$("#"+id).remove();
			} else if (data.indexOf('error:') != '-1' || data.indexOf('unique') != '-1') {
				toastr.error(data);
			}
		}
	} );
}
function uploadOvpn() {
	toastr.clear();
	if ($( "#ovpn_upload_name" ).val() == '' || $('#ovpn_upload_file').val() == '') {
		toastr.error('All fields must be completed');
	} else {
		$.ajax( {
			url: "options.py",
			data: {
				uploadovpn: $('#ovpn_upload_file').val(),
				ovpnname: $('#ovpn_upload_name').val(),
				token: $('#token').val()
			},
			type: "POST",
			success: function( data ) {
				data = data.replace(/\s+/g,' ');
				if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1')  {
					toastr.error(data);
				} else if (data.indexOf('success') != '-1') {
					toastr.clear();
					toastr.success(data)
					location.reload()
				} else {
					toastr.error('Something wrong, check and try again');
				}
			}
		} );
	}
}
function OpenVpnSess(id, action) {
	$.ajax({
		url: "options.py",
		data: {
			actionvpn: action,
			openvpnprofile: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else if (data.indexOf('success') != '-1') {
				toastr.clear();
				toastr.success(data)
				location.reload()
			} else {
				toastr.error('Something wrong, check and try again');
			}
		}
	} );
}
function scanPorts(id) {
	$.ajax({
		url: "options.py",
		data: {
			scan_ports: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#show_scans_ports_body").html(data);
				$("#show_scans_ports" ).dialog({
					resizable: false,
					height: "auto",
					width: 360,
					modal: true,
					title: "Openned ports",
					buttons: {
						Close: function() {
							$( this ).dialog( "close" );
							$("#show_scans_ports_body").html('');
						}
					}
				});
			}
		}
	} );
}
function viewFirewallRules(id) {
	$.ajax({
		url: "options.py",
		data: {
			viewFirewallRules: id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error: ') != '-1') {
				toastr.error(data);
			} else {
				toastr.clear();
				$("#firewall_rules_body").html(data);
				$("#firewall_rules" ).dialog({
					resizable: false,
					height: "auto",
					width: 860,
					modal: true,
					title: "Firewall rules",
					buttons: {
						Close: function() {
							$( this ).dialog( "close" );
							$("#firewall_rules_body").html('');
						}
					}
				});
			}
		}
	} );
}
function loadServices() {
	$.ajax({
		url: "options.py",
		data: {
			loadservices: 1,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				$('#ajax-services-body').html(data);
				$.getScript(awesome);
			}
		}
	} );
}
function loadupdatehapwi() {
	$.ajax({
		url: "options.py",
		data: {
			load_update_hapwi: 1,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('danger') != '-1' || data.indexOf('unique') != '-1' || data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				$('#ajax-updatehapwi-body').html(data);
			}
		}
	} );
}
function loadchecker() {
	$.ajax({
		url: "options.py",
		data: {
			loadchecker: 1,
			page: cur_url[0].split('#')[0],
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('group_error') == '-1' && data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				$('#checker').html(data);
				$( "select" ).selectmenu();
				$("button").button();
				$.getScript('/inc/users.js');
				$.getScript(awesome);
			}
		}
	} );
}
function loadopenvpn() {
	$.ajax({
		url: "options.py",
		data: {
			loadopenvpn: 1,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('group_error') == '-1' && data.indexOf('error:') != '-1') {
				toastr.error(data);
			} else {
				$('#openvpn').html(data);
				$.getScript(awesome);
			}
		}
	} );
}
function checkTelegram(telegram_id) {
	$.ajax({
		url: "options.py",
		data: {
			check_telegram: telegram_id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('error_code') != '-1') {
				toastr.error(data);
			} else {
				toastr.success('Test message has been sent');
			}
		}
	} );
}
function checkSlack(slack_id) {
	$.ajax({
		url: "options.py",
		data: {
			check_slack: slack_id,
			token: $('#token').val()
		},
		type: "POST",
		success: function (data) {
			data = data.replace(/\s+/g, ' ');
			if (data.indexOf('error:') != '-1' || data.indexOf('error_code') != '-1') {
				toastr.error(data);
			} else {
				toastr.success('Test message has been sent');
			}
		}
	} );
}
function updateServerInfo(ip, id) {
	$.ajax({
			url: "options.py",
			data: {
				act: 'updateSystemInfo',
				server_ip: ip,
				server_id: id,
				token: $('#token').val()
			},
			type: "POST",
			success: function (data) {
				data = data.replace(/\s+/g, ' ');
				if (data.indexOf('error:') != '-1' || data.indexOf('error_code') != '-1') {
					toastr.error(data);
				} else {
					$("#server_info-"+id).html(data);
					$('#server_info-'+id).show();
					$('#server_info_link-'+id).attr('title', 'Hide System info');
					$.getScript(awesome);
				}
			}
		} );
}
function showServerInfo(id, ip) {
	if ($('#server_info-'+id).css('display') == 'none') {
		$.ajax({
			url: "options.py",
			data: {
				act: 'getSystemInfo',
				server_ip: ip,
				server_id: id,
				token: $('#token').val()
			},
			type: "POST",
			success: function (data) {
				data = data.replace(/\s+/g, ' ');
				if (data.indexOf('error:') != '-1' || data.indexOf('error_code') != '-1') {
					toastr.error(data);
				} else {
					$("#server_info-"+id).html(data);
					$('#server_info-'+id).show();
					$('#server_info_link-'+id).attr('title', 'Hide System info');
					$.getScript(awesome);
				}
			}
		} );
	} else {
		$('#server_info-'+id).hide();
		$('#server_info_link-'+id).attr('title', 'Show System info');
	}
}
