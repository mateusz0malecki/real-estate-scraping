from fastapi import APIRouter, Depends, status, HTTPException, Path, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.model_house import House
from models.model_flat import Flat
from schemas import schemas_estate
from exceptions import exceptions

router = APIRouter(tags=['Estates'])


@router.get(
    "/{rent_or_sale}/{estate}",
    status_code=status.HTTP_200_OK
)
async def get_estates(
        rent_or_sale: str = Path(description="Should equal 'sale' or 'rent'"),
        estate: str = Path(description="Should equal 'house' or 'flat'"),
        db: Session = Depends(get_db),
        page: int = Query(default=1),
        page_size: int = Query(default=20),
        min_number_of_rooms: int | None = Query(default=None),
        max_number_of_rooms: int | None = Query(default=None),
        min_area: int | None = Query(default=None),
        max_area: int | None = Query(default=None),
        min_price: int | None = Query(default=None),
        max_price: int | None = Query(default=None),
        min_price_per_m2: int | None = Query(default=None),
        max_price_per_m2: int | None = Query(default=None),
        min_rent_price: int | None = Query(default=None),
        max_rent_price: int | None = Query(default=None),
):
    """
    Returns list of estates that matches used filter query parameters.
    Pagination included.
    """
    if rent_or_sale not in ["sale", "rent"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if estate not in ["house", "flat"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for_sale = True if rent_or_sale == 'sale' else False
    if estate == 'house':
        queryset = db.query(House).filter(House.for_sale == for_sale)
        model = House
    else:
        queryset = db.query(Flat).filter(Flat.for_sale == for_sale)
        model = Flat

    if min_number_of_rooms:
        queryset = queryset.filter(model.number_of_rooms >= min_number_of_rooms)
    if max_number_of_rooms:
        queryset = queryset.filter(model.number_of_rooms <= max_number_of_rooms)
    if min_area:
        queryset = queryset.filter(model.area >= min_area)
    if max_area:
        queryset = queryset.filter(model.area <= max_area)
    if min_price and for_sale:
        queryset = queryset.filter(model.price >= min_price)
    if max_price and for_sale:
        queryset = queryset.filter(model.price <= max_price)
    if min_price_per_m2 and not for_sale:
        queryset = queryset.filter(model.price_per_m2 >= min_price_per_m2)
    if max_price_per_m2 and not for_sale:
        queryset = queryset.filter(model.price_per_m2 <= max_price_per_m2)
    if min_rent_price and not for_sale:
        queryset = queryset.filter(model.rent_price >= min_rent_price)
    if max_rent_price and not for_sale:
        queryset = queryset.filter(model.rent_price <= max_rent_price)

    first = (page - 1) * page_size
    last = first + page_size
    if for_sale:
        response = schemas_estate.EstateSalePagination(
            estate,
            rent_or_sale,
            queryset.all(),
            first,
            last,
            page,
            page_size
        )
    else:
        response = schemas_estate.EstateRentPagination(
            estate,
            rent_or_sale,
            queryset.all(),
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
        id_scrap: int = Path(description="Id of specific offer"),
        db: Session = Depends(get_db)
):
    """
    Displays all available data about chosen house.
    """
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
        id_scrap: int = Path(description="Id of specific offer"),
        db: Session = Depends(get_db)
):
    """
    Displays all available data about chosen flat.
    """
    flat = Flat.get_flat_by_scrap_id(db, id_scrap)
    if not flat:
        raise exceptions.EstateNotFound(id_scrap)
    return flat
