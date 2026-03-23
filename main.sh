register_user(){
read -p "Enter Username:" username
read -sp "Enter Password:" password
hashed=$(echo -n "$password" | sha256sum | awk "$1")
echo "$username-$hashed" > users.tsv
}
