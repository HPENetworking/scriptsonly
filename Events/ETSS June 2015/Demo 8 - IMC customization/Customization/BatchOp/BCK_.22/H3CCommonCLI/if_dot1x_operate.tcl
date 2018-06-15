
#**************************************************************************
#Identification: if_dot1x_operate.tcl
#Purpose:        enable/disable interface 802.1x by cli.
#**************************************************************************

set timeout $standard_timeout

send "dot1x\r"
expect {
  "enabled globally" {
      expect -re $enable_prompt      
  } -re {(.+])}
}

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

if { $ifdot1xoper == 1 } {
   send "dot1x\r"
   expect {
      "802.1x is enabled" {
      	expect -re $enable_prompt
      
      } -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "dot1x\r"
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
   send "undo dot1x\r"
   expect {
    	"802.1X is disabled" {
    		expect -re $enable_prompt
    	
    	} -re {(.+])} {
		    set operInfo $expect_out(1,string)
		    set parEnd {.+]}
		    set parCmd "dot1x\r"
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
             