from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserReaction, MessageBase


async def delete_user_reactions(session: AsyncSession, user_id: int, message_id: int):

    await session.execute(
        delete(UserReaction)
        .where(
            UserReaction.user_id == user_id,
            UserReaction.message_id == message_id
        )
    )

async def create_user_reactions(session: AsyncSession, user_id: int, message_id: int, reactions: list[str]):

    for em in reactions:
        new_reaction = UserReaction(
            user_id=user_id,
            message_id=message_id,
            reaction=em,
        )
        session.add(new_reaction)

    await session.commit()

async def get_list_of_message_reactions(session: AsyncSession, message_id: int) -> list[dict]:
    statement = (
        select(UserReaction.reaction, func.count(UserReaction.id).label("count"))
        .where(UserReaction.message_id == message_id)
        .group_by(UserReaction.reaction)
    )

    result = await session.execute(statement)
    reactions = result.all()

    return [{"emoji": react.reaction, "count": react.count} for react in reactions ]

