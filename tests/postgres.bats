#!/usr/bin/env bats

if ! grep -q "profile_postgres" /opt/puppetlabs/puppet/cache/client_data/catalog/`hostname`.json >&2 ; then
  echo 1
  exit 1  
fi

@test "Is postgres server installed?" {
  rpm -q postgresql-server
}

@test "Is postgres running?" {
  if [ -e '/usr/bin/systemctl' ]
  then
    run systemctl status postgresql
  else
    run service postgresql status
  fi
  [ "$status" -eq 0 ]
}


