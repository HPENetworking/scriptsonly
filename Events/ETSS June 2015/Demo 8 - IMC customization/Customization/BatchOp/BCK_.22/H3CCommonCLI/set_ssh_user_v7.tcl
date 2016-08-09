
#**************************************************************************
#Identification: set_ssh_user
#Purpose:        set ssh user by cli.
#**************************************************************************

set timeout $standard_timeout

set my_authentication "any"
if { $SSHUserAuthType == 2 } {
   set my_authentication "password"
} elseif { $SSHUserAuthType == 3 } {
   set my_authentication "publickey"
} elseif { $SSHUserAuthType == 5 } {
   set my_authentication "password-publickey"
} else {   
   set my_authentication "any"
}

set my_servicetype "all"
if { $SSHUserServiceType == 3 } {
   set my_servicetype "stelnet"
} elseif { $SSHUserServiceType == 4 } {
   set my_servicetype "sftp"
} 

#v5 device
if { $my_authentication == "password" } {
    send "ssh user $SSHUserName service-type $my_servicetype authentication-type $my_authentication\r"
} elseif { $SSHUserPublicKeyName == ""} {
    send "ssh user $SSHUserName service-type $my_servicetype authentication-type $my_authentication\r"
} else {
    send "ssh user $SSHUserName service-type $my_servicetype authentication-type $my_authentication assign publickey $SSHUserPublicKeyName\r"
}
sleep 1
expect {
    "Keyname does not exist" {
		expect -re $enable_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: Keyname does not exist"
		return
    } "Too many parameters" {
       #error, v3 device
    } -re $error_pattern {	
	   #error, v3 device	
	} -re $enable_prompt {
		# Done
		return
	}
}

#clear 
expect *

#v3 device
if { $my_authentication == "any" } {
    set my_authentication "all"
}
send "ssh user $SSHUserName authentication-type $my_authentication\r"
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


send "ssh user $SSHUserName service-type $my_servicetype\r"
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

set len [string length $SSHUserPublicKeyName]
if { $len > 0 } {
	send "ssh user $SSHUserName assign publickey $SSHUserPublicKeyName\r"
	expect {
	    "does not exist" {	        
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Keyname does not exist !"
			expect -re $enable_prompt
	    } -re $error_pattern {
			set error_message $expect_out(1,string)
			expect -re $enable_prompt
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Device error: $error_message"
		} -re "\r\n.+$enable_prompt" {
			# Done
		}
	}
}