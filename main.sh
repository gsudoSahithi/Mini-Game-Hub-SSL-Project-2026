authenticate(){
read -p "Enter UserName:" username
if cut -f1 users.tsv | grep -qw "$username" ;then
check_password "$username"
else
 read -p "Username not found.Do you want to register? (y/n):" choice 
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
echo "Player 1 Login"
player1=$(authenticate)

echo "Player 2 Login"
player2=$(authenticate)
