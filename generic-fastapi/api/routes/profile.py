from ..depends import GetUser, create_router
from ..schema.user import User

router = create_router()


@router.get('', response_model=User)
async def read_user(user: GetUser):
    return user
