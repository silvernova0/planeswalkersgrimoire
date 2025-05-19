from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.database import get_db
from app.models import MetaDeck

router = APIRouter()

@router.get("/meta/top-commanders")
async def get_top_commanders(db: AsyncSession = Depends(get_db)):
    # Get top 3 commanders by count
    result = await db.execute(
        select(
            MetaDeck.commander,
            func.count(MetaDeck.id).label("count")
        )
        .where(MetaDeck.commander != None)
        .group_by(MetaDeck.commander)
        .order_by(desc("count"))
        .limit(3)
    )
    commanders = result.all()
    # For each commander, get 3 example decks
    data = []
    for commander, count in commanders:
        decks_result = await db.execute(
            select(MetaDeck)
            .where(MetaDeck.commander == commander)
            .limit(3)
        )
        decks = decks_result.scalars().all()
        data.append({
            "commander": commander,
            "count": count,
            "decks": [
                {
                    "id": d.id,
                    "name": d.name,
                    "placement": d.placement,
                    "url": d.url
                } for d in decks
            ]
        })
    return data