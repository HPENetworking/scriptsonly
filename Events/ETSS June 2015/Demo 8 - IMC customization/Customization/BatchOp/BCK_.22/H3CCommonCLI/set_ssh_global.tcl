
#**************************************************************************
#Identification: set_ssh_global_cli
#Purpose:        set ssh global by cli.
#**************************************************************************

set timeout $standard_timeout

if { $SSHServerCompatibleSSH1x == 1 } {
   send "ssh server compatible-ssh1x enable\r"
} else {
   send "undo ssh server compatible-ssh1x enable\r"
}

expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $exec_prompt
		#set ERROR_RESULT  true
		#set ERROR_MESSAGE "Device error: $error_message"
		#return
		#v3 device not support this command, so ignore it
	} -re $enable_prompt {
		# Done
	}
}

send "ssh server authentication-retries $SSHServerAuthRetries\r"
expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $exec_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: $error_message"
		return
	} -re $enable_prompt {
		# Done
	}
}

send "ssh server rekey-interval $SSHServerRekeyInterval\r"
expect {
	-re $error_pattern {
		set error_message $expect_out(1,string)
		expect -re $exec_prompt
		set ERROR_RESULT  true
		set ERROR_MESSAGE "Device error: $error_message"
		return
	} -re $enable_prompt {
		# Done
	}
}

send "ssh server authentication-timeout $SSHServerAuthTimeout\r"
sleep 1
expect {
	-re $error_pattern {
		#v5 device		
		send "ssh server timeout $SSHServerAuthTimeout\r"
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
	} -re $enable_prompt {
		# Done
	}
}

send "sftp timeout $SFTPServerIdleTimeout\r"
sleep 1
expect {
	-re $error_pattern {
	    #v5 device
		send "sftp server idle-timeout $SFTPServerIdleTimeout\r"
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
	} -re $enable_prompt {
		# Done
	}
}

if { $SFTPServerEnable == 1 } {
   send "sftp server enable\r"
} else {
   send "undo sftp server enable\r"
}
sleep 1
expect {
	-re $error_pattern {
	    if { $SFTPServerEnable == 2 } {
	    	send "undo sftp server\r"
	        expect {
		       -re $error_pattern {
					set error_message $expect_out(1,string)
					expect -re $enable_prompt
					set ERROR_RESULT  true
					set ERROR_MESSAGE "Device error: $error_message"					
				} -re $enable_prompt {
					# Done
				}
			}      
		} else {			          
			set error_message $expect_out(1,string)
			expect -re $enable_prompt
			set ERROR_RESULT  true
			set ERROR_MESSAGE "Device error: $error_message"			
		}
	} -re $enable_prompt {
		# Done
	}
}

#v3 don't support next command 
if { $SSHServerEnable == 1 } {
   send "ssh server enable\r"
} else {
   send "undo ssh server enable\r"
}
sleep 1
expect {
	-re $error_pattern {
	    #v3 device
	    
	} -re "\n.+$enable_prompt" {
		# Done
		return
	}
}