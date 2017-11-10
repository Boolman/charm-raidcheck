#!/usr/bin/python

import urllib
import subprocess
import re
import charms.reactive as reactive
from charms import apt
from charmhelpers.core import hookenv
from charmhelpers.contrib.charmsupport import nrpe
from charmhelpers.core.host import rsync


hooks = hookenv.Hooks()

def install_packages(packages):
    hookenv.status_set('maintenance', 'Installing software')
    hookenv.log("Installing packages")
    apt.queue_install(packages)
    apt.install_queued()

@hooks.hook('upgrade-charm')
def upgrade-charm():
    main()

@hooks.hook('nrpe-external-master-relation-joined',
            'nrpe-external-master-relation-changed')
def main():
    cmd = subprocess.Popen(['lsmod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stederr = cmd.communicate()
    if re.compile('(megaraid).*').findall(stdout.decode('utf-8')):
        megaraid = True

    hostname = nrpe.get_nagios_hostname()
    current_unit = nrpe.get_nagios_unit_name()
    nrpe_setup = nrpe.NRPE(hostname=hostname)
    if os.path.isdir(NAGIOS_PLUGINS):
        rsync(os.path.join(os.getenv('CHARM_DIR'), 'files', 'nagios',
                           'check_lsi_raid'),
              os.path.join(NAGIOS_PLUGINS, 'check_lsi_raid'))

    if megaraid:
        install_packages(['storcli', 'libfile-which-perl'])
        add_lsi_check()

    nrpe_setup.write()


def add_lsi_check():
    nrpe_setup.add_check(
        shortname='lsi-raidcheck',
        description='LSI Raid Check {%s}' % current_unit,
        check_cmd=(os.path.join(NAGIOS_PLUGINS, 'check_lsi_raid'))
    )




