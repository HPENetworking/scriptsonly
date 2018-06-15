
#**************************************************************************
#Identification: set_snmp_param_v3
#Purpose:        Set snmp param by cli.
#**************************************************************************

set timeout $standard_timeout

#snmp_type v3
#read_mib_view_type 1:included 2:excluded
#write_mib_view_type 1:included 2:excluded
#priv_auth 1:none_none 2:none_md5 3:none_sha 4:des56_md5 5:des56_sha 6:aes128_md5 7:aes128_sha 8:3des_md5 9:3des_sha


    send "snmp-agent sys-info version v3\r"
    expect -re {(.+])}
    set operInfo $expect_out(1,string)
    set parEnd {.+]}
    set parCmd "snmp-agent sys-info version v3"
    set result_tmp [result_check $operInfo $parCmd $parEnd]
    if {$result_tmp != 0} {
        set ERROR_RESULT true
        set ERROR_MESSAGE $result_tmp
        return
    }
  

    if {$read_mib_view_type == 1} {
        send "snmp-agent mib-view included $read_mib_view $read_mib_node\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent mib-view included $read_mib_view $read_mib_node"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    } elseif {$read_mib_view_type == 2} {
        send "snmp-agent mib-view excluded $read_mib_view $read_mib_node\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent mib-view excluded $read_mib_view $read_mib_node"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$write_mib_view_type == 1} {
        send "snmp-agent mib-view included $read_mib_view $write_mib_node\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent mib-view included $read_mib_view $write_mib_node"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    } elseif {$write_mib_view_type == 2} {
        send "snmp-agent mib-view excluded $read_mib_view $write_mib_node\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "ssnmp-agent mib-view excluded $read_mib_view $write_mib_node"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }
    if {$priv_auth == 1} {
        send "snmp-agent group v3 $group_name read-view $read_mib_view write-view $write_mib_view\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent group v3 $group_name read-view $read_mib_view write-view $write_mib_view"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    } else {
        send "snmp-agent group v3 $group_name authentication read-view $read_mib_view write-view $write_mib_view\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent group v3 $group_name authentication read-view $read_mib_view write-view $write_mib_view"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }    
   
    if {$priv_auth == 1} {
        send "snmp-agent usm-user v3 $user_name $group_name\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 2} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 3} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 4} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode des56 $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode des56 $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 5} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode des56 $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode des56 $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 6} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode aes128 $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode aes128 $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }

    if {$priv_auth == 7} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode aes128 $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode aes128 $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }
   

    if {$priv_auth == 8} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode 3des $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod md5 $auth_pwd privacy-mode 3des $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }
    
    if {$priv_auth == 9} {
        send "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode 3des $priv_pwd\r"
        expect -re {(.+])}
        set operInfo $expect_out(1,string)
        set parEnd {.+]}
        set parCmd "snmp-agent usm-user v3 $user_name $group_name authentication-mod sha $auth_pwd privacy-mode 3des $priv_pwd"
        set result_tmp [result_check $operInfo $parCmd $parEnd]
        if {$result_tmp != 0} {
            set ERROR_RESULT true
            set ERROR_MESSAGE $result_tmp
            return   
        }
    }    
            