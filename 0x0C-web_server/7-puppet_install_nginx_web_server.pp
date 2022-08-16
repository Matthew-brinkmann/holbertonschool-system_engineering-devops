# install and configure an Nginx server using Puppet. perform a 301 redirect when querying /redirect_me.
# strings to set up redirect_me.

package { 'nginx':
  provider => 'apt',
}

exec { 'rm':
  command  => 'rm /var/www/html/index.nginx-debian.html',
  onlyif   => 'test -e /var/www/html/index.nginx-debian.html',
  provider => 'shell',
}

file { 'school':
  path    => '/var/www/html/index.html',
  mode    => '0644',
  content => 'Hellow World',
}

exec { 'sed':
  command  => 'sed -i "/server_name _;/a\\\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;" /etc/nginx/sites-available/default',
  provider => 'shell',
}

exec { 'nginx start':
  command  => 'service nginx start',
  provider => 'shell',
}
