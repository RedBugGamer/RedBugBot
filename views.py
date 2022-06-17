import datetime
from typing import Coroutine
import nextcord
import requests
from sqlite3 import Connection, Cursor
import asyncio
import json
from utilitie import *
from vars import *


class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):

        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id in blockedusers:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description="Acces denied - You have been blocked", color=0xE74C3C
                )
            )
            return
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "O ist dran"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "X ist dran"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X gewinnt!"
            elif winner == view.O:
                content = "O gewinnt!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: list[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + \
                self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Schiffefeld(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="⠀", style=nextcord.ButtonStyle.blurple)
    async def Spielfeld1(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Dein spielfeld XD", ephemeral=True)

    @nextcord.ui.button(label="⠀", style=nextcord.ButtonStyle.blurple)
    async def Spielfeld2(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Dein spielfeld XD", ephemeral=True)

    @nextcord.ui.button(label="⠀", style=nextcord.ButtonStyle.blurple, row=2)
    async def Spielfeld3(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Dein spielfeld XD", ephemeral=True)


class Schiffetot(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Player1")
    async def Field1(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message(
            "Player1", ephemeral=True, view=Schiffefeld()
        )
        button.disabled = True
        await interaction.edit(view=self)

    @nextcord.ui.button(label="Player2")
    async def Field2(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message(
            "Player2", ephemeral=True, view=Schiffefeld()
        )
        button.disabled = True
        await interaction.edit(view=self)


class lichtschalter(nextcord.ui.View):
    def __init__(self, lichtid: str):
        self.lichtid = lichtid
        super().__init__()

    @nextcord.ui.button(emoji="💡")
    async def lichtschalter(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if interaction.user.id in [redbuggamer, 381905896546107392, 772467937436893205]:
            requests.get(
                f"http://raspberrypi:8088/rest/devices/{self.lichtid}/methods/1"
            )
            await interaction.response.send_message(
                f"licht {self.lichtid} getoggelt", ephemeral=True
            )
        else:
            await interaction.response.send_message("Keine permission", ephemeral=True)


class mypoll(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="0", style=nextcord.ButtonStyle.green, custom_id="poll:up", emoji="✅"
    )
    async def pollup(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if await check_developer_mode_interaction(interaction):
            return
        if interaction.user.id in blockedusers:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description="Acces denied - You have been blocked", color=0xE74C3C
                )
            )
            return
        id1 = interaction.message.id
        # print(id1)
        # print(cursor.execute("SELECT * FROM polls WHERE id = ?", (id1,)).fetchall())
        try:
            id, up, down, owner, voted, expires = cursor.execute(
                "SELECT * FROM polls WHERE id = ?", (id1,)
            ).fetchall()[0]
            output = {}
            if not str(interaction.user.id) in voted.split("-") and not str(
                owner
            ) == str(interaction.user.id):
                voters = voted.split("-")
                voters.append(str(interaction.user.id))
                output["voted"] = "-".join(voters)
                button.label = str(up + 1)
                cursor.execute(
                    "UPDATE polls SET up = ?, voted = ?,expires = ? WHERE id = ?",
                    (up + 1, output["voted"], id1, datetime.datetime.now()),
                )
                connection.commit()
                self.children[1].label = str(
                    int(self.children[0].label) - int(self.children[2].label)
                )
                await interaction.edit(view=self)
            else:
                id, up, down, owner, voted, expires = cursor.execute(
                    "SELECT * FROM polls WHERE id = ?", (id1,)
                ).fetchall()[0]
                self.children[0].label = str(up)
                self.children[1].label = str(up-down)
                self.children[2].label = str(down)
                await interaction.response.send_message(
                    "Du hast leider schon gevotet oder bist owner", ephemeral=True
                )
                await interaction.message.edit(view=self)
        except IndexError:
            await interaction.response.send_message(
                "Sorry, aber der Poll ist expired", ephemeral=True
            )

    @nextcord.ui.button(
        label="0",
        style=nextcord.ButtonStyle.grey,
        disabled=True,
        custom_id="poll:ratio",
    )
    async def ratio(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Lol", ephemeral=True)

    @nextcord.ui.button(
        label="0", style=nextcord.ButtonStyle.red, custom_id="poll:down", emoji="❌"
    )
    async def polldown(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if await check_developer_mode_interaction(interaction):
            return
        if interaction.user.id in blockedusers:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description="Acces denied - You have been blocked", color=0xE74C3C
                )
            )
            return
        id1 = interaction.message.id
        # print(id1)
        # print(cursor.execute("SELECT * FROM polls WHERE id = ?", (id1,)).fetchall())
        try:
            id, up, down, owner, voted, expires = cursor.execute(
                "SELECT * FROM polls WHERE id = ?", (id1,)
            ).fetchall()[0]
            output = {}
            if not str(interaction.user.id) in voted.split("-") and not str(
                owner
            ) == str(interaction.user.id):
                voters = voted.split("-")
                voters.append(str(interaction.user.id))
                output["voted"] = "-".join(voters)
                button.label = str(down + 1)
                cursor.execute(
                    "UPDATE polls SET down = ?, voted = ?,expires = ? WHERE id = ?",
                    (down + 1, output["voted"], id1, datetime.datetime.now()),
                )
                connection.commit()
                self.children[1].label = str(
                    int(self.children[0].label) - int(self.children[2].label)
                )
                await interaction.edit(view=self)
            else:
                id, up, down, owner, voted, expires = cursor.execute(
                    "SELECT * FROM polls WHERE id = ?", (id1,)
                ).fetchall()[0]
                self.children[0].label = str(up)
                self.children[1].label = str(up-down)
                self.children[2].label = str(down)
                await interaction.response.send_message(
                    "Du hast leider schon gevotet oder bist owner", ephemeral=True
                )
                await interaction.message.edit(view=self)
        except IndexError:
            await interaction.response.send_message(
                "Sorry, aber der Poll ist expired", ephemeral=True
            )

    @nextcord.ui.button(label="#", style=nextcord.ButtonStyle.gray, custom_id="poll:thread")
    async def thread(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.message.thread == None:
            button.disabled = True
            await interaction.message.edit(view=self)
            t = await interaction.message.create_thread(name="Discussion")
            await t.add_user(interaction.user)
    # @nextcord.ui.button(label = "edit",style = nextcord.ButtonStyle.blurple,custom_id="poll:edit")
    # async def edit(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
    #     try:
    #         id, up, down, owner, voted, expires = cursor.execute(
    #                 "SELECT * FROM polls WHERE id = ?", (interaction.message.id,)
    #             ).fetchall()[0]
    #         if str(interaction.user.id) == str(owner):
    #             await interaction.response.send_message("Gib bitte jetzt eine ")
    #     except IndexError:
    #         await interaction.response.send_message(
    #             "Sorry, aber der Poll ist expired", ephemeral=True
    #         )


class EmbedBuilder(nextcord.ui.View):
    def __init__(self, embed: dict, owner: int, description_msg: nextcord.Message):
        super().__init__(timeout=None)
        self.embed = embed
        self.owner = owner
        self.description_msg = description_msg

    @nextcord.ui.button(label="Send", style=nextcord.ButtonStyle.green)
    async def send(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.owner == interaction.user.id:
            await interaction.channel.send(embed=nextcord.Embed.from_dict(self.embed))
            await interaction.message.delete()
            await self.description_msg.delete()
            self.stop()
        else:
            await interaction.response.send_message(
                "Du bist halt kein Owner, weißt du...", ephemeral=True
            )

    @nextcord.ui.button(label="Edit")
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner:
            await interaction.response.send_message(
                "Du bist halt kein Owner, weißt du...", ephemeral=True
            )
            return
        await interaction.response.send_message(
            "Du kannst jetzt key=value in den chat schreiben", ephemeral=True
        )
        try:
            msg: nextcord.Message = await client.wait_for(
                "message", timeout=30, check=lambda m: m.author == interaction.user
            )
            if len(msg.content.split("=")) == 2:
                e = nextcord.Embed.from_dict(self.embed)
                key = msg.content.split("=")[0]
                value = msg.content.split("=")[1]
                d = [
                    "titel",
                    "description",
                    "color",
                    "footer",
                    "image",
                    "thumbnail",
                ]
                colors = {
                    "red": nextcord.Color.red(),
                    "orange": nextcord.Color.orange(),
                    "yellow": nextcord.Color.yellow(),
                    "green": nextcord.Color.green(),
                    "blue": nextcord.Color.blue(),
                    "white": nextcord.Color.from_rgb(255, 255, 255),
                    "black": nextcord.Color.from_rgb(0, 0, 0),
                }
                if key in d:
                    match key:
                        case "titel":
                            e.title = value
                        case "description":
                            e.description = value
                        case "color":
                            if value in colors:
                                d1 = e.to_dict()
                                d1["color"] = int(colors[value])
                                e = nextcord.Embed.from_dict(d1)
                        case "footer":
                            e.set_footer(value)
                        case "image":
                            e.set_image(value)
                        case "thumbnail":
                            e.set_thumbnail(value)
                    await interaction.message.edit(embed=e)
                    self.embed = e.to_dict()
                else:
                    await msg.reply(
                        "Du musst einen echten Parameter angeben", delete_after=5
                    )

            else:
                await msg.reply("Du musst ein key=value Paar angeben", delete_after=5)
        except asyncio.TimeoutError:
            await interaction.message.channel.send(
                "Sorry du warst nicht schnell genug", delete_after=5
            )
        await msg.delete()

    @nextcord.ui.button(label="Add Field")
    async def field_add(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if self.owner == interaction.user.id:
            await interaction.response.send_message(
                "Gib jetzt bitte Titel=Beschreibung an", ephemeral=True
            )
            try:
                msg: nextcord.Message = await client.wait_for(
                    "message", timeout=30, check=lambda m: m.author == interaction.user
                )
                await msg.delete()
                if len(msg.content.split("=")) == 2:
                    titel = msg.content.split("=")[0]
                    description = msg.content.split("=")[1]
                    e = nextcord.Embed.from_dict(self.embed)
                    e.add_field(name=titel, value=description, inline=False)
                    self.embed = e.to_dict()
                await interaction.message.edit(embed=e)
            except asyncio.TimeoutError:
                await interaction.message.channel.send(
                    "Sorry du warst nicht schnell genug", delete_after=5
                )

        else:
            await interaction.response.send_message(
                "Du bist halt kein Owner, weißt du...", ephemeral=True
            )

    @nextcord.ui.button(label="Copy")
    async def copy(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.owner == interaction.user.id:
            response = json.dumps(self.embed)
            a = cursor.execute("SELECT * FROM embeds").fetchall()
            newid = list(
                set(range(0, len(a) + 1)).difference(i[0] for i in a))[0]
            cursor.execute(
                "INSERT INTO embeds VALUES (?,?,?)",
                (
                    newid,
                    response,
                    datetime.datetime.now() + datetime.timedelta(minutes=10),
                ),
            )
            connection.commit()
            await interaction.response.send_message(f"Die Einbettung: `T!deploy {newid}` (gilt 10 Minuten)")
        else:
            await interaction.response.send_message(
                "Du bist halt kein Owner, weißt du...", ephemeral=True
            )

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if self.owner == interaction.user.id:
            await interaction.message.delete()
            await self.description_msg.delete()
            self.stop()
        else:
            await interaction.response.send_message(
                "Du bist halt kein Owner, weißt du...", ephemeral=True
            )

# class ConfirmButton(nextcord.ui.View):
#     def __init__(self,user:nextcord.User,ok:Coroutine,cancel:Coroutine):
#         self.user = user
#         self.ok = ok
#         self.cancel = cancel
#         super().__init__(timeout=None)
    
#     @nextcord.ui.button(label = "Ok", style = nextcord.ButtonStyle.green)
#     async def ok_(self,button:nextcord.ui.Button, interaction: nextcord.Interaction):
#         await self.ok
#         for i in self.children:
#             i.disabled = True
#         await interaction.edit(view=self)
#         self.stop()
#     @nextcord.ui.button(label = "Cancel", style = nextcord.ButtonStyle.red)
#     async def cancel_(self,button: nextcord.ui.Button,interaction: nextcord.Interaction):
#         await self.cancel
#         for i in self.children:
#             i.disabled = True
#         await interaction.edit(view=self)
#         self.stop()