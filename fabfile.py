from fabric.api import run,sudo,settings,cd

def all():
	make_user()
	intall_dotfiles()
	root_install_peco()
	root_install_ag()
	root_install_vim74()
	root_install_node()

def make_user():
	admin_username = 'sairoutine'

	with settings(warn_only=True):
 		if run('adduser {username}'.format(username=admin_username)):
 			run('echo "{username} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'.format(username=admin_username))
			run('cp -r /root/.ssh/ /home/{username}/'.format(username=admin_username))
			run('chown -R {username} /home/{username}/.ssh'.format(username=admin_username))

def install_dotfiles():
	admin_username = 'sairoutine'

	with settings(user=admin_username, warn_only=True):
		run('git clone https://github.com/sairoutine/dotfiles.git')

		#with cd('./dotfiles'):

		run('mkdir -p ./.vim/bundle/')
		run('git clone https://github.com/Shougo/neobundle.vim.git ./.vim/bundle/neobundle.vim')
		run('git clone https://github.com/Shougo/vimproc.vim.git ./.vim/bundle/vimproc.vim')

		with cd('./.vim/bundle/vimproc.vim/'):
			run('make')

def root_install_peco():
	run('wget https://github.com/peco/peco/releases/download/v0.3.2/peco_linux_amd64.tar.gz')
	run('tar -xzf peco_linux_amd64.tar.gz')
	run('mv ./peco_linux_amd64/peco /usr/local/bin/')

	# rm
	run('rm -rf peco_linux_amd64.tar.gz ./peco_linux_amd64')

def root_install_ag():
	run('rpm -ivh http://swiftsignal.com/packages/centos/6/x86_64/the-silver-searcher-0.13.1-1.el6.x86_64.rpm')

def root_install_vim74():
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

def root_install_node():
	run('yum install -y epel-release')
	run('yum install -y nodejs npm --enablerepo=epel')
	run('npm install -g jshint')
