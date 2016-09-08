
set timeout $standard_timeout
sleep 1

expect -re $exec_prompt {
}

send "export\r"

expect -re #

expect -re $exec_prompt {
}
