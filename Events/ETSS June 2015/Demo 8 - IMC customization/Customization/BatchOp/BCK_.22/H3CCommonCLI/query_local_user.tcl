
#**************************************************************************
#Identification: query_local_user
#Purpose:        query local user by cli.
#**************************************************************************

#clear last response
send "\r"
set loop true

while {$loop == "true"} {
	expect {
		-re $error_pattern {
			set error_message $expect_out(1,string)
			expect -re $exec_prompt
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Device error: $error_message"
			set loop false
		} -re "$exec_prompt" {
			# Done
			set loop false
		}
	}
}

#get the current config
set timeout $long_timeout
send "display current-configuration\r"
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
		} -re "\n$exec_prompt" {
			# Done
			set loop false
		}
	}
}

set timeout $standard_timeout
	