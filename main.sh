#!/bin/bash
register_user(){ 
read -p "Enter Username:" username

read -p "Enter Password:" password
hashed=$(echo -n "$password" | sha256sum | awk '{print$1}')
echo -e "$username\t$hashed" >> users.tsv
}
#check_password checks if the password is correct 
check_password() {
    username=$1

    while true; do
        read -p "Enter password: " password
        echo ""

        hashed=$(echo -n "$password" | sha256sum | awk '{print $1}')

        stored_hash=$(grep "^$username	" users.tsv | awk '{print $2}')

        if [ "$hashed" == "$stored_hash" ]; then
            echo "Login Successful!!"
            return
        else
            echo "Incorrect password, please re-enter."
        fi
    done
}


# Checking if they are different users 
while [ "$player1" = "$player2" ]; do
    echo "Both players cannot be same. Enter Player 2 again."
    player2=$(authenticate)
done
python3 game.py "$player1" "$player2"
 
