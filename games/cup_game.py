from typing import Callable
from discord.ext.commands import Context
import discord
import tools


class CupButton(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        this_cup: int,
        correct_cup: int,
        cups: list[discord.ButtonStyle],
        slurs: list[str] = [
            "NIGGA",
            "NIGGER",
            "RETARD",
            "CHING CHONG",
            "CHINK",
            "CHINKY",
        ],
        ctx: Context,
        kill_view: Callable,
    ) -> None:
        self._this_cup = this_cup
        self._correct_cup = correct_cup
        self._cups = cups
        self._slurs = slurs
        self._ctx = ctx
        self._kill_view = kill_view

        super().__init__(
            style=style,
            emoji="<:cup:1189263945744261121>",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if self._ctx.author != interaction.user:
            await interaction.response.send_message(
                f"{tools.random.choice(self._slurs)} THIS ISNT YOUR GAME",
                ephemeral=True,
            )

            return

        view = discord.ui.View(timeout=1)

        for i in range(len(self._cups)):
            if self._correct_cup == i:
                view.add_item(
                    discord.ui.Button(
                        style=self._cups[i],
                        emoji="🥎",
                        disabled=True,
                    )
                )

                continue

            if self._this_cup == i and self._correct_cup != i:
                view.add_item(
                    discord.ui.Button(
                        style=self._cups[i],
                        emoji="❌",
                        disabled=True,
                    )
                )

                continue

            view.add_item(
                discord.ui.Button(
                    style=self._cups[i],
                    emoji="<:cup:1189263945744261121>",
                    disabled=True,
                )
            )

        if self._this_cup == self._correct_cup:
            await interaction.response.edit_message(
                content=f"ok good job, it was indeed cup {self._this_cup + 1} :thumbsup:",
                view=view,
            )

            self._kill_view()
            return

        await interaction.response.edit_message(
            content=f"{tools.random.choice(self._slurs)} IT WAS CUP {self._correct_cup + 1}",
            view=view,
        )

        self._kill_view()


class CupGame(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 10,
        cups: list[discord.ButtonStyle] = [
            discord.ButtonStyle.red,
            discord.ButtonStyle.green,
            discord.ButtonStyle.blurple,
        ],
        ctx: Context,
        msg: discord.Message,
    ) -> None:
        self._cups = cups
        self._correct_cup = tools.random.randint(0, len(self._cups) - 1)
        self._ctx = ctx
        self._msg = msg

        super().__init__(timeout=timeout)

        for i in range(len(self._cups)):
            self.add_item(
                CupButton(
                    style=self._cups[i],
                    this_cup=i,
                    correct_cup=self._correct_cup,
                    ctx=self._ctx,
                    cups=self._cups,
                    kill_view=self.stop,
                )
            )

    async def on_timeout(self) -> None:
        view = discord.ui.View(timeout=1)

        for i in range(len(self._cups)):
            view.add_item(
                discord.ui.Button(
                    style=self._cups[i],
                    emoji="<:cup:1189263945744261121>",
                    disabled=True,
                )
            )

        await self._msg.edit(
            content="bro you really took THAT long to press a FUCKING BUTTON??",
            view=view,
        )