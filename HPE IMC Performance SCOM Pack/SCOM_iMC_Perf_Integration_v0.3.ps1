# Copyright 2016 Hewlett Packard Enterprise Development LP.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#####################################################################
# Title : PowerShell script intended to be used to create new
#         SCOM Management Pack which get performance data for
#         network devices directly in iMC using Rest API
# Author : Fabien GIRAUD
# Version : 0.2
#
# Description :
# PowerShell script intended to be used to create new SCOM Management
# Pack which get performance data for network devices directly in 
# iMC using Rest API
#
# Version History :
#	V0.1 : creation of the script and simple test with CPU and/or 
#          Memory usage (first phase : simply display the perf data
#          on stdout and store in file).
#          Script gets ip address of the SCOM node (for phase 1, hard
#          coded), then using iMC API gets dev id in iMC. Then the 
#          script will list the performance indexes for Memory and
#          CPU usage, then it will get last performance data for 
#          this indexes / device
#          Parameters:
#					- Type of output (txt, csv or scom)
#					- Device IP (string)
#	V0.2 : Adding SCOM capabilities in order to directly write
#		   performance data in SCOM performance monitoring
#   v0.3 : Changing the way scom integration works - Since it can't
#          be run in a collection rule for each Network Device,
#          this will run on management server and so get the list
#          of all Network Device and put the perf data in the perf
#          view of the management server
#          New parameters order:
#					- Type of output (txt, csv or scom)
#					- Device IP (only applicable for csv and txt)
#
####################################################################

 # Parameters
param ($outputType,$deviceIP)

 # iMC Connection variable and initialization
 
$imchost = "10.10.105.2"
$imcport = "8080"
$imcprot = "http"
$iMCUser = "imcrs"
$iMCPWD = "imcrs"

$ImcApiBaseUrl = $imcprot + "://" + $imchost + ":" + $imcport + "/imcrs/" 

$secpasswd = ConvertTo-SecureString $iMCPWD -AsPlainText -Force
$imcadmin = New-Object System.Management.Automation.PSCredential ($iMCUser, $secpasswd)


if(!$imcadmin){ $imcadmin = Get-Credential }


#-----------------------------------------------------------------------------#
# Base Query of devices. Used to find the id of the current device based on IP #
# Parameters:																   #
#			- Device IP (string)											   #
#-----------------------------------------------------------------------------#
Function imcDeviceLookup
{  
param ($itemIP)                    
 
    $url = $ImcApiBaseUrl + "plat/res/device?" + "ip" + "=" + $itemIP + "&exact=true"
 
    Write-Host "--Debug-- URL: $url"
 
    $result = Invoke-RestMethod -Uri $url -method GET -DisableKeepAlive -TimeoutSec $customTimeOut -Verbose -Credential $imcadmin -ContentType "application/xml"
    $imcDevice = $result.list.device
    $imcDevID = $imcDevice.id
    
	write-host "--Debug-- Found device information: Label="$imcDevice.label" IP="$imcDevice.ip" Location="$imcDevice.Location

    write-host "Result : Device ID = ($imcDevID)"
if ($imcDevID) {return $imcDevID}
else {return 0}
}

#-----------------------------------------------------------------------------#
# Base Query of Performance Tasks. Used to find the id of the tasks we want to #
# use (first phase : only CPU Usage and Memory Usage)                          #
#-----------------------------------------------------------------------------#
Function imcPerfTaskLookup
{
$imcPerfIndexList = @("CPU Usage","Memory Usage")
$globalTaskIDList = @()

	foreach ($item in $imcPerfIndexList) {
		write-host "--Debug-- Perf index: $item"
		$url = $ImcApiBaseUrl + "perf/task?" + "name" + "=" + $item
		
		Write-Host "--Debug-- URL: $url"
		
		$result = Invoke-RestMethod -Uri $url -method GET -DisableKeepAlive -TimeoutSec $customTimeOut -Verbose -Credential $imcadmin -ContentType "application/xml"
		$imcTasks = $result.list.task
		
		$tempTaskIDList = @()
		foreach($i in $imcTasks) {

			write-host "--Debug-- "$i.taskName "ID="$i.taskId
			
			$tempTaskIDList += $i.taskId
		}
		
		$globalTaskIDList += $tempTaskIDList

	}

	write-host "Result : Task IDs list = $globalTaskIDList"
	
	return $globalTaskIDList
}

#-----------------------------------------------------------------------------#
# Query of perf data. Used to get latest perf data for both specific dev id    #
# and task ids.                                                                #
# Parameters:                                                                  #
#			- Dev ID (integer)                                                 #
#			- Task ID (integer array)                                          #
#-----------------------------------------------------------------------------#
Function imcPerfDataGet
{
param ($DevID,$TaskIDs)
$PerfDataList = @()

	foreach ($item in $TaskIDs) {
		write-host "--Debug-- Task ID: $item"
		$url = $ImcApiBaseUrl + "perf/summaryData?" + "taskId" + "=" + $item + "&devId" + "=" + $DevID + "&dataGranularity=1"
		
		Write-Host "--Debug-- URL: $url"
		
		$result = Invoke-RestMethod -Uri $url -method GET -DisableKeepAlive -TimeoutSec $customTimeOut -Verbose -Credential $imcadmin -ContentType "application/xml"
		
		if ($result) {
			$imcTempPerfData = $result.list.perfSummaryData

			foreach ($i in $imcTempPerfData) {
				write-host "Performance data "$i.taskName $i.objIndexDesc "for device ID "$DevID "="$i.currentValue
				$PerfDataList += $i
			}
		}
	}

return $PerfDataList
}

