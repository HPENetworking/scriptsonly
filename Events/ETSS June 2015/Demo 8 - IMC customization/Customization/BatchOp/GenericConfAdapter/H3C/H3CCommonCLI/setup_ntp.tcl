expect -re $enable_prompt

send "ntp-service enable\r"

expect -re $enable_prompt

if {$Authentication} {
send "ntp-service authentication enable\r"
  expect -re $enable_prompt
  send "ntp-service authentication-keyid $keyid authentication-mode md5 simple $key\r"
  expect -re $enable_prompt
  send "ntp-service reliable authentication-keyid $keyid\r"
  expect -re $enable_prompt
  send "ntp-service unicast-server $server authentication-keyid $keyid\r"
 } else {
  send "ntp-service unicast-server $server\r"
  }

expect -re $enable_prompt

if {$Commit} {
  send "save force\r"
  }

expect -re $enable_prompt
