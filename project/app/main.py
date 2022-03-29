from fastapi import FastAPI, Depends
from .config import get_settings, BaseSettings, Settings

app = FastAPI()


@app.get("/settings")
def settings_endpoint(settings: Settings = Depends(get_settings)):
    return {"settings": {"environement": settings.environement,
                         "testing": settings.testing}
            }
