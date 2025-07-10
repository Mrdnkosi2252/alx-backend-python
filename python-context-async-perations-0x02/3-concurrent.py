import aiosqlite
import asyncio

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("alx_prodev.db") as db:
        async with db.execute("SELECT * FROM user_data") as cursor:
            return await cursor.fetchall()

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("alx_prodev.db") as db:
        async with db.execute("SELECT * FROM user_data WHERE age > 40") as cursor:
            return await cursor.fetchall()

# Run both queries concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n📋 All users:")
    if users:
        for user in users:
            print(user)
    else:
        print("No users found.")

    print("\n👴 Users older than 40:")
    if older_users:
        for user in older_users:
            print(user)
    else:
        print("No users older than 40.")

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
