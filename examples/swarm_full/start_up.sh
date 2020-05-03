# Assumed to be in a VM.
# See

eval $(docker-machine env default)

docker-machine create --driver virtualbox default

docker-machine create manager
docker-machine create agent1
docker-machine create agent2

eval `docker-machine env manager`

docker swarm init --advertise-addr `docker-machine ip manager`

docker-machine ssh agent1 docker swarm join --token `docker swarm join-token -q worker` `docker-machine ip manager`:2377
docker-machine ssh agent2 docker swarm join --token `docker swarm join-token -q worker` `docker-machine ip manager`:2377

# For elasticsearch to not give Out of Memory errors, we need set vm.max_map_count of the kernel of VMs to
# atleast 262144. To do this, run the following commands.

docker-machine ssh manager sudo sysctl -w vm.max_map_count=262144
docker-machine ssh agent1 sudo sysctl -w vm.max_map_count=262144
docker-machine ssh agent2 sudo sysctl -w vm.max_map_count=262144


# Start program

docker stack deploy -c docker-stack.yml elk

open http://`docker-machine ip manager`

docker stack deploy -c amms-stack.yml amms-serving