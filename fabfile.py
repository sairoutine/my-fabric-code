# coding:utf-8
from fabric.api import * 

def all():
	root_install_git()
	make_user()
	install_dotfiles()
	root_install_ssh_auth()
	root_install_peco()
	root_install_pt()
	root_install_vim74()
	root_install_zsh()
	root_install_tmux()
	root_install_node()

	puts('all done.')

def add_user(admin_username):
	make_user(admin_username)
	install_dotfiles(admin_username)
	root_install_ssh_auth(admin_username)

	puts('add user done.')


def make_user(admin_username='sairoutine'):
	with hide('commands'):
 		run('adduser {username}'.format(username=admin_username))
	 	run('echo "{username} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'.format(username=admin_username))
		run('cp -r /root/.ssh/ /home/{username}/'.format(username=admin_username))
		run('chown -R {username} /home/{username}/.ssh'.format(username=admin_username))

	puts('add {username} done.'.format(username=admin_username))

def install_dotfiles(admin_username='sairoutine'):
	with settings(user=admin_username, warn_only=True):
		with hide('commands'):
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
		run('wget https://github.com/peco/peco/releases/download/v0.5.3/peco_linux_amd64.tar.gz')
		run('tar -xzf peco_linux_amd64.tar.gz')
		run('mv ./peco_linux_amd64/peco /usr/local/bin/')

		# rm
		run('rm -rf peco_linux_amd64.tar.gz ./peco_linux_amd64')

	puts('install peco done.')

def root_install_pt():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('wget https://github.com/monochromegane/the_platinum_searcher/releases/download/v2.2.0/pt_linux_amd64.tar.gz')
		run('tar -xzf pt_linux_amd64.tar.gz')
		run('mv ./pt_linux_amd64/pt /usr/local/bin/')

		# rm
		run('rm -rf pt_linux_amd64.tar.gz ./pt_linux_amd64')

	puts('install pt done.')



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
		run('curl -LOk https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz')
		run('tar -xf libevent-2.1.8-stable.tar.gz')
		with cd('libevent-2.1.8-stable'):
			run('./configure')
			run('make')
			run('make install')
		# rm
		run('rm -rf libevent-2.1.8-stable.tar.gz ./libevent-2.1.8-stable')

		# install tmux
		run('curl -LOk https://github.com/tmux/tmux/releases/download/2.8/tmux-2.8.tar.gz')
		run('tar xzf tmux-2.8.tar.gz')
		with cd('./tmux-2.8'):
			run('./configure CFLAGS="-I/usr/local/include" CPPFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib"')
			run('make')
			run('make install')
		run('ln -s /usr/local/lib/libevent-2.0.so.5 /usr/lib64/libevent-2.0.so.5')
		# rm
		run('rm -rf tmux-2.8.tar.gz ./tmux-2.8')


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
			run('make prefix=/usr all')
			run('make prefix=/usr install')
		# rm
		run('rm -rf git-2.3.3.tar.gz ./git-2.3.3')

	puts('install git done.')

def root_install_zsh():
	if env.user != 'root':
		abort('rootで実行してください')

	with hide('commands'):
		run('yum install -y gcc-c++')
		run('wget "http://downloads.sourceforge.net/project/zsh/zsh/5.1.1/zsh-5.1.1.tar.gz"');
 		run('tar xvf zsh-5.1.1.tar.gz')
		with cd('zsh-5.1.1'):
			run(' ./configure --prefix=/ --enable-multibyte')
			run('make')
			run('make install')
		run('rm zsh-5.1.1.tar.gz')
		run('rm -rf zsh-5.1.1')
		run('chsh -s /bin/zsh')
	puts('install zsh done.')

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

