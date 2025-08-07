BREST_FRONTS=(
    "bufn1"
    "bun2"
    "bun3"
)
USERNAME="u"
PASSWORD="1"


ping_host() {
    ping -c 1 -W 2 "$1" &> /dev/null
    return $?
}


for host in "${BREST_FRONTS[@]}"; do
    if ping_host "$host"; then
        sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USERNAME@$host" "sudo apt install -y brest-marketplace"
    fi
done


sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USERNAME@buarm" "sudo apt install -y apache2"


