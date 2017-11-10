## Using charmbox to build the charm

### Configure directories, exports and an alias for docker
```
cd git/juju/local && mkdir -p {data,charms,interfaces,layers}
export JUJU_BASE=$HOME/git/juju/local
export JUJU_DATA=$JUJU_BASE/data
export JUJU_REPOSITORY=$JUJU_BASE/charms
export INTERFACE_PATH=$JUJU_BASE/interfaces
export LAYER_PATH=$JUJU_BASE/layers

alias dock_juju="sudo docker run --rm --name juju_dev -t -i -v $JUJU_DATA:/home/ubuntu/.local/share/juju -v $JUJU_REPOSITORY:/home/ubuntu/charms -v $LAYER_PATH:/home/ubuntu/charms/layers -v $INTERFACE_PATH:/home/ubuntu/charms/interfaces jujusolutions/charmbox"
```

### Clone the needed repositories to the correct paths
```
git clone https://github.com/MartinHell/charm-designate-horizon-dashboard.git $JUJU_REPOSITORY
git clone https://github.com/MartinHell/charm-interface-dashboard-plugin.git $INTERFACE_PATH
```

### Rename the interface charm directory
```
mv $INTERFACE_PATH/charm-interface-dashboard-plugin $INTERFACE_PATH/interface-dashboard-plugin
```

### Run docker and build the charm
```
dock_juju
cd charms/MY_CHARM
charm build
```
