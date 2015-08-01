from fabric.api import * 

def all():
	make_user()
	intall_dotfiles()
	root_install_peco()
	root_install_ag()
	root_install_vim74()
	root_install_node()

def make_user():
	admin_username = 'sairoutine'

	with hide('commands'):
 		run('adduser {username}'.format(username=admin_username))
	 	run('echo "{username} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'.format(username=admin_username))
		run('cp -r /root/.ssh/ /home/{username}/'.format(username=admin_username))
		run('chown -R {username} /home/{username}/.ssh'.format(username=admin_username))

	puts('add {username} done.'.format(username=admin_username))

def install_dotfiles():
	admin_username = 'sairoutine'

	with settings(user=admin_username, warn_only=True):
		with hide('commands'):
			run('git clone https://github.com/sairoutine/dotfiles.git')

			with cd('./dotfiles'):
				run('sh ./dotfilesLink.sh')

			run('git clone https://github.com/Shougo/neobundle.vim.git ./.vim/bundle/neobundle.vim')
			run('git clone https://github.com/Shougo/vimproc.vim.git ./.vim/bundle/vimproc')

			with cd('./.vim/bundle/vimproc/'):
				run('make')

		puts('install dotfiles done.')

def root_install_peco():

	with hide('commands'):
		run('wget https://github.com/peco/peco/releases/download/v0.3.2/peco_linux_amd64.tar.gz')
		run('tar -xzf peco_linux_amd64.tar.gz')
		run('mv ./peco_linux_amd64/peco /usr/local/bin/')

		# rm
		run('rm -rf peco_linux_amd64.tar.gz ./peco_linux_amd64')

	puts('install peco done.')

def root_install_ag():

	with hide('commands'):
		run('rpm -ivh http://swiftsignal.com/packages/centos/6/x86_64/the-silver-searcher-0.13.1-1.el6.x86_64.rpm')

	puts('install ag done.')

def root_install_vim74():

	with hide('commands'):
		# needed by vim7.4
		run('yum install -y gcc ncurses-devel')

		# install vim7.4
		run('wget ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2')
		run('tar xjf vim-7.4.tar.bz2')
		with cd('./vim74'):
			run('make')
			run('make install')
		# rm
		run('rm -rf vim-7.4.tar.bz2 ./vim74')

	puts('install vim74 done.')

def root_install_node():

	with hide('commands'):
		run('wget http://nodejs.org/dist/v0.12.2/node-v0.12.2.tar.gz')
 		run('tar xvf node-v0.12.2.tar.gz')
		with cd('node-v0.12.2'):
			run(' ./configure')
			run('make')
			run('make install')
		run('rm node-v0.12.2.tar.gz')
		run('rm -rf node-v0.12.2')
		run('yum install -y epel-release')
		run('yum install -y npm --enablerepo=epel')
		run('npm install -g jshint')
	puts('install node done.')
