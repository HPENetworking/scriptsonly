
#**************************************************************************
# Identification:enter_exec
# Purpose:       enter the "exec" mode on the device
#**************************************************************************

set IGNORE_DELAY true
set loop true
set timeout $standard_timeout

while {$loop == "true"} {
	expect {
		-re $password_prompt {					    
		    send "$password"
		    sleep 1
			send "\r"
			
			set sent_password "true"
		} -re $username_prompt {
			if {$username == "\x24username" || $username == ""} {
				set ERROR_MESSAGE "Missing username"
				set ERROR_RESULT true
				set loop false
				#exit
			} else {
			    #sleep 1
				send "$username\r"
				set sent_password "false"
			}
		} "Press Y or ENTER to continue, N to exit" {
			send "Y"			
		} -re "y/n" {
			send "y\r"
		} -re "Store key in cache|Update cached key" {
			send "y\r"
		} "Wrong password" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Wrong password."
			#exit
			set loop false
		} "Please press ENTER" {
			send "\r"
			set loop false
		} "Login failed" {
			# Failure ... get out
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Device rejected the username or password."
			#exit			
			set loop false
		} "Passphrase for key" {
			send "$passphrase\r"
		} "Unable to use key file" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Unable to use key file."
			set loop false
		} "Network error" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Network error."
			set loop false
		} "Access denied" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Access denied."
			set loop false
		} "Authentication refused" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Authentication refused."
			set loop false
		} "FATAL ERROR:" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "FATAL ERROR."
			set loop false
		} "Fatal:" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "FATAL."
			set loop false
		} "Unable to load private key" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Unable to load private key."
			set loop false
		} "Server refused" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Server refused."
			set loop false
		} "Enter passphrase for key" {
			send "$passphrase\r"
		} "Are you sure you want to continue connecting" {
			send "yes\r"
		} "Permission denied" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Permission denied."
			set loop false
		} "Received disconnect" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Received disconnect."
			set loop false
		} "bad permissions" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "bad permissions."
			set loop false
		} "Identity file * not accessible:" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Identity file not accessible."
			set loop false
		} "Connection refused" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Connection refused."
			set loop false
		} "Connection timed out" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Connection timed out."
			set loop false
		} "connection is closed" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "connection is closed."
			set loop false
		} "Connection closed" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Connection closed."
			set loop false
		} "Write failed:" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Write failed: Broken pipe."
			set loop false
		} "Missing argument" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Missing argument."
			set loop false
		} "no authentication methods available" {
		#Bitvise
			set ERROR_RESULT  true
			set ERROR_MESSAGE "no authentication methods available."
			set loop false
		} "Authentication failed" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Authentication failed."
			set loop false
		} "S/A/C" {
			send "S\r"
		} "assphrase:" {
			send "$passphrase\r"
		} "Too many authentication failures" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Too many authentication failures."
			set loop false
		} "Connection aborted" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Connection aborted."
			set loop false
		} "parameter failed" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "parameter failed."
			set loop false
		} "Connection failed" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Connection failed."
			set loop false
		} "passphrase is invalid" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "passphrase is invalid."
			set loop false
		} "Server rejected" {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Server rejected."
			set loop false
		} -re $exec_prompt {
			set loop false

			if {$enable_password != "\x24enable_password" && $enable_password != ""} {

				send "super\r"
				set loop2 true
                set send_super false
                
				while {$loop2 == "true"} {
					expect {
						$password_prompt {
							if { $send_super == "false" } {
							   send "$enable_password\r"	
							   set send_super true	
							}	
						} "assword is not set" {
							expect -re $exec_prompt
							set loop2 false
						} "Wrong password" {
							expect -re $exec_prompt
							set ERROR_RESULT  true
							set ERROR_MESSAGE "Super password is invalid."
							#exit
							set loop2 false
						} -re $exec_prompt {
							set loop2 false
						}
					}
				}				
			}
		} "Login password has not been set" {
			# Failure ... get out
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Cannot login. Message from device: Login password has not been set!"
			set loop false
			#exit
		} timeout {
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Timeout to login. No message recive from device!"
			#exit
			set loop false
		}
	}
}
set IGNORE_DELAY false