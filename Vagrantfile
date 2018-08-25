# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.provider 'virtualbox'
  config.vm.box = 'ubuntu/xenial64'

  config.vm.provider :virtualbox do |vb|
    vb.name = 'ist-652'
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3-pip
    pip3 install twitterscraper beautifulsoup4
  SHELL
end