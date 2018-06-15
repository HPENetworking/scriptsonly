#! /usr/local/bin/perl

sub cleanupLocalUser
{
	#打开文件，用于测试	
	#open(CFGFILE,"F:/temp/10.153.89.178.cfg") || die "File don't exist!";
	#my($config) = "";
	#while(<CFGFILE>) {
	#	$config = $config.$_."\r\n";
	#}
			
	my($config) = @_;

	# CLI sometimes leaks in some syslog messages.. remove them _first_ [important]
	$config =~ s/(^|\n)\%.*//g; 

	$config =  removeMores($config);
	$config =~ s/display current-configuration\n//;
	$config =  stripLastLine($config);

	# Add a leading newline to match file transfer results
	$config = "\n".$config;

	# This driver requires that deployed configurations contain \r\n's
	$config =~ s/\n/\r\n/g;
	
	#命令行输出格式如下
    #local-user zxm
	# password simple icc
	# authorization-attribute level 3
	# service-type ssh telnet
	
	#local-user test
    # password cipher =W6JJ`N_LBKQ=^Q`MAF4<1!!
    #authorization-attribute level 3
    #service-type ssh telnet

    my $FormatResult  = "";       
	my $keyLocalUser = "local-user ";
	my $keyPasswordSimple = "password simple ";
	my $keyPasswordCipher = "password cipher ";
	my $keyUserLevel = "authorization-attribute level ";
	my $keyServiceType = "service-type ";
	
	my $LocalUserName = "";	
	my $LocalUserServiceType = "";
	my $LocalUserPassword = "";
	my $LocalUserLevel = "";
	my $loc = -1;
	my $PasswordMode = "";
	
	my $start_ = 0;
	my $end_key = "\r\n";
	my $first_line = 1;
	my $next_loc = -1;
	my $next_config = $config ;
	
	while(1) {	
		$LocalUserName = "";	
		$LocalUserPassword = "";
		$PasswordMode = "";
		$LocalUserLevel = "";
		$LocalUserServiceType = "";
		
		#user name		
	    $loc       = index ($next_config, $keyLocalUser, 0);
	    if ($loc != -1) {  
	    	$start_ = $loc + length $keyLocalUser;	 
	    	$next_config = substr($next_config, $start_); 
	    		    	  		    		        	
	    	$next_loc = index ($next_config, $keyLocalUser, 0);
	    	if ($next_loc == -1) {
		    	$next_loc = 65536;
		    }  
		    		    
	    	$loc       = index ($next_config, $end_key, 0);
	    	if ($loc != -1) {    		
	    		$LocalUserName = substr($next_config, 0, $loc);
	    		$LocalUserName = mytrim($LocalUserName);	
	    		$LocalUserName = ltrim($LocalUserName);	  
	    		$LocalUserName = rtrim($LocalUserName);	   
	    		my $emptyLoc =  index ($LocalUserName, " ", 0);		   		
	    		if ($emptyLoc != -1) {
	    			#error, not the user name	    			
	    	        return $FormatResult;
	    		}    		   		
	    	}
	    }
	    else
	    {	  	
	    	return $FormatResult;
	    }
	    	    	    	
    	#password simple
    	$loc       = index ($next_config, $keyPasswordSimple, 0);
    	if ($loc != -1 && $loc < $next_loc) {
    		$start_ = $loc + length $keyPasswordSimple;	  
    		$loc    = index ($next_config, $end_key, $start_);
    		if ($loc != -1) {    		
	    		$LocalUserPassword = substr($next_config, $start_, $loc - $start_);
	    		$LocalUserPassword = mytrim($LocalUserPassword);
	    		$PasswordMode = "simple";	    		
	    	}
    	}
    	else {
	    	#password cipher
	    	$loc       = index ($next_config, $keyPasswordCipher, 0);
	    	if ($loc != -1 && $loc < $next_loc) {
	    		$start_ = $loc + length $keyPasswordCipher;	  	    		
	    		$loc    = index ($next_config, $end_key, $start_);
	    		if ($loc != -1) {    		
		    		$LocalUserPassword = substr($next_config, $start_, $loc - $start_);
		    		$LocalUserPassword = mytrim($LocalUserPassword);
		    		$PasswordMode = "cipher";		    		  		
		    	}
	    	}
        }
        
        #authorization-attribute level 3
        #level 3
        $loc       = index ($next_config, $keyUserLevel, 0);
    	if ($loc != -1 && $loc < $next_loc) {
    		$start_ = $loc + length $keyUserLevel;	  
    		$loc    = index ($next_config, $end_key, $start_);
    		if ($loc != -1) {    		
	    		$LocalUserLevel = substr($next_config, $start_, $loc - $start_);
	    		$LocalUserLevel = mytrim($LocalUserLevel);	    		   		
	    	}
    	}
    	else {
    		my $tmpKeyUserLevel = "level ";
    	   	$loc       = index ($next_config, $tmpKeyUserLevel, 0);
	    	if ($loc != -1 && $loc < $next_loc) {
	    		$start_ = $loc + length $tmpKeyUserLevel;	  
	    		$loc    = index ($next_config, $end_key, $start_);
	    		if ($loc != -1) {    		
		    		$LocalUserLevel = substr($next_config, $start_, $loc - $start_);
		    		$LocalUserLevel = mytrim($LocalUserLevel);	    		   		
		    	}
	    	}
    	}
    	
    	#service-type, may be more than one line
    	my $last_loc = -1;
    	my $first_type = 1;
    	while (1) {    	
	    	$loc       = index ($next_config, $keyServiceType, $last_loc + 1);
	    	if ($loc != -1 && $loc < $next_loc) {
	    		$start_ = $loc + length $keyServiceType;	  
	    		$loc    = index ($next_config, $end_key, $start_);
	    		if ($loc != -1) {    		
		    		my $tmpLocalUserServiceType = substr($next_config, $start_, $loc- $start_);
		    		$tmpLocalUserServiceType = mytrim($tmpLocalUserServiceType);
		    		$tmpLocalUserServiceType = rtrim($tmpLocalUserServiceType);	    	
		    		
		    		my $tmpLoc = index ($tmpLocalUserServiceType, "authentication-type", 0); 	
		    		if ( $tmpLoc != -1) {
		    		    last;	
		    		}
		    		
		    		$tmpLoc = index ($tmpLocalUserServiceType, "all", 0); 	
		    		if ( $tmpLoc != -1) {
		    		    last;	
		    		}
		    		
		    		if ($first_type == 1) {
		    		    $LocalUserServiceType = $tmpLocalUserServiceType;	
		    		    $first_type = 0;
		    		}	    		
		    		else {
		    		    $LocalUserServiceType = $LocalUserServiceType." ".$tmpLocalUserServiceType;	
		    	    }
		    	}
		    	
		    	$last_loc = $loc;
	    	}
	    	else {
	    	    last;	
	    	}
        }
    	
    	if ($first_line == 1) {
    	   	$FormatResult = "\$LocalUserName = ".$LocalUserName."?|?\$PasswordMode = ".$PasswordMode."?|?\$LocalUserPassword = ".$LocalUserPassword."?|?\$LocalUserLevel = ".$LocalUserLevel."?|?\$LocalUserServiceType = ".$LocalUserServiceType;    	
    	   	$first_line = 0;
    	}
    	else {
    		$FormatResult = $FormatResult."\r\n"."\$LocalUserName = ".$LocalUserName."?|?\$PasswordMode = ".$PasswordMode."?|?\$LocalUserPassword = ".$LocalUserPassword."?|?\$LocalUserLevel = ".$LocalUserLevel."?|?\$LocalUserServiceType = ".$LocalUserServiceType;
    	}    	    	      	
    } 
    
    return $FormatResult;
}

