from __future__ import print_function
from datetime import datetime

from fabric.api import local, run, env, cd, sudo

env.hosts = ['deploy@ubuntu']

def archive(branch='master'):
    with cd("~/bigbrother"):
        run("git pull")
        run("git archive --format zip --output archive.zip {0}".format(branch))

def expand(target='/var/apps/bigbrother/releases/'):
    folder = datetime.now().strftime('%Y%m%d%H%M%S')
    sudo("mkdir -p {0}{1}/bigbrother".format(target, folder))
    sudo("unzip ~/bigbrother/archive.zip -d {0}{1}/bigbrother".format(target,
        folder))
    run("rm ~/bigbrother/archive.zip")
    hack_local_files(target, folder)
    update_symlinks(target, folder)

def hack_local_files(target, folder):
    current = target + folder + '/bigbrother'
    sudo("mv {0}/settings.py {0}/settings.py.orig".format(current))
    sudo("cp {0}current/bigbrother/settings.py {1}/settings.py".format(
        target, current))

def update_symlinks(target, folder):
    current = target + folder
    previous = target + 'current'
    sudo("ln -s /lib/django-trunk/django/contrib/admin/static/admin "
        "{0}/bigbrother/media/admin".format(current))
    sudo("rm {0}".format(previous))
    sudo("ln -s {0} {1}".format(current, previous))


def reload_apache():
    sudo("/etc/init.d/apache2 reload")

def deploy(branch=None, expand_target=None):
    if branch is None:
        archive()
    else:
        archive(branch)
    if expand_target is None:
        expand()
    else:
        expand(expand_target)
    reload_apache()
