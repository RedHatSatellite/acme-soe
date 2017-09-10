#!/usr/bin/env bats

# vim: filetype=sh:autoindent:tabstop=2:shiftwidth=2:expandtab

load os_helper

# if you use ntp, then this test is not for you

@test "chrony, is chrony installed?" {
    tPackageExists chrony
}

@test "chrony, is chronyd running?" {
  if [ -e '/usr/bin/systemctl' ]
  then
    run systemctl status chronyd
  else
    run service chronyd status
  fi
  [ "$status" -eq 0 ]
}

@test "chrony, are we talking to at least two servers?" {
  result="$(chronyc sources | grep ^\^ | wc -l)"
  [ ${result} -ge 2 ]
}

