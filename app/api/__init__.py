from app.api.sessions import router as sessions_router
from app.api.scenarios import router as scenarios_router

ROUTERS = [
    scenarios_router,
    sessions_router,
]

__all__ = ["ROUTERS"]