#-----------------------------------------------------------------------------#
# Display perf data. This function will use the perf data collected. In a first    #
# step we will write this to a text file. Second step will use scom management #
# pack.                                                                        #
# Parameters:                                                                  #
#			- Device IP														   #
#			- PerfData (list of performance data)                              #
#			- Type: txt, csv or scom 										   #
#			- Device Name (only used for scom output type)                     #
#-----------------------------------------------------------------------------#
Function displayPerfData
{
param ($type, $devIP, $perfDataList, $devName)

	# option 1 : txt
	# write in a readable text format file
	if ($type -eq "txt") {
		$txtFile = "Perf_$devIP.txt"
		$FileExists =  Test-Path $txtFile
		if (-not $FileExists) {
			$text = " ------------------------------------------"
			$text | Out-File $txtFile
			$text = "| Performance data for device $devIP |"
			$text | Out-File $txtFile -Append
			$text = " ------------------------------------------"
			$text | Out-File $txtFile -Append
		
		}
		
		$text = "--------------------------------------------"
		$text | Out-File $txtFile -Append
		$text = Get-date -format g
		$text | Out-File $txtFile -Append
		$text = "--------------------------------------------"
		$text | Out-File $txtFile -Append
		foreach ($i in $perfDataList) {
			$text = $i.taskName + $i.objIndexDesc + "=" + $i.currentValue
			$text | Out-File $txtFile -Append
		}
	}
	
	# option 2 : csv
	# write in a csv comma separated file to be used in external soft such as excel
	elseif ($type -eq "csv") {
		$txtFile = "Perf_$devIP.csv"
		$FileExists =  Test-Path $txtFile
		if (-not $FileExists) {
			foreach ($i in $perfDataList) {
				if ($text) {$text +=","}
				$text += $i.taskName + $i.objIndexDesc
			}
			$text += ",DateTime"
			$text | Out-File $txtFile
		}
		foreach ($i in $perfDataList) {
			if ($text2) {$text2 +=","}
			$text2 += $i.currentValue
		}
		$currentDateTime = Get-date
		$text2 += "," + $currentDateTime
		$text2 | Out-File $txtFile -Append
	}
	
	# option 3 : scom
	# write directly in scom performance view (will be done in release 0.2 :))
	elseif ($type -eq "scom") {
		#Load the MOMScript API, PropertyBag, and log a starting script event 
#		$api = New-Object -comObject 'MOM.ScriptAPI'
#		$bag = $api.CreatePropertyBag()
		$api.LogScriptEvent("SCOM_iMC_Perf_integration.ps1",100,1,"Starting write perf data in SCOM for $devIP")
		foreach ($i in $perfDataList) {
            $PerfName=$i.taskname
            $InstanceDesc=$i.objIndexDesc
            $Counter = $PerfName +"---" + $InstanceDesc
            $PerfValue=$i.currentValue
		    $bag = $api.CreatePropertyBag()
			$bag.AddValue("Counter",$Counter)
			$bag.AddValue("Instance",$devName)
			$bag.AddValue("PerfValue",$PerfValue)
            write-host "--Debug-- Writing perf data on device $devName for $Counter = $PerfValue"
            $bag
		}
		$api.LogScriptEvent("SCOM_iMC_Perf_integration.ps1",101,1,"Ending write perf data in SCOM for $devIP")

	}
}

#-----------------------------------------------------------------------------#
# Base Query of Network devices in SCOM. Used to get the list of all Network   #
# Devices discovered in SCOM. 												   #
#-----------------------------------------------------------------------------#
Function SCOMNetworkDeviceLookup
{  

	$SCOMNetworkDevices = Get-SCOMClass -DisplayName "Network Device" | Get-SCOMClassInstance
	$SCOMNetworkDevices | Format-List *
	$SCOMNetDevicesShort=$SCOMNetworkDevices | select DisplayName, @{Label="SNMPAddress";Expression={$_.'[System.NetworkManagement.Node].SNMPAddress'}}
	
	write-host "--Debug-- List of Device IP on which we'll get perf data in iMC :" $SCOMNetDevicesShort.SNMPAddress.Value
	return $SCOMNetDevicesShort
}
#-----------------------------------------------------------------------------#
#        Main                                                                 #
#-----------------------------------------------------------------------------#

$customTimeOut=5
$headers = @{"X-Requested-With"="powershell"}

 # Beginning of execution :)
 
$TasksIDList = imcPerfTaskLookup

if ($outputType -eq "scom") {
	$api = New-Object -comObject 'MOM.ScriptAPI'
	$api.LogScriptEvent("SCOM_iMC_Perf_integration.ps1",100,1,"Starting get performance data in iMC through rest API for device $deviceIP")
	$SCOMNetDevices=SCOMNetworkDeviceLookup
	
	foreach ($NetDevice in $SCOMNetDevices)
	{
        if ($NetDevice.SNMPAddress.Value) {
            write-host "--Debug-- Getting info on " $NetDevice.DisplayName "SNMP Address="$NetDevice.SNMPAddress.Value
		    $deviceID = imcDeviceLookup $NetDevice.SNMPAddress.Value
		    if ($deviceID) {
                $PerfData = imcPerfDataGet $deviceID $TasksIDList
                displayPerfData $outputType $deviceIP $PerfData $NetDevice.DisplayName
            }
        }
	}
	
}

else {	
	$deviceID = imcDeviceLookup $deviceIP
	if ($deviceID) {
        $PerfData = imcPerfDataGet $deviceID $TasksIDList
        displayPerfData $outputType $deviceIP $PerfData
    }
}
	
if ($outputType -eq "scom") {
	$api.LogScriptEvent("SCOM_iMC_Perf_integration.ps1",101,1,"Ending get performance data in iMC through rest API for device $deviceIP")
}
