
#**************************************************************************
#Identification: if_updown_operate.tcl
#Purpose:        up/down interface by cli.
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

if { $ifupdownoper == 1 } {
   send "undo shutdown\r"
   expect {
      "not shut down" {
      	expect -re $enable_prompt
      
      } -re {(.+])} {
      	set operInfo $expect_out(1,string)
      	set parEnd {.+]}
      	set parCmd "undo shutdown\r"
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
   send "shutdown\r"
   expect {
    	"been" {
    		expect -re $enable_prompt
    	
    	} -re {(.+])} {
		    set operInfo $expect_out(1,string)
		    set parEnd {.+]}
		    set parCmd "shutdown\r"
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
             