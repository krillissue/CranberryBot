from typing import Any
import json, os, tools.random, time


class DB:
    def __init__(self, path: str = "db.json") -> None:
        self.path = path
        self.data: dict[str, dict] = {
            "leaderboards": {},
            "msg_history": {},
            "polls": {},
            "warns": {},
        }

        if not os.path.exists(self.path):
            with open(self.path, "w") as fp:
                json.dump(self.data, fp)

    def save(self) -> None:
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def load(self) -> None:
        with open(self.path) as fp:
            self.data = json.load(fp)

    def add_win(self, leaderboard: str, player_id: int) -> None:
        self.load()

        if not self.data["leaderboards"].get(leaderboard):
            self.data["leaderboards"][leaderboard] = {}

        if not self.data["leaderboards"][leaderboard].get(str(player_id)):
            self.data["leaderboards"][leaderboard][str(player_id)] = 0

        self.data["leaderboards"][leaderboard][str(player_id)] += 1

        self.save()

    def get_leaderboard(self, leaderboard: str) -> dict[str, int]:
        self.load()

        if not self.data["leaderboards"].get(leaderboard):
            return {}

        return dict(
            sorted(
                self.data["leaderboards"][leaderboard].items(),
                key=(lambda item: item[1]),
                reverse=True,
            )
        )

    def set_msg_history(self, id: int, history: str):
        self.load()
        self.data["msg_history"][str(id)] = history
        self.save()

    def get_msg_history(self, id: int) -> str:
        self.load()
        return self.data["msg_history"].get(str(id), "")

    def add_msg(self, id: int, name: str, msg: str, res: str, images: list[str]):
        self.load()

        images = [
            f"\nAttached image #{i} description: {images[i]}"
            for i in range(len(images))
        ]
        entry = f"{name}: {msg}\nCranberryBot: {res}{''.join(images)}"

        if not self.data["msg_history"].get(str(id), ""):
            self.data["msg_history"][str(id)] = entry
            self.save()
            return

        self.data["msg_history"][str(id)] += f"\n{entry}"
        self.save()

    def clear_msg_history(self, id: int):
        self.load()
        self.data["msg_history"][str(id)] = ""
        self.save()

    def clear_global_msg_history(self):
        self.load()
        self.data["msg_history"] = {}
        self.save()

    def create_poll(self, options: list[int], msg: str) -> str:
        self.load()
        id = tools.random.id()
        self.data["polls"][id] = {"msg": msg, "options": options, "votes": {}}
        self.save()
        return id

    def set_vote(self, poll_id: str, user_id: int, option: int):
        self.load()
        self.data["polls"][poll_id]["votes"][str(user_id)] = option
        self.save()

    def get_votes(self, poll_id: str) -> dict[str, int]:
        self.load()
        votes = {}

        for option in self.data["polls"][poll_id]["options"]:
            votes[str(option)] = 0

        for vote in self.data["polls"][poll_id]["votes"].values():
            votes[str(vote)] += 1

        return votes

    def remove_vote(self, poll_id: str, user_id: int):
        self.load()

        try:
            del self.data["polls"][poll_id]["votes"][str(user_id)]
        except:
            pass

        self.save()

    def get_warns(self, user_id: int):
        self.load()

        user_warns = self.data["warns"].get(str(user_id), {})

        for key in user_warns:
            if time.time() > user_warns[key]["expires_in"]:
                del user_warns[key]

        return user_warns

    def set_warns(self, user_id: int, warns: dict):
        self.load()
        self.data["warns"][str(user_id)] = warns
        self.save()

    def remove_warn(self, user_id: int, warn_id: str) -> bool:
        user_warns = self.get_warns(user_id)

        if not user_warns.get(warn_id):
            return False

        del user_warns[warn_id]
        self.set_warns(user_id, user_warns)
        return True

    def add_warn(self, user_id: int, reason: str) -> str:
        self.load()

        id = tools.random.id(8)

        if not self.data["warns"].get(str(user_id)):
            self.data["warns"][str(user_id)] = {}

        self.data["warns"][str(user_id)][id] = {
            "expires_in": time.time() + (30 * 24 * 60 * 60),
            "reason": reason,
        }

        self.save()

        return id
