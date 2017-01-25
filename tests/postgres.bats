#!/usr/bin/env bats
# vim: filetype=sh:autoindent:tabstop=2:shiftwidth=2:expandtab

set -o pipefail

load os_helper

if ! grep -q "profile_postgres" /var/lib/puppet/client_data/catalog/`hostname`.json >&2 ; then
  echo 1
  exit 1  
fi

@test "Is postgres server installed?" {
    rpm -q postgresql-server
}

@test "Is postgres running?" {
    systemctl status postgresql
}


