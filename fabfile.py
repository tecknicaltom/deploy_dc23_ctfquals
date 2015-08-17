from fabric.api import require, sudo, put
from fabric.contrib.files import upload_template, exists
from os.path import basename

apt_dependencies = ['xinetd', 'libc6:i386', 'libstdc++6:i386']
deploy_directory = '/opt/quals/'

def make_xinetd_challenge(name, port, local_exe, local_flag):
    if(not exists('/home/%s' % name)):
        sudo('useradd -m %s' % name)
        sudo('chown root /home/%s' % name)

        put(local_path=local_exe, remote_path=deploy_directory, use_sudo=True, mode=0755)
        sudo('chown root:root %s/%s' % (deploy_directory, basename(local_exe)))

        put(local_path=local_flag, remote_path='/home/%s' % name, use_sudo=True, mode=0640)
        sudo('chown root:{name} /home/{name}/{flag_filename}'.format(name=name, flag_filename=basename(local_flag)))

        upload_template('xinetd_service.conf', '/etc/xinetd.d/%s' % name, context={
            'name': name,
            'exe_filename': basename(local_exe),
            'port': port,
            'deploy_directory': deploy_directory,
        }, use_sudo=True)
        sudo('chown root:root /etc/xinetd.d/%s' % name)


def deploy():
    require('hosts')
    sudo('sudo dpkg --add-architecture i386')
    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    if apt_dependencies:
        sudo('apt-get install -y %s' % ' '.join(apt_dependencies))

    sudo('mkdir -p %s' % deploy_directory)
    put(local_path='cd_runner/cd_runner', remote_path=deploy_directory, use_sudo=True, mode=0755)
    sudo('chown root:root %s/cd_runner' % deploy_directory)

    make_xinetd_challenge('babyecho', 3232, '../baby_s_first-1-babyecho/orig/babyecho_eb11fdf6e40236b1a37b7974c53b6c3d', '../baby_s_first-1-babyecho/flag.txt')
    make_xinetd_challenge('r0pbaby', 10436, '../baby_s_first-1-r0pbaby/orig/r0pbaby_542ee6516410709a1421141501f03760', '../baby_s_first-1-r0pbaby/flag.txt')
    make_xinetd_challenge('wwtw', 2606, '../pwnable-2-wibbly_wobbly_timey_wimey/orig/wwtw_c3722e23150e1d5abbc1c248d99d718d', '../pwnable-2-wibbly_wobbly_timey_wimey/flag.txt')

    sudo('/etc/init.d/xinetd restart')
