#! /usr/local/bin/perl

sub cleanupConfiguration
{
        my($config) = @_;

        # CLI sometimes leaks in some syslog messages.. remove them _first_ [important]
        # $config =~ s/(^|\n)\%.*//g;

        $start = index($config, "\# software id = ");
        if ($start == -1)
        {
                $start = 0;
        }

        $cleanConfig = substr($config, $start);

        # Get rid of the exec prompt at the end, and any blank lines
        $cleanConfig =~ s/\[.*\] \>.*/\n/;
        $cleanConfig =~ s/\n+$//;

        # Add a trailing newline to match file transfer results
        $cleanConfig = $cleanConfig . "\n";

        return $cleanConfig;
}
