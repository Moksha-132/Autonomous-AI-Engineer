import random
import string

def password_generator(length, special_chars=1):
    chars = string.ascii_letters + string.digits + string.punctuation
    if length < 8:
        print("Password length must be at least 8 characters.")
        return
    password = [random.choice(chars) for _ in range(length)]
    # add special character if required
    if special_chars > 0:
        password.append(random.choice(string.punctuation))
    random.shuffle(password)
    return "".join(password)

print("Generated Passwords:")
for i in range(3):
    print(f"Password {i+1}: {password_generator(12, 2)}")
