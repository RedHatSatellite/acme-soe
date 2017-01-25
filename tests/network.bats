#!/usr/bin/env bats
# vim: filetype=sh:autoindent:tabstop=2:shiftwidth=2:expandtab

set -o pipefail

load os_helper

@test "Check that I can ping my gateway" {
  gw=$(ip route show | grep default | cut -d" " -f3)
  run ping -c 1 ${gw}
}

@test "Check that I can resolve www.redhat.com" {
  run nslookup www.redhat.com 
}

