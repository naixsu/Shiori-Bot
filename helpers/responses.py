from discord import Message

async def send_message(ctx: Message, message: str) -> None:
    if not message:
        print("Message was empty because intents were not enabled")
        return

    try:
        await ctx.delete()
        await ctx.channel.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")