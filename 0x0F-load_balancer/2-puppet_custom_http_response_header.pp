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
  content => 'Hello World',
  require =>  File['/var/www/html/index.nginx-debian.html'],
}

file { 'error404':
  path    => '/var/www/html/Http404.html',
  mode    => '0644',
  content => "Ceci n'est pas une page",
  require =>  File['school'],
}

file_line { 'redirection':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\tserver_name _;\n\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;",
  match   => 'server_name _;',
  require => File['error404'],
}

file_line { 'redirectionerror':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\tserver_name _;\n\terror_page 404 /Http404.html;",
  match   => 'server_name _;',
  require => File_line['redirection'],
}

file_line { 'servedheader':
  ensure  => present,
  path    => '/etc/nginx/sites-available/default',
  line    => "\tserver_name _;\n\tadd_header X-Served-By $HOSTNAME;",
  match   => 'server_name _;',
  require => File_line['redirectionerror'],
}

exec { 'nginx restart':
  command  => 'service nginx restart',
  provider => 'shell',
  require  =>  File_line['servedheader'],
}