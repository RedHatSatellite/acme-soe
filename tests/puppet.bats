#!/usr/bin/env bats

@test "Is puppet-agent installed?" {
    skip "we use Ansible, not puppet."
    rpm -q puppet-agent
}

# if you do NOT use puppet agent, then test for 3 instead of 0 at the end of the block
# if that is the case, you will obviously also want to change the test description
@test "Is puppet agent running?" {
    skip "we use Ansible, not puppet."
  if [ -e '/usr/bin/systemctl' ]
  then
    run systemctl status puppet
  else
    run service puppet status
  fi
  [ $status -eq 0 ]
}

# only usefult if not running puppet agent
@test "was a cron job created for puppet?" {
  skip "only enable this if you run puppet from cron instead of the default service"
  [[ -f /etc/cron.d/puppet ]]
  grep -v ^# /etc/cron.d/puppet | grep "puppet agent --onetime --no-daemonize"
}

