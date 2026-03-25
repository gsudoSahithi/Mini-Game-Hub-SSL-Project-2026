register_user(){ 
read -p "Enter Username:" username
if cut -f1 users.tsv | grep -qw "$username" ;then
 echo "User Name already exists! Try Again"
 register_user
fi
read -sp "Enter Password:" password
hashed=$(echo -n "$password" | sha256sum | awk "$1")
echo "$username\t$hashed" >> users.tsv
}
