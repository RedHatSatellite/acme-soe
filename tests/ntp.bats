#!/usr/bin/env bats

# note that on RHEL7 you might be using the default of chrony
# instead of ntp

@test "Is ntp installed?" {
  rpm -q ntp
}

@test "Is ntpd running?" {
  if [ -e '/usr/bin/systemctl' ]
  then
    run systemctl status ntpd
  else
    run service ntpd status
  fi
  [ "$status" -eq 0 ]
}

@test "ntp, are we talking to at least two servers?" {
  result="$(ntpdc -l 127.0.0.1 | grep ^client | wc -l)"
  [ ${result} -ge 2 ]
}

