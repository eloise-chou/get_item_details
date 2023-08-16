import logging 
import pandas as pd
from typing import Tuple

from model.request import get_current_item_details

logger = logging.getLogger('Shopee_API')
logger.setLevel(logging.WARNING)


def df_column_to_item_details(data: pd.Series) -> list:
    try:
        item_id     :int = data["item_id"]
        shop_id     :int = data["shop_id"] 
        item_details = get_current_item_details(
            item_id     = item_id,
            shop_id     = shop_id,
        )
        return item_details
    except Exception as e:
        logger.warning(e)
        return [-1, -1, -1, -1]


def item_detail_to_df(data: pd.Series) -> pd.DataFrame:
    item_detail = df_column_to_item_details(data)

    

    data['current_stock'] = item_detail[0]
    data['current_price'] = item_detail[1]
    return data