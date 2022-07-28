from pydantic import BaseModel


def lower_camel(string: str) -> str:
    camel = ''.join(word.capitalize() for word in string.split('_'))
    low_camel = camel[0].lower() + camel[1:]
    return low_camel


class EstatePagination(BaseModel):
    page_number: int = None
    page_size: int = None
    total_record_count: int = None
    pagination: dict = {}

    def __init__(self, estate, rent_or_sale, instances, first, last, page, page_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_number = page
        self.page_size = page_size
        self.total_record_count = len(instances)
        self.records = instances[first:last]

        if last >= len(instances):
            self.pagination["next"] = None
        else:
            self.pagination["next"] = f"/{estate}/{rent_or_sale}?page={page + 1}&page_size={page_size}"
        if page > 1:
            self.pagination["previous"] = f"/{estate}/{rent_or_sale}?page={page - 1}&page_size={page_size}"
        else:
            self.pagination["previous"] = None
