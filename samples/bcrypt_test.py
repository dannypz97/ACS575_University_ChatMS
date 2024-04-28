import bcrypt

# Password to Hash
original_password = b'root'

# Generating Salt
salt = bcrypt.gensalt()

# Hashing Password
hash_password = bcrypt.hashpw(
    password=original_password,
    salt=salt
)

print('Hash: ', hash_password)

# User-provided Password
user_password = b'root'


# Checking Password
check = bcrypt.checkpw(
    password=user_password,
    hashed_password=hash_password
)

print()

# Verifying the Password
if check:
    print("Valid Credential!!")
else:
    print("Invalid Credential!!")