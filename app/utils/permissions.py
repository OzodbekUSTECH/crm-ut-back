from app.models import User
from app.utils.exceptions import CustomExceptions

class has_permission:

    
    @staticmethod
    async def is_id_belongs_to_current_user(
        id: int,
        current_user: User
    ) -> bool:
        if id != current_user.id:
            raise CustomExceptions.forbidden()
        return True
