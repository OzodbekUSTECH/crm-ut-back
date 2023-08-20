from fastapi import HTTPException, status

class CustomExceptions:
    @staticmethod
    def forbidden(detail="Forbidden"):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

    @staticmethod
    def not_found(detail="Not found"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

    @staticmethod
    def unauthorized(detail="Unauthorized"):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
    
    @staticmethod
    def conflict(detail="Already exists"):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
    
    @staticmethod
    def unprocessable_entity(detail="Somethign was wrong in data"):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

# Использование

