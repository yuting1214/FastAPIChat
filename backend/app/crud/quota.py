from sqlalchemy.orm import Session
from backend.app.models import Quota
from backend.app.models.quota import user_quota_association_table

async def get_user_quota(db: Session, user_id: int, quota_resource_type: str):
    return await db.query(Quota).join(user_quota_association_table).filter(
        user_quota_association_table.c.user_id == user_id,
        Quota.resource == quota_resource_type
    ).first()