# = Class: test
#
# install/configure testing framework
#
class test () {
  package { 'bats':
    ensure => latest,
    name   => 'bats',
  }

file { '/root/.ssh':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0700',
    }
    
    ssh_authorized_key { 'jenkins':
        ensure => present,
        key    => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQCUjnUfNNshxzbaHbjHJ5ohEvEMaNF6qab9uqAxXAZNtkoOmAjhAyW61jXpiQg82/5O9ReTVG0Ag49vVfZBq8wvgemC4MVZIDwK2M1h2rD2EQ0MN3w5o/YNeFJ6xXKCKePw4hf/yTjP/Pg0PStFjasPXWIPwqra83FH+ZOPYFta7FLI6W+5f7wNvIEx2l75OYNiItaCH7MqV6U7zUAX2QGczESZ3TmF1QGbv40iUcs9c6JkXBqgUHwd5AGu9b/lr/tTp1n4QHHDNtMKS6h79J36OwRE5TJkXEM34zw6RBV1Twx+SKP7dW2CVykQJ85L6ba8Ym4v44rEjEFIC7zBSFAH',
        type   => 'ssh-rsa',
        user   => 'root',
        target => '/root/.ssh/authorized_keys',
    }
}
