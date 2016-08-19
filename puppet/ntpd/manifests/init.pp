class ntpd {
	package {
		'ntp':
		ensure => installed,
	}
	->
	service {
		'ntpd':
		ensure => 'running',
		enable => true,
		# require => Package['ntp'] # covered by the arrow
	}
}
