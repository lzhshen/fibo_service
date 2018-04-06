# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant_data"
  config.vm.box = "centos/7"
  config.vm.provision :shell, path: "./bootstrap.sh"
  # Run Ansible from the Vagrant VM
  config.vm.provision "ansible_local" do |ansible|
    ansible.provisioning_path="/vagrant_data/ansible"
    ansible.inventory_path = "inventory"
    ansible.playbook = "deploy.yml"
    ansible.verbose = "vvv"
    ansible.sudo = true
    ansible.limit = "all"
  end
end
