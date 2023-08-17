"""
API tool for collection stocks for shopee.

"""
import requests as rq
from typing import Dict, Any, Tuple
from functools import lru_cache
import logging

logger = logging.getLogger('Shopee_API')
# API_URL = "https://shopee.sg/api/v4/pdp/get_pc"
# API_URL = "https://shopee.tw/api/v4/pdp/get_pc"
API_URL = "https://shopee.my/api/v4/pdp/get_pc"

def wait_for_some_second(sec :float = 1.0):
    def fn_decorator(fn):
        def waited_function(*args, **kargs):
            import time 
            time.sleep(sec)
            print(f"Dealing with ID = {kargs.get('item_id', None)}")
            result = fn(*args, **kargs)
            return result
        return waited_function
    return fn_decorator

def get_param_dict(shop_id:int, item_id:int) :
    """    
    Returns a dictionary with keys 'item_id', 'shop_id' and
    their corresponding integer values.
    """
    return dict(shop_id=shop_id, item_id=item_id)


def get_shopee_api_dict(params) -> Dict[str, Any]:
    """    
    Returns a dictionary with data obtained from a GET request to Shopee
    API using the provided parameters.
    """
    my_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    req = rq.get(API_URL, params=params, headers=my_headers)
    return req.json()

def get_model_list(shopee_api_return_dict:Dict[str, Any]) -> list:
    """    
    Returns the value associated with the ['data']['item']['models'] key from the
    provided Shopee API response dictionary.
    """

    item_status = shopee_api_return_dict['data']['item']['item_status']
    model_info_list = []
    
    try:
        model_list = shopee_api_return_dict['data']['item']['models']
        for model in model_list:
            # if need item_id, add here
            model_id = model['model_id']
            model_status = item_status
            model_stock = model['stock']
            model_price = model['price']

            model_info = {
                "model_id": model_id,
                "status": model_status,
                "stock": model_stock,
                "price": model_price / 100_000 #/100000 because the orig price is somehow bluffed
            }

            model_info_list.append(model_info)

        return model_info_list
    except KeyError as ke:
        raise ke
    
    
@wait_for_some_second(sec = 1)
def get_current_item_details(shop_id:int, item_id:int) -> list:
    """
    Returns the value of the 'normal_stock' key from the Shopee API response
    dictionary obtained using the provided
    item_id, model_id, and shop_id parameters.
    """
    params = get_param_dict(shop_id, item_id)
    request_dict = get_shopee_api_dict(params=params)
    try:
        current_item_details =  get_model_list(request_dict)
        return current_item_details
    except KeyError as ke:
        logger.warning(f"Model Info {params} has no 'item' key!")