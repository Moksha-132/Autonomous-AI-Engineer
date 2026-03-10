import secrets
import string

class PasswordGenerator:
    """A cryptographically secure password generator."""

    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        self.all_characters = self.lowercase + self.uppercase + self.digits + self.symbols

    def generate_password(self, length=16):
        """Generates a high-entropy password of specified length."""
        if length < 8:
            raise ValueError("Password length should be at least 8 characters for security.")

        # Ensure at least one character from each required set
        password = [
            secrets.choice(self.lowercase),
            secrets.choice(self.uppercase),
            secrets.choice(self.digits),
            secrets.choice(self.symbols)
        ]

        # Fill the remaining length with random choices from all sets
        password += [secrets.choice(self.all_characters) for _ in range(length - 4)]

        # Shuffle the list to ensure character sets aren't in a predictable order
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    def generate_batch(self, count=5, length=16):
        """Generates a set of unique passwords."""
        passwords = set()
        while len(passwords) < count:
            passwords.add(self.generate_password(length))
        return list(passwords)

if __name__ == "__main__":
    generator = PasswordGenerator()

    # Demonstration 1: Standard 16-character passwords
    print("--- Batch 1: Standard 16-character passwords ---")
    batch1 = generator.generate_batch(count=3, length=16)
    for i, pwd in enumerate(batch1, 1):
        print(f"Password {i}: {pwd}")

    # Demonstration 2: High-entropy 32-character passwords
    print("\n--- Batch 2: High-entropy 32-character passwords ---")
    batch2 = generator.generate_batch(count=2, length=32)
    for i, pwd in enumerate(batch2, 4):
        print(f"Password {i}: {pwd}")

    # Demonstration 3: Single 12-character password call
    print("\n--- Batch 3: Single 12-character password ---")
    single_pwd = generator.generate_password(12)
    print(f"Password 6: {single_pwd}")
