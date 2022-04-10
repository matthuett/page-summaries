from fastapi import Depends, APIRouter

from ..config import Settings, get_settings

router = APIRouter()


@router.get("/ping")
async def settings_endpoint(settings: Settings = Depends(get_settings)):
    return {"msg": {"environment": settings.environment,
                    "testing": settings.testing
                    }
            }
