#!/usr/bin/env bash

register_user(){ 
BLUE=$'\e[34m'
RESET=$'\e[0m'
read -p "${BLUE}Enter Username: ${RESET}" username

read -p "${BLUE}Enter Password: ${RESET}" password
hashed=$(echo -n "$password" | sha256sum | awk '{print$1}')
echo -e "$username\t$hashed" >> users.tsv
}

#check_password checks if the password is correct
check_password() {
    username=$1

    while true; do
        read -p $'\e[34mEnter password: \e[0m' password

        hashed=$(echo -n "$password" | sha256sum | awk '{print $1}')
        stored_hash=$(grep "^$username	" users.tsv | awk '{print $2}')

        if [ "$hashed" == "$stored_hash" ]; then
            BL=$'\e[32m'
            RE=$'\e[0m'
            echo -e "${BL}Login Successful!!${RE}" >&2
            return
        else
            BLU=$'\e[31m'
            RESE=$'\e[0m'
            echo -e "${BLU}Incorrect password, please re-enter.${RESE}" >&2
        fi
    done
}
#this handles login logic and register processes
authenticate(){
read -p "Enter UserName:" username
if cut -f1 users.tsv | grep -qw "$username" ;then
check_password "$username"
else
MAG=$'\e[35m'
RES=$'\e[0m'
 read -p "${MAG}Username not found.Do you want to register? (y/n):${RES}" choice 
  if [ "$choice" = "y" ] || [ "$choice" = "Y" ];then 
      register_user
  elif [ "$choice" = "n" ] || [ "$choice" = "N" ];then
      authenticate
  else
       :
  fi
fi
echo "$username"
}

#player 1&2 logins
echo "Player 1 Login"
player1=$(authenticate)

echo "Player 2 Login"
player2=$(authenticate)

# Checking if they are different users 
while [ "$player1" = "$player2" ]; do
    B=$'\e[33m'
    R=$'\e[0m'
    echo -e "${B}Both players cannot be same. Enter Player 2 again.${R}"
    player2=$(authenticate)
done

python3 game.py "$player1" "$player2"
