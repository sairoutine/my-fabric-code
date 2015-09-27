# coding:utf-8
from fabric.api import * 

def all():
	make_user()
	install_dotfiles()
	root_install_ssh_auth()
	root_install_peco()
	root_install_ag()
	root_install_vim74()
	root_install_tmux()
	root_install_node()
	root_install_git()

	puts('all done.')

def make_user(admin_username='sairoutine'):
	with hide('commands'):
 		run('adduser {username}'.format(username=admin_username))
	 	run('echo "{username} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'.format(username=admin_username))
		run('cp -r /root/.ssh/ /home/{username}/'.format(username=admin_username))
		run('chown -R {username} /home/{username}/.ssh'.format(username=admin_username))

	puts('add {username} done.'.format(username=admin_username))

def install_dotfiles(admin_username='sairoutine'):
	with settings(user=admin_username, warn_only=True):
		with cd('~/'):
			run('git clone https://github.com/sairoutine/dotfiles.git')

			with cd('./dotfiles'):
				run('sh ./dotfilesLink.sh')

			run('git clone https://github.com/Shougo/neobundle.vim.git ./.vim/bundle/neobundle.vim')
			run('git clone https://github.com/Shougo/vimproc.vim.git ./.vim/bundle/vimproc')

			with cd('./.vim/bundle/vimproc/'):
				# needed by make
				run('sudo yum install -y gcc ncurses-devel')
				run('make')

		puts('install dotfiles done.')

def root_install_ssh_auth(admin_user='sairoutine'):
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('cp -r ~/.ssh  /home/{username}/'.format(username=admin_user))

	puts('install ssh auth done.')

def root_install_peco():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('wget https://github.com/peco/peco/releases/download/v0.3.2/peco_linux_amd64.tar.gz')
		run('tar -xzf peco_linux_amd64.tar.gz')
		run('mv ./peco_linux_amd64/peco /usr/local/bin/')

		# rm
		run('rm -rf peco_linux_amd64.tar.gz ./peco_linux_amd64')

	puts('install peco done.')

def root_install_ag():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('rpm -ivh http://swiftsignal.com/packages/centos/6/x86_64/the-silver-searcher-0.13.1-1.el6.x86_64.rpm')

	puts('install ag done.')

def root_install_vim74():
	if env.user != 'root':
		abort('rootで実行してください')

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

def root_install_tmux():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		# needed by tmux
		#run('yum -y groupinstall "Development Tools"')
		run('yum install -y gcc ncurses-devel')

		# libevent2.0
		run('curl -L https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz -o libevent-2.0.21-stable.tar.gz')
		run('tar xzf libevent-2.0.21-stable.tar.gz')
		with cd('libevent-2.0.21-stable'):
			run('./configure')
			run('make')
			run('make install')
		# rm
		run('rm -rf libevent-2.0.21-stable.tar.gz ./libevent-2.0.21-stable')

		# install tmux
		run('wget http://downloads.sourceforge.net/tmux/tmux-1.9a.tar.gz')
		run('tar xzf tmux-1.9a.tar.gz')
		with cd('./tmux-1.9a'):
			run('./configure CFLAGS="-I/usr/local/include" CPPFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib"')
			run('make')
			run('make install')
		run('ln -s /usr/local/lib/libevent-2.0.so.5 /usr/lib64/libevent-2.0.so.5')
		# rm
		run('rm -rf tmux-1.9a.tar.gz ./tmux-1.9a')


	puts('install tmux done.')

def root_install_node():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('yum install -y epel-release')
		run('yum install -y node npm --enablerepo=epel')
		run('npm install -g jshint')
	puts('install node done.')

def root_install_git():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('yum install -y curl-devel expat-devel gettext-devel openssl-devel zlib-devel')

		run('wget https://www.kernel.org/pub/software/scm/git/git-2.3.3.tar.gz')
		run('tar xzvf git-2.3.3.tar.gz')
		with cd('./git-2.3.3'):
			run('make prefix=/usr/bin all')
			run('make prefix=/usr/bin install')
		# rm
		run('rm -rf git-2.3.3.tar.gz ./git-2.3.3')

	puts('install git done.')


def root_install_node12():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('yum install -y gcc-c++')
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

def root_install_elixir():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('wget http://www.erlang.org/download/otp_src_17.5.tar.gz')
		run('tar zxvf otp_src_17.5.tar.gz')
		with cd('otp_src_17.5'):
			run('./configure')
			run('make')
			run('make install')
		run('rm -rf otp_src_17.5')

		run('git clone https://github.com/elixir-lang/elixir.git')
		with cd('./elixir'):
			run('make')
			run('make install')
		run('rm -rf ./elixir')
	puts('install elixir done.')
def root_install_phoenix():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('mix archive.install https://github.com/phoenixframework/phoenix/releases/download/v0.16.1/phoenix_new-0.16.1.ez')

	puts('install phoenix done.')

