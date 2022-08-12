exec { 'echo "Host 52.204.151.72
    IdentityFile ~/.ssh/school
    PasswordAuthentication no" >> /etc/ssh/ssh_config':
  path => "/bin"
}