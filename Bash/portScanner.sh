IP=$1
firstport=$2
lastport=$3


function portscan

{
for ((counter=$firstport; counter<=$lastport; counter++))
do
(echo >/dev/tcp/$IP/$counter) > /dev/null 2>&1 && echo “$counter open”
done
}

portscan