sub cleanupSSHGlobal
{
	#打开文件，用于测试	
	#open(CFGFILE,"F:/temp/test.cfg") || die "File don't exist!";
	#my($config) = "";
	#while(<CFGFILE>) {
	#	$config = $config.$_."\r\n";
	#}
			
	my($config) = @_;

	# CLI sometimes leaks in some syslog messages.. remove them _first_ [important]
	$config =~ s/(^|\n)\%.*//g; 

	$config =  removeMores($config);
	$config =~ s/display ssh server status\n//;
	$config =  stripLastLine($config);

	# Add a leading newline to match file transfer results
	$config = "\n".$config;

	# This driver requires that deployed configurations contain \r\n's
	
	$config =~ s/\n/\r\n/g;
	
	#命令行输出格式如下
	#SSH server: Enable
	#SSH version : 1.99
	#SSH connection timeout : 60 seconds
	#SSH server key generating interval : 0 hours
	#SSH Authentication retries : 3 times
	#SFTP Server: Enable
	#SFTP idle timeout : 10 minutes
	    
	my $SSHServerCompatibleSSH1x = "";	
	my $SSHServerVersion = "";
	my $SSHServerRekeyInterval = "";
	my $SSHServerAuthRetries = "";
	my $SSHServerAuthTimeout = "";
	my $SFTPServerIdleTimeout = "";
	my $SSHServerEnable = "";
	my $SFTPServerEnable = "";
	
	my $loc_start = -1;
	my $loc_end = -1;
	my $key_ = "";
		
	my $end_key = "\r";
		    
	#SSH server: Enable
	$key_ = "SSH server: ";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config, $end_key, $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerEnable = substr($config, $start_, $loc_end - $start_);
    		$SSHServerEnable = mytrim($SSHServerEnable);    		   		
    	}
    }
    
    #SFTP Server: Enable
	$key_ = "SFTP Server:";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config, $end_key, $start_);
    	if ($loc_end != -1) {    		
    		$SFTPServerEnable = substr($config, $start_, $loc_end - $start_);
    		$SFTPServerEnable = mytrim($SFTPServerEnable);    		   		
    	}
    }
        	
	#SSH version : 1.99
	$key_ = "SSH version :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config, $end_key, $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerVersion = substr($config, $start_, $loc_end - $start_);
    		$SSHServerVersion = mytrim($SSHServerVersion);    		   		
    	}
    }
    
    #SSH connection timeout : 60 seconds
	$key_ = "SSH connection timeout :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config, $end_key, $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerAuthTimeout = substr($config, $start_, $loc_end - $start_);
    		$SSHServerAuthTimeout = mytrim($SSHServerAuthTimeout);    		   		
    	}
    }
	
	#SSH connection timeout : 60 seconds
	$key_ = "SSH connection timeout :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config,"seconds", $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerAuthTimeout = substr($config, $start_, $loc_end - $start_);
    		$SSHServerAuthTimeout = mytrim($SSHServerAuthTimeout);    		   		
    	}
    }
    
    #SSH server key generating interval : 0 hours
	$key_ = "SSH server key generating interval :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config,"hours", $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerRekeyInterval = substr($config, $start_, $loc_end - $start_);
    		$SSHServerRekeyInterval = mytrim($SSHServerRekeyInterval);    		   		
    	}
    }
    
    #SSH Authentication retries : 3 times
	$key_ = "SSH Authentication retries :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config,"times", $start_);
    	if ($loc_end != -1) {    		
    		$SSHServerAuthRetries = substr($config, $start_, $loc_end - $start_);
    		$SSHServerAuthRetries = mytrim($SSHServerAuthRetries);    		   		
    	}
    }
    
    #SFTP idle timeout : 10 minutes
	$key_ = "SFTP idle timeout :";		
    $loc_start       = index ($config, $key_, 0);
    if ($loc_start != -1) {    		    	
    	$start_ = $loc_start + length $key_;	   
    	    	
    	$loc_end       = index ($config,"minutes", $start_);
    	if ($loc_end != -1) {    		
    		$SFTPServerIdleTimeout = substr($config, $start_, $loc_end - $start_);
    		$SFTPServerIdleTimeout = mytrim($SFTPServerIdleTimeout);    		   		
    	}
    }
		
	$FormatResult = "\$SSHServerCompatibleSSH1x = ".$SSHServerCompatibleSSH1x."?|?\$SSHServerVersion = ".$SSHServerVersion."?|?\$SSHServerRekeyInterval = ".$SSHServerRekeyInterval."?|?\$SSHServerAuthRetries = ".$SSHServerAuthRetries."?|?\$SSHServerAuthTimeout = ".$SSHServerAuthTimeout."?|?\$SFTPServerIdleTimeout = ".$SFTPServerIdleTimeout."?|?\$SSHServerEnable = ".$SSHServerEnable."?|?\$SFTPServerEnable = ".$SFTPServerEnable;    	
	
    return $FormatResult;
}

