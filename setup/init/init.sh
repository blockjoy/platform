#!/bin/bash

# Wait for the DB to be ready (using wait-for-it or similar)
#./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up"

# Prompt for interactive input
echo
read -p "Enter your email: " email
read -p "Enter your first name: " fname
read -p "Enter your last name: " lname
read -s -p "Enter your password: " password
echo  # move to a new line after password input

# Run the Python script with the interactive inputs
python database-setup.py -e "$email" -f "$fname" -l "$lname" -p "$password"

printf "\n***Initial User Set is Complete***\n"
printf "\n----------Credentials----------\n"
printf "Admin User: \t\t$email\n"
printf "Non-Admin User: \tuser@example.com\n"
printf "Both user passwords are set to what you defined.\n"

printf "The Blockvisor stack setup is complete.  You can now access it at http://<server_ip>\n\n"

