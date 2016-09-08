
#**************************************************************************
# Identification:result_check.tcl
# Purpose:       result check by cli
#**************************************************************************

proc result_check {operInfo parCmd parEnd} {
    foreach infoItem [split $operInfo "\n"] {
        if {[regexp $parCmd $infoItem] == 1} {
            continue
        } elseif {[regexp $parEnd $infoItem] == 1} {
            continue
        } else {
            set infoTrim [string trim $infoItem]
            if {[string length $infoTrim] == 0} {
                continue
            } elseif {[regexp $infoTrim $parCmd] == 1} {
                continue
            } else {
                return $operInfo
            }
        }
    }
    return 0
}
