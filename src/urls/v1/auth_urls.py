from fastapi import APIRouter

from src.services.auth.controller import AuthController


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


router.post("/register")(
    AuthController.register
)

router.post("/login")(
    AuthController.login
)

router.get("/me")(
    AuthController.me
)