#!/usr/bin/env bats

if ! grep -q "profile_apache" /var/lib/puppet/client_data/catalog/`hostname`.json >&2 ; then
  echo 1
  exit 1 
fi

@test "Is httpd installed?" {
  rpm -q httpd
}

@test "Is http running?" {
  if [ -e '/usr/bin/systemctl' ]
  then
    run systemctl status httpd
  else
    run service httpd status
  fi
  [ "$status" -eq 0 ]
}

@test "Can we get a file?" {
  cat > /var/www/html/index.html <<EOF
<html>
OK
</html>
EOF
  wget http://localhost/
}

    
