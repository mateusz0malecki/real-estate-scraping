from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Union

from db.database import get_db
from models.model_house import House
from models.model_flat import Flat
from schemas import schemas_estate
from exceptions import exceptions

router = APIRouter(tags=['Estates'])


@router.get(
    "/{for_sale}/{estate}",
    status_code=status.HTTP_200_OK
)
async def get_estates(
        estate: str,
        rent_or_sale: str,
        db: Session = Depends(get_db),
        page: int = 1,
        page_size: int = 20,
):

    if rent_or_sale not in ["sale", "rent"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if estate not in ["house", "flat"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for_sale = True if rent_or_sale == 'sale' else False
    if estate == 'house':
        instances = db.query(House).filter(House.for_sale == for_sale)
    else:
        instances = db.query(Flat).fliter(Flat.for_sale == for_sale)

    first = (page - 1) * page_size
    last = first + page_size
    if for_sale:
        response = schemas_estate.EstateSalePagination(
            estate,
            rent_or_sale,
            instances.all(),
            first,
            last,
            page,
            page_size
        )
    else:
        response = schemas_estate.EstateRentPagination(
            estate,
            rent_or_sale,
            instances.all(),
            first,
            last,
            page,
            page_size
        )
    return response


@router.get(
    "/details/house/{id_scrap}",
    status_code=status.HTTP_200_OK,
    response_model=schemas_estate.HouseWithDetails
)
async def get_house(
        id_scrap: int,
        db: Session = Depends(get_db)
):
    house = House.get_house_by_scrap_id(db, id_scrap)
    if not house:
        raise exceptions.EstateNotFound(id_scrap)
    return house


@router.get(
    "/details/flat/{id_scrap}",
    status_code=status.HTTP_200_OK,
    response_model=schemas_estate.FlatWithDetails
)
async def get_flat(
        id_scrap: int,
        db: Session = Depends(get_db)
):
    flat = Flat.get_flat_by_scrap_id(db, id_scrap)
    if not flat:
        raise exceptions.EstateNotFound(id_scrap)
    return flat
