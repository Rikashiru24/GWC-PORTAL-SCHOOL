users = [
 {'first_name': 'Harvina', 'last_name': 'Arisgas', 'email': 'arisgaharvin2017@gmail.com'},
 {'first_name': 'Harvin', 'last_name': 'Arisga', 'email': 'harvinarisga2017@gmail.com'}, 
 {'first_name': 'Maria', 'last_name': 'Santos', 'email': 'harvinarisga21@gmail.com'}
]

user_list = []
for user in users:
    user_list.append(
        {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
        )
print(user_list[0])