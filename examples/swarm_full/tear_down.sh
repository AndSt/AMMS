

docker stack rm elk
docker stack rm amms-serving

docker-machine stop manager agent1 agent2
docker-machine rm -f manager agent1 agent2

