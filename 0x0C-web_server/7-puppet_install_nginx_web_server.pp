# install and configure an Nginx server using Puppet. perform a 301 redirect when querying /redirect_me.
# strings to set up redirect_me.

package { 'nginx':
  provider => 'apt',
}

exec { 'nginx start':
  command  => 'service nginx start',
  provider => 'shell',
  require  =>  Package['nginx'],
}

file { '/var/www/html/index.nginx-debian.html':
  ensure  => absent,
  require =>  Exec['nginx start'],
}

file { 'school':
  path    => '/var/www/html/index.html',
  mode    => '0644',
  content => 'Hellow World',
  require =>  File['/var/www/html/index.nginx-debian.html'],
}

file_line { 'redirection':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\tserver_name _;\n\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;",
  match   => 'server_name _;',
  require => File['school'],
}

file_line { 'redirectionerror':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\tserver_name _;\n\terror_page 404 /Http404.html;",
  match   => 'server_name _;',
  require => File_line['redirection'],
}

exec { 'nginx restart':
  command  => 'service nginx restart',
  provider => 'shell',
  require  =>  File_line['redirectionerror'],
}
