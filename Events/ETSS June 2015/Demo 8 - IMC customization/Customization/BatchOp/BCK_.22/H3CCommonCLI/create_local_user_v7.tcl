
#**************************************************************************
#Identification: create_local_user_cli
#Purpose:        ctreate local user by cli.
#**************************************************************************

set timeout $standard_timeout

send "local-user $LocalUserName\r"
expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $enable_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: $error_message"
		return
	} -re $enable_prompt {
		# Done
	}
}

send "password $PasswordMode $LocalUserPassword\r"
expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $enable_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: $error_message"
        send "quit\r"
        expect -re $enable_prompt
		return
	} -re $enable_prompt {
		# Done
	}
}

sleep 1
expect *

send "authorization-attribute user-role $LocalUserLevel\r"
sleep 1
expect {
	-re "$error_pattern|Unrecognized" {
	
	    send "level $LocalUserLevel\r"
	    expect {
			-re $error_pattern {
				set error_message $expect_out(1,string)
				expect -re $enable_prompt
				set ERROR_RESULT  true
				set ERROR_MESSAGE "Device error: $error_message"
                send "quit\r"
                expect -re $enable_prompt
				return
			} -re $enable_prompt {
				# Done
			}
		}		
	} -re $enable_prompt {
		# Done
	}
}
#sleep 1s because some device can not expect correctly
sleep 1
expect *
send "service-type $LocalUserServiceType\r"
sleep 1
expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $enable_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: $error_message"
        send "quit\r"
        expect -re $enable_prompt
	} -re $enable_prompt {
		# Done
	}
}

send "quit\r"
expect -re $enable_prompt

