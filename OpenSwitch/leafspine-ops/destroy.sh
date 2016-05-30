switches=(leaf1 leaf2 leaf3 leaf4 spine1 spine2)
leafs=(leaf1 leaf2 leaf3 leaf4)
spines=(spine1 spine2)

echo Destroy switches
for switch in "${switches[@]}"
do
  docker rm -f ${switch}
done

echo
echo Destroy OOB network
docker network rm oob

echo Destroy networks
for leaf in "${leafs[@]}"
do
  for spine in "${spines[@]}"
  do
    echo
    echo Destroying network ${leaf}_${spine}
    docker network rm ${leaf}_${spine}
  done
done

echo
echo Environment destroyed

