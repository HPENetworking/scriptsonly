switches=(leaf1 leaf2 leaf3 leaf4 spine1 spine2)
leafs=(leaf1 leaf2 leaf3 leaf4)
spines=(spine1 spine2)
dockerimage="cloudsvet/openswitch:0525"

echo Create OOB network
docker network create oob

echo Run switches
for switch in "${switches[@]}"
do
  echo
  echo Run ${switch}
  docker run --privileged -d -v /tmp:/tmp -v /dev/log:/dev/log -v /sys/fs/cgroup:/sys/fs/cgroup -h ${switch} --name ${switch} --net oob ${dockerimage} /sbin/init
done

echo Create networks
for leaf in "${leafs[@]}"
do
  for spine in "${spines[@]}"
  do
    echo
    echo Creating and attaching network ${leaf}_${spine}
    docker network create ${leaf}_${spine}
    docker network connect ${leaf}_${spine} ${leaf}
    docker network connect ${leaf}_${spine} ${spine}
  done
done

echo
echo Move leaf interfaces to OpenSwitch namespace
for leaf in "${leafs[@]}"
do
  echo ${leaf}
  for index in ${!spines[@]}
  do
    let "port = $index + 1"
    docker exec ${leaf} ip link set eth${port} down
    docker exec ${leaf} ip link set eth${port} name ${port}
    docker exec ${leaf} ip link set ${port} netns swns
  done
done

echo
echo Move spine interfaces to OpenSwitch namespace
for spine in "${spines[@]}"
do
  echo ${spine}
  for index in ${!leafs[@]}
  do
    let "port = $index + 1"
    docker exec ${spine} ip link set eth${port} down
    docker exec ${spine} ip link set eth${port} name ${port}
    docker exec ${spine} ip link set ${port} netns swns
  done
done

echo
echo Generate Ansible host file \(hosts in current folder\)
echo "[leafs]" > hosts
for leaf in "${leafs[@]}"
do
  ip=$(docker inspect --format='{{json .NetworkSettings.Networks.oob.IPAddress}}' ${leaf})
  echo ${leaf} ansible_host=${ip//\"/} ansible_port=22 >> hosts
done

echo >> hosts
echo "[spines]" >> hosts
for spine in "${spines[@]}"
do
  ip=$(docker inspect --format='{{json .NetworkSettings.Networks.oob.IPAddress}}' ${spine})
  echo ${spine} ansible_host=${ip//\"/} ansible_port=22 >> hosts
done

cat hosts

echo
echo Network is ready
