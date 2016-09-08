
#**************************************************************************
# Identification:initialize
# Purpose:       initialize variables
#**************************************************************************

set standard_timeout 10
set long_timeout 120
set very_long_timeout 1800
set very_very_long_timeout 2400

#Image sync and software center through VPN might take hours
set squeeze_timeout 15000
set username_prompt "sername:|ogin:"
set password_prompt assword:
set exec_prompt <.+>
set sftp_exec_prompt sftp>
set enable_prompt ]
set enforce_save false
set timeout $standard_timeout
set more_prompt {---- More ----}
set pause $more_prompt
set sent_password "false"
set banner_skip_repeat 0
set use_undeterministic_prompt "undeterministic prompt is not in use"
set error_pattern {(% (Incomplete|Unknown|Unrecognized|Too many parameters|Error:|Invalid|.*uthorization failed).*)}

set ERROR_RESULT false
set ERROR_MESSAGE ""
