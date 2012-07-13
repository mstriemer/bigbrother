import os
from datetime import datetime

from fabric.api import run, env, cd, sudo, settings, prefix

env.user = 'mark'
env.hosts = ['{}@striemer.ca'.format(env.user)]
env.app_name = 'bigbrother'
env.repo_name = 'repo'
env.root_dir = os.path.join('/var/apps', env.app_name)
env.repo_dir = os.path.join(env.root_dir, env.repo_name)
env.shared_settings = os.path.join(env.root_dir, 'shared/settings/local.py')
env.local_settings = os.path.join(env.repo_dir, 'settings/local.py')
env.environment_dir = os.path.join('/var/apps/environments', env.app_name)
env.branch_name = 'master'

def update_repo():
    with settings(warn_only=True):
        if run('test -d {repo_dir}'.format(**env)).failed:
            sudo('git clone git://github.com/mstriemer/{app_name}.git '
                '{repo_dir}'.format(**env))
            sudo('chown -R {user}:{user} {repo_dir}'.format(**env))
    with cd(env.repo_dir):
        run('git fetch origin')
        sha = run('git ls-remote origin {branch_name}'.format(**env)).split()[0]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        run('git checkout -b deploy_{timestamp} {sha}'.format(
                timestamp=timestamp, sha=sha))
        manage('collectstatic --noinput')
        manage('compress')

def update_symlinks():
    create_symlink = None
    create_shared_settings = None
    with settings(warn_only=True):
        create_shared_settings = run('test -e {shared_settings}'.format(**env)).failed
        create_symlink = run('test -e {local_settings}'.format(**env)).failed
    if create_shared_settings:
        sudo('mkdir -p {shared_settings_dir}'.format(
                shared_settings_dir=os.path.dirname(env.shared_settings)))
        sudo('touch {shared_settings}'.format(**env))
    if create_symlink:
        with cd(os.path.dirname(env.local_settings)):
            run('ln -s {shared_settings}'.format(**env))

def update_packages():
    with settings(warn_only=True):
        if run('test -d {environment_dir}'.format(**env)).failed:
            run('virtualenv {environment_dir}'.format(**env))
    run('pip install -r {requirements} -E {environment}'.format(
            requirements=os.path.join(env.repo_dir, 'requirements.txt'),
            environment=env.environment_dir))

def deploy(branch='master'):
    env.branch_name = branch
    update_repo()
    update_packages()
    update_symlinks()
    print("To restart the app run 'restart'")

def restart():
    sudo('service {app_name} restart'.format(**env))

def syncdb():
    manage('syncdb')

def migrate():
    manage('migrate')

def manage(command):
    with cd(env.repo_dir):
        with prefix('source {virtualenv}'.format(virtualenv=os.path.join(
                env.environment_dir, 'bin', 'activate'))):
            run("python manage.py {command}".format(command=command))
