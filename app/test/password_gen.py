import random
import string

password = "".join(random.choices(string.ascii_letters + string.digits, k=6))
print(password)