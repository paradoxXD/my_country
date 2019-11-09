def User(username, email, password):
    return f"INSERT INTO users(username,email,user_password)VALUES('{username}','{email}','{password}');"