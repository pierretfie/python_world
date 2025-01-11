import re

def check_password_strength(password):
    # Criteria for evaluation
    length_criteria = len(password) >= 8
    lowercase_criteria = bool(re.search(r'[a-z]', password))
    uppercase_criteria = bool(re.search(r'[A-Z]', password))
    digit_criteria = bool(re.search(r'\d', password))
    special_char_criteria = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    common_patterns = ["123456", "password", "qwerty", "abc123", "iloveyou"]

    # Check if password contains common patterns
    common_pattern_criteria = not any(pattern in password.lower() for pattern in common_patterns)

    # Calculate the strength score
    score = sum([
        length_criteria,
        lowercase_criteria,
        uppercase_criteria,
        digit_criteria,
        special_char_criteria,
        common_pattern_criteria,
    ])

    # Assign strength levels
    if score == 6:
        return "Strong", score
    elif 4 <= score < 6:
        return "Moderate", score
    else:
        return "Weak", score


# Input password from user
password = input("Enter a password to check its strength: ")

# Check the password strength
strength, score = check_password_strength(password)

# Display the result
print(f"Password Strength: {strength} (Score: {score}/6)")