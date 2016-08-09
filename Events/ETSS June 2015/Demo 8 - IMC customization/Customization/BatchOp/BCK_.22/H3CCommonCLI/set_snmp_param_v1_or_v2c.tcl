
#**************************************************************************
#Identification: set_snmp_param_v1_or_v2c
#Purpose:        Set snmp param by cli.
#**************************************************************************

set timeout $standard_timeout

#snmp_type 1:v1 2:v2c

if {$snmp_type == 1} {
    send "snmp-agent sys-info version v1\r"
    expect -re {(.+])}
    set operInfo $expect_out(1,string)
    set parEnd {.+]}
    set parCmd "snmp-agent sys-info version"
    set result_tmp [result_check $operInfo $parCmd $parEnd]
    if {$result_tmp != 0} {
        set ERROR_RESULT true
        set ERROR_MESSAGE $result_tmp
        return   
    }
}

if {$snmp_type == 2} {
    send "snmp-agent sys-info version v2c\r"
    expect -re {(.+])}
    set operInfo $expect_out(1,string)
    set parEnd {.+]}
    set parCmd "snmp-agent sys-info version"
    set result_tmp [result_check $operInfo $parCmd $parEnd]
    if {$result_tmp != 0} {
        set ERROR_RESULT true
        set ERROR_MESSAGE $result_tmp
        return
    }
}


    send "snmp-agent community read $read\r"
    expect -re {(.+])}
    set operInfo $expect_out(1,string)
    set parEnd {.+]}
    set parCmd "snmp-agent community read $read"
    set result_tmp [result_check $operInfo $parCmd $parEnd]
    if {$result_tmp != 0} {
        set ERROR_RESULT true
        set ERROR_MESSAGE $result_tmp
        return   
    }
    
    send "snmp-agent community write $write\r"
    expect -re {(.+])}
    set operInfo $expect_out(1,string)
    set parEnd {.+]}
    set parCmd "snmp-agent community write $write"
    set result_tmp [result_check $operInfo $parCmd $parEnd]
    if {$result_tmp != 0} {
        set ERROR_RESULT true
        set ERROR_MESSAGE $result_tmp
        return   
    }
   
            