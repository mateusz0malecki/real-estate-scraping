from fastapi import HTTPException, status


class EstateNotFound(HTTPException):
    def __init__(self, id_scrap: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estate with id '{id_scrap}' not found."
        )
