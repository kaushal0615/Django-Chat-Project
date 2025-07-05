from ninja import Router
from .room_endpoints import router as room_router
from .message_endpoints import router as message_router

router = Router()

# Mount room and message routes under this combined router
router.add_router("", room_router)
router.add_router("", message_router)