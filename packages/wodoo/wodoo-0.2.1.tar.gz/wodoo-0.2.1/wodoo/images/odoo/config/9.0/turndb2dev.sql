--set critical
update res_users set password = '', password_crypt = '${DEFAULT_DEV_PASSWORD}';
update ir_cron set active=false;
update ir_mail_server set smtp_host='${TEST_MAIL_HOST}', smtp_user=null, smtp_pass=null, smtp_encryption='none', smtp_port=${TEST_MAIL_SMTP_PORT};
delete from ir_config_parameter where key='webkit_path';
update fetchmail_server set server='${TEST_MAIL_HOST}', port='${TEST_MAIL_IMAP_PORT}', "user"='postmaster', password='postmaster', type='imap';
delete from ir_config_parameter where key = 'database.enterprise_code';


--set not-critical

/*if-table-exists caldav_cal*/ update caldav_cal set password = '1';
/*if-table-exists delivery_carrier_file*/update delivery_carrier_file set export_path = '/opt/out_dir';

