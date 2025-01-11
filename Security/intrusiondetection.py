import re
from collections import defaultdict

# Sample suspicious IP list
SUSPICIOUS_IPS = ["192.168.1.100", "10.0.0.1"]

# Rules
FAILED_LOGIN_THRESHOLD = 5  # Define the number of failed logins allowed
REQUEST_THRESHOLD = 100     # Define max requests per IP

# Function to parse log file
def analyze_logs(log_file):
    failed_logins = defaultdict(int)
    request_counts = defaultdict(int)
    alerts = []

    with open(log_file, "r") as file:
        for line in file:
            # Check for failed login attempts
            if "failed login" in line.lower():
                ip = extract_ip(line)
                if ip:
                    failed_logins[ip] += 1
                    if failed_logins[ip] > FAILED_LOGIN_THRESHOLD:
                        alerts.append(f"Alert: Too many failed login attempts from IP {ip}")

            # Count requests from each IP
            ip = extract_ip(line)
            if ip:
                request_counts[ip] += 1
                if request_counts[ip] > REQUEST_THRESHOLD:
                    alerts.append(f"Alert: High traffic detected from IP {ip}")

            # Check for suspicious IPs
            if ip in SUSPICIOUS_IPS:
                alerts.append(f"Alert: Suspicious IP access detected from {ip}")

    return alerts

# Function to extract IP addresses
def extract_ip(log_line):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_line)
    return match.group(0) if match else None

# Main function
if __name__ == "__main__":
    log_file = "network_logs.txt"  # Replace with your log file path
    alerts = analyze_logs(log_file)

    if alerts:
        print("Intrusion Detection Alerts:")
        for alert in alerts:
            print(alert)
    else:
        print("No suspicious activities