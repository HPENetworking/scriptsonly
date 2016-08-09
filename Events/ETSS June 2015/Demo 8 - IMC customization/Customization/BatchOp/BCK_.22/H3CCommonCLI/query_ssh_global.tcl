#**************************************************************************
#Identification: query_ssh_global
#Purpose:        query ssh global information by cli.
#**************************************************************************

set timeout $long_timeout
send "display ssh server status\r"
set loop true

while {$loop == "true"} {
	expect {
		-re "$more_prompt" {
			send " "
		} -re $error_pattern {
			set error_message $expect_out(1,string)
			expect -re $exec_prompt
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Device error: $error_message"
			set loop false
		} -re $exec_prompt {
			# Done
			set loop false
		}
	}
}

set timeout $standard_timeout