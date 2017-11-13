#!/usr/bin/python

import urllib
import subprocess
import re
import sys
import os
sys.path.append('lib')
import charms.reactive as reactive
from charms import apt
from charmhelpers.core import hookenv
from charmhelpers.contrib.charmsupport import nrpe
from charmhelpers.core.host import rsync


NAGIOS_PLUGINS = '/usr/lib/nagios/plugins'
SUDOERS_DIR = '/etc/sudoers.d'
hooks = hookenv.Hooks()

def install_packages(packages):
    hookenv.status_set('maintenance', 'Installing software')
    hookenv.log("Installing packages")
    apt.queue_install(packages)
    apt.install_queued()

@hooks.hook('upgrade-charm')
def upgrade_charm():
    hookenv.status_set('maintenance', 'Forcing package update and reconfiguration on upgrade-charm')
    hookenv.status_set('maintenance', 'Reconfiguring')
    remove_state('raidcheck_installed')

@reactive.when_not('raidcheck_installed')
def main():
    cmd = subprocess.Popen(['lsmod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stederr = cmd.communicate()
    if re.compile('(megaraid).*').findall(stdout.decode('utf-8')):
        megaraid = True

    if os.path.isdir(NAGIOS_PLUGINS):
        rsync(os.path.join(os.getenv('CHARM_DIR'), 'files', 'nagios',
                           'check_lsi_raid'),
              os.path.join(NAGIOS_PLUGINS, 'check_lsi_raid'))
        rsync(os.path.join(os.getenv('CHARM_DIR'), 'files', 'nagios',
                           'nagios_sudoers'),
              os.path.join(SUDOERS_DIR, 'nagios_sudoers'))        

    hostname = nrpe.get_nagios_hostname()
    current_unit = nrpe.get_nagios_unit_name()
    nrpe_setup = nrpe.NRPE(hostname=hostname)

    # Install megaraid tools
    # And add megaraid nagios check
    if megaraid:
        install_packages(['storcli', 'libfile-which-perl'])

        nrpe_setup.add_check(
          shortname='lsi-raidcheck',
          description='LSI Raid Check {%s}' % current_unit,
          check_cmd=(os.path.join(NAGIOS_PLUGINS, 'check_lsi_raid'))
        )


    nrpe_setup.write()
    reactive.set_state('raidcheck_installed')
    hookenv.status_set('active', 'Unit is ready')
