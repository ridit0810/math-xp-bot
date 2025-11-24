import json
from discord.ext import commands
import os

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "./data/users.json"
        self.data = {}
        
        # Ensure data directory exists
        if not os.path.exists("./data"):
            os.makedirs("./data")

        # Load data on startup
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file):
            self.data = {}
            self.save_data()
        else:
            try:
                with open(self.file, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}

    def save_data(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_xp(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {"xp": 0, "level": 1}

        self.data[user_id]["xp"] += amount

        # Leveling formula
        level = self.data[user_id]["level"]
        xp = self.data[user_id]["xp"]
        required = level * 100

        if xp >= required:
            self.data[user_id]["level"] += 1
            self.data[user_id]["xp"] = xp - required
            self.save_data()
            return True  # leveled up

        self.save_data()
        return False

    def get_stats(self, user_id):
        return self.data.get(str(user_id), {"xp": 0, "level": 1})

async def setup(bot):
    await bot.add_cog(XPSystem(bot))
