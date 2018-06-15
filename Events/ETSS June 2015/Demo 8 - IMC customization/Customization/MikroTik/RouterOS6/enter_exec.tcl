set IGNORE_DELAY true

set loop true
set timeout $standard_timeout

while {$loop == "true"} {
        expect {
                $password_prompt {
                                send "$password"
                                sleep 1
                                send "\r"
                }  $username_prompt {
                                send "$username"
                                sleep 1
                                send "\r"
                }  $login_as {
                                send "$username"
                                sleep 1
                                send "\r"
                }  $info_prompt {
                                send "\r"
                }  "Store key in cache" {
                        send "y\r"
                        set loop false
                } -re $exec_prompt {
                        set loop false
                } "incorrect username or password" {
                        set ERROR_MESSAGE "Authentication failed"
                        set ERROR_RESULT true
                        return
                } "Access denied" {
                        set ERROR_MESSAGE "Authentication failed"
                        set ERROR_RESULT true
                        return
                }
          }
}

set IGNORE_DELAY false
