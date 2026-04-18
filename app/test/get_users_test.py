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
# print(user_list)

classes = [{'Subject': 'Introduction to Computer Science', 'Instructor': 'Harvin Risga'}, 
 {'Subject': 'Programming Fundamentals', 'Instructor': 'Harvin Risga'}, 
 {'Subject': 'College Algebra', 'Instructor': 'Roberto Gonzales'}, 
 {'Subject': 'English Composition', 'Instructor': 'Jose Rizal'}, 
 {'Subject': 'Physics for Computing', 'Instructor': 'Harvin Risga'}]

for cl in classes:
    print(cl["Subject"])