import re
import math
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# -----------------------------
# LOAD BREACHED PASSWORDS
# -----------------------------

def load_common_passwords(file_path):
    try:
        with open(file_path, "r", encoding="latin-1") as file:
            return set(line.strip().lower() for line in file)
    except FileNotFoundError:
        print(Fore.RED + "[ERROR] rockyou.txt not found.")
        return set()


COMMON_PASSWORDS = load_common_passwords("rockyou.txt")

# -----------------------------
# ENTROPY CALCULATION
# -----------------------------

def calculate_entropy(password):
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26

    if re.search(r"[A-Z]", password):
        pool += 26

    if re.search(r"[0-9]", password):
        pool += 10

    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

# -----------------------------
# CRACK TIME ESTIMATION
# -----------------------------

def estimate_crack_time(entropy):
    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec

    seconds = (2 ** entropy) / guesses_per_second

    if seconds < 60:
        return f"{round(seconds)} seconds"

    elif seconds < 3600:
        return f"{round(seconds / 60)} minutes"

    elif seconds < 86400:
        return f"{round(seconds / 3600)} hours"

    elif seconds < 31536000:
        return f"{round(seconds / 86400)} days"

    else:
        return f"{round(seconds / 31536000)} years"

# -----------------------------
# PASSWORD ANALYSIS
# -----------------------------

def analyze_password(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short.")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Number Check
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # Symbol Check
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        feedback.append("Add special symbols.")

    # Breached Password Check
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("This password has appeared in known data breaches.")

    # Repeated Character Check
    if re.search(r"(.)\1{2,}", password):
        feedback.append("Too many repeated characters.")

    # Entropy
    entropy = calculate_entropy(password)

    # Crack Time
    crack_time = estimate_crack_time(entropy)

    # Strength Rating
    if score <= 2:
        strength = "Weak"
        color = Fore.RED

    elif score <= 4:
        strength = "Medium"
        color = Fore.YELLOW

    else:
        strength = "Strong"
        color = Fore.GREEN

    return {
        "strength": strength,
        "score": score,
        "entropy": entropy,
        "feedback": feedback,
        "crack_time": crack_time,
        "color": color
    }

# -----------------------------
# MAIN PROGRAM
# -----------------------------

print(Fore.CYAN + """
====================================
        ENTROPYSCAN v1.0
====================================
""")

password = input("Enter password: ")

result = analyze_password(password)

print("\n" + Fore.CYAN + "========== PASSWORD ANALYSIS ==========\n")

print(f"Strength   : {result['color']}{result['strength']}{Style.RESET_ALL}")
print(f"Score      : {result['score']}/6")
print(f"Entropy    : {result['entropy']} bits")
print(f"Crack Time : {result['crack_time']}")

print("\nIssues Found:")

if result["feedback"]:
    for item in result["feedback"]:
        print(Fore.RED + f"- {item}")
else:
    print(Fore.GREEN + "- No major issues detected.")

print(Fore.CYAN + "\n======================================")