
#**************************************************************************
# Identification:enter_enable
# Purpose:       enter the "enable" mode on the device
#**************************************************************************

send "system-view\r"
expect {
	"The number of users" {
		set ERROR_MESSAGE "Device reports too many users are in system-view mode: please try again later."
		set ERROR_RESULT  true
		#exit
	} -re "$error_pattern" {
		expect -re $exec_prompt
		set ERROR_MESSAGE "The user is not authorized to use the 'system-view' command."
		set ERROR_RESULT  true
		#exit
	} -re $enable_prompt {
		# Success
	}
}