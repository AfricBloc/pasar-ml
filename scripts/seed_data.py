"""
Seed the Pasar ML environment with sample data for testing.
"""

def run():
    print("🌱 Seeding Pasar with mock products & users...")
    # Placeholder – later can connect to DB or backend API
    products = ["Red Sneakers", "Blue Jacket", "Vintage Watch"]
    users = ["alice@example.com", "bob@example.com"]
    print(f"✅ Created {len(products)} products and {len(users)} users.")

if __name__ == "__main__":
    run()
