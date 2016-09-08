
#**************************************************************************
# Identification:exit_enable
# Purpose:       exit the "enable" mode on the device
#**************************************************************************

send "quit\r"
expect -re $exec_prompt
    