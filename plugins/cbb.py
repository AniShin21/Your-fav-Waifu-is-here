from database.database import *


@Bot.on_callback_query()
async def cb_handler(client, query):
    """Handle callback queries for giveaway and verification."""
    data = query.data
    user = query.from_user

    if data == "giveaway":
        # Check if user is already verified
        already_verified = await db_is_already_verified(user.id)

        if already_verified:
            # User is already verified
            await query.answer("✅ You are already verified and in the giveaway!")
        else:
            # Add the user to the verified list
            added = await add_verified(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            if added:
                await query.answer("🎉 Successfully added to the giveaway!")
                await query.message.edit_text(
                    text="🎉 You are now verified and in the giveaway!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")]
                        ]
                    )
                )
            else:
                await query.answer("⚠️ Something went wrong. Please try again.")

    elif data == "close":
        # Close the message
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
