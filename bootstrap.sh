#!/usr/bin/env bash


sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip
sudo yum -y install python36u-devel
sudo yum install -y epel-release
sudo yum -y install ansible
sudo yum -y install nginx
sudo systemctl start nginx
sudo systemctl enable nginx

sudo pip3.6 install virtualenv

