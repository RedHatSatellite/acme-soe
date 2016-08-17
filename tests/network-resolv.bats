#!/usr/bin/env bats

@test "dns_search, can I ping a short hostname?" {
  ping -c 1 $(hostname -s)
}

@test "nameserver, is at least one nameserver set?" {
  grep -q nameserver /etc/resolv.conf
}

@test "nameserver, is the first nameserver pingable?" {
  nameserver1=$(grep nameserver /etc/resolv.conf | awk '{ print $2 }' | 
head -n 1)
  ping -c 1 ${nameserver1}
}

@test "nameserver, is the last nameserver pingable?" {
  nameserver2=$(grep nameserver /etc/resolv.conf | awk '{ print $2 }' | 
tail -n 1)
  ping -c 1 ${nameserver2}
}

# check that bind-utils is installed, otherwise we have no nslookup command
@test "is bind-utils installed?" {
  rpm -q bind-utils
}

# try to resolve the SUT's hostname
@test "name resolution, can I resolve System Under Test fqdn?" {
  nslookup $(hostname -f)
}

###
### add some DNS lookups of internal machines
### obviously you need to adjust these to your site name
###
# webserver at ACME
@test "name resolution, can I resolve the webserver fqdn?" {
  nslookup www.example.com
}

# Jenkins server at ACME
@test "name resolution, can I resolve the Jenkins server fqdn?" {
  nslookup jenkins.example.com
}
