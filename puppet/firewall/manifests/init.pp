class firewall (
  $serverprofile = 'dmz',
) {
  service { 'firewalld':
    ensure => 'stopped',
    enable => false,
  }

  if $serverprofile == 'dmz'
  {
    service { 'iptables':
      ensure => 'running',
      enable => true,
    }
  }
  else {
    service { 'iptables':
      ensure => 'stopped',
      enable => false,
    }
  }
  file { '/etc/sysconfig/iptables':
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0600',
    content => template('firewall/iptables.erb'),
    require => Package['iptables'],
  }

  package { ['iptables', 'iptables-services']:
    ensure => latest,
  }
}
