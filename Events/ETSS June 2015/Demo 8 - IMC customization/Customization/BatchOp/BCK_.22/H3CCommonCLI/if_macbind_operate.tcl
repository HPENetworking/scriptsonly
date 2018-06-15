
#**************************************************************************
#Identification: if_macbind_operate.tcl
#Purpose:        enable/disable interface macbind by cli.
#**************************************************************************

set timeout $standard_timeout

send  "interface $portdesc\r"
expect -re {(.+])}
set operInfo $expect_out(1,string)
set parEnd {.+]}
set parCmd "interface $portdesc\r"
set result_tmp [result_check $operInfo $parCmd $parEnd]
if {$result_tmp != 0} {
    set ERROR_RESULT true
    set ERROR_MESSAGE $result_tmp
    return
}

if { $ifmacbindoper == 1 } {
   send "port-security max-mac-count 1\r"
   expect {
       -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "port-security max-mac-count 1\r"
      	set result_tmp [result_check $operInfo $parCmd $parEnd]
      	if {$result_tmp != 0} {
        	  send "quit\r"
          	expect -re $enable_prompt
          	set ERROR_RESULT true
          	set ERROR_MESSAGE $result_tmp
          	return
      	}	
      } 
   }
   send "port-security port-mode autolearn\r"
   expect {
       -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "port-security port-mode autolearn\r"
      	set result_tmp [result_check $operInfo $parCmd $parEnd]
      	if {$result_tmp != 0} {
        	  send "quit\r"
          	expect -re $enable_prompt
          	set ERROR_RESULT true
          	set ERROR_MESSAGE $result_tmp
          	return
      	}	
      } 
   }
} else {
   send "undo port-security port-mode\r"
   expect {
       -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "undo port-security port-mode\r"
      	set result_tmp [result_check $operInfo $parCmd $parEnd]
      	if {$result_tmp != 0} {
        	  send "quit\r"
          	expect -re $enable_prompt
          	set ERROR_RESULT true
          	set ERROR_MESSAGE $result_tmp
          	return
      	}	
      } 
   }
   
   send "undo port-security max-mac-count\r"
   expect {
       -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "undo port-security max-mac-count\r"
      	set result_tmp [result_check $operInfo $parCmd $parEnd]
      	if {$result_tmp != 0} {
        	  send "quit\r"
          	expect -re $enable_prompt
          	set ERROR_RESULT true
          	set ERROR_MESSAGE $result_tmp
          	return
      	}	
      } 
   }
}

send "quit\r"
expect -re $enable_prompt
             