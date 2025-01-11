import re

# List of suspicious keywords
SUSPICIOUS_KEYWORDS = ["login", "secure", "bank", "verify", "account", "update"]

# Function to analyze URL
def is_phishing_url(url):
    # Flag to identify phishing
    phishing_score = 0

    # Check if URL contains suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url.lower():
            phishing_score += 1

    # Check for IP address in URL
    if re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', url):
        phishing_score += 1

    # Check for excessive length
    if len(url) > 75:
        phishing_score += 1

    # Check for multiple special characters
    if url.count('-') > 3 or url.count('.') > 5:
        phishing_score += 1

    # Final decision
    if phishing_score >= 3:
        return True, phishing_score
    else:
        return False, phishing_score


# Test URLs
urls = [
    "http://secure-login-bank.com",
    "http://192.168.1.1/login",
    "https://google.com",
    "http://very-long-url-with-many-characters-and-suspicious-keywords-login-update.com",
]

# Analyze each URL
for url in urls:
    is_phishing, score = is_phishing_url(url)
    print(f"URL: {url}")
    print(f"Phishing: {'Yes' if is_phishing else 'No'} (Score: {score}/4)\n")