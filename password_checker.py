import math

def analyze_characters(password):

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return {
        "lowercase": has_lower,
        "uppercase": has_upper,
        "digits": has_digit,
        "special": has_special
    }


def analyze_length(password):

    length = len(password)

    if length < 8:
        status = "Weak"
    elif length < 12:
        status = "Medium"
    else:
        status = "Strong"

    return length, status


def calculate_entropy(password):

    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26

    if any(c.isupper() for c in password):
        charset_size += 26

    if any(c.isdigit() for c in password):
        charset_size += 10

    if any(not c.isalnum() for c in password):
        charset_size += 32

    entropy = len(password) * math.log2(charset_size)

    if entropy < 40:
        strength = "Weak"
    elif entropy < 60:
        strength = "Medium"
    else:
        strength = "Strong"

    return round(entropy, 2), strength


def check_common_password(password):

    with open("common_passwords.txt", "r") as file:
        common_passwords = file.read().splitlines()

    return password.lower() in common_passwords


def calculate_final_score(password):

    score = 0
    length = len(password)

    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(not c.isalnum() for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset)

    if entropy >= 60:
        score += 2
    elif entropy >= 40:
        score += 1

    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    else:
        strength = "Strong"

    return score, strength