sub cleanupSSHUser
{
	#open(CFGFILE,"F:/temp/test.cfg") || die "File don't exist!";
	#my($config) = "";
	#while(<CFGFILE>) {
	#	$config = $config.$_."\r\n";
	#}
			
	my($config) = @_;

	# CLI sometimes leaks in some syslog messages.. remove them _first_ [important]
	$config =~ s/(^|\n)\%.*//g; 

	$config =  removeMores($config);
	$config =~ s/display ssh user-information\n//;
	$config =  stripLastLine($config);

	# Add a leading newline to match file transfer results
	$config = "\n".$config;

	# This driver requires that deployed configurations contain \r\n's
	$config =~ s/\n/\r\n/g;
	
	#命令行输出格式如下
	#display ssh user-information
    #Total ssh users:5
	#Username            Authentication-type  User-public-key-name  Service-type
	#lll                 password-publickey   lll                   stelnet|sftp
	#wds                 password-publickey   wds                   stelnet|sftp
	#zxm                 password             null                  stelnet|sftp
	#zxm_41              password             null                  stelnet|sftp
	#zxm_20110721093511  password             null                  stelnet|sftp
	#<H3C>
		
	my $loc       = index ($config, "Service-type", 0);
	if ($loc != -1) { 
		$config = substr($config, $loc+12);     
	}
	
	$config = ltrim($config);
	$config = rtrim($config);
	
    my $FormatResult = "";
    my $SSHUserName = "";
    my $SSHUserAuthType = "";
    my $SSHUserPublicKeyName = "";
    my $SSHUserServiceType = "";
    my $SSHUserWorkDirectory = "";
    
    my $first_line = 1;    
    my $loc1 = -1;
    my $CurLine = "";
    my $haveMore = 1;
    
    while (1) {          	
	    $SSHUserName = "";
	    $SSHUserAuthType = "";
	    $SSHUserPublicKeyName = "";
	    $SSHUserServiceType = "";
	    $SSHUserWorkDirectory = "";
    
        $loc = index ($config, "\r\n", 0);
    	if ($loc == -1) {
    		$haveMore = 0;    	
    		$CurLine = $config;		
    		$CurLine = ltrim($CurLine);	
    	}
    	else {
    		$CurLine = substr($config, 0, $loc);     	
	    	$CurLine = rtrim(ltrim($CurLine));
	    	$config = substr($config, $loc+2);       		    	    		    	  
	    	
	    	if (length($CurLine) == 0) {
	    	    next;	
	    	}	
    	}
    	    	    	
    	#user-name
    	$loc1 = index ($CurLine, " ", 0);  
    	if ($loc1 == -1) {
    	    return $FormatResult;	
    	}
    	 	    	    	
    	$SSHUserName = substr($CurLine, 0, $loc1); 
    	$SSHUserName = mytrim($SSHUserName);
    	$CurLine  = substr($CurLine , $loc1+1);  
    	$CurLine = ltrim($CurLine);
     	    	   	
    	#auth type
    	$loc1 = index ($CurLine, " ", 0);
    	$SSHUserAuthType = substr($CurLine, 0, $loc1); 
    	$CurLine  = substr($CurLine , $loc1+1);  
    	$CurLine = ltrim($CurLine);   
    		
    	#publickey name
    	$loc1 = index ($CurLine, " ", 0);
    	$SSHUserPublicKeyName = substr($CurLine, 0, $loc1); 
    	$CurLine  = substr($CurLine , $loc1+1);  
    	$CurLine = ltrim($CurLine);  
    	   	
    	#service type    	
    	$SSHUserServiceType = ltrim($CurLine); 
    	$SSHUserServiceType = rtrim($CurLine); 
    	    	    	    	                 
    	if ($first_line == 1) {
    		if (length($SSHUserName) > 0) {
	    	   	$FormatResult = "\$SSHUserName = ".$SSHUserName."?|?\$SSHUserAuthType = ".$SSHUserAuthType."?|?\$SSHUserPublicKeyName = ".$SSHUserPublicKeyName."?|?\$SSHUserServiceType = ".$SSHUserServiceType."?|?\$SSHUserWorkDirectory = ".$SSHUserWorkDirectory;    	
	    	   	$first_line = 0;
    	    }
    	}
    	else {
    		if (length($SSHUserName) > 0) {
    		   $FormatResult = $FormatResult."\r\n"."\$SSHUserName = ".$SSHUserName."?|?\$SSHUserAuthType = ".$SSHUserAuthType."?|?\$SSHUserPublicKeyName = ".$SSHUserPublicKeyName."?|?\$SSHUserServiceType = ".$SSHUserServiceType."?|?\$SSHUserWorkDirectory = ".$SSHUserWorkDirectory;    	
    	    }
    	}   
    	
    	if ($haveMore == 0) { 
    	    return $FormatResult;	
    	}    	    	
    } 
    
    return $FormatResult;
}

sub removeMores
{
	my $string = shift;

	$string =~ s/  ---- More ----(\x1b\[\d+n)*\x1b\[\d+D +\x1b\[\d+D//g;
        $string =~ s/ ---- More ----(\s)*//g;
	return $string;
}

sub trim($) {
    my $string = shift;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    return $string;
}

sub rtrim($) {
    my $string = shift;
    $string =~ s/\s+$//;
    return $string;
}

sub ltrim($) {
    my $string = shift;
    $string =~ s/^\s+//;
    return $string;
}

sub mytrim($) {
     my $string = shift;
    $string =~ s/\r//g;
    $string =~ s/\n//g;
    return $string;
}

sub stripLastLine
{
	my($rawdata) = @_;

	$rawdata =~ s/\n+$//;
	$rawdata =~ s/[\S ]*?$//;
	$rawdata =~ s/\n+$//;
	
	return $rawdata;
}