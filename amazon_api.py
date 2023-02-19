from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException
from response_parser import parse_response
from consts import *
import logging

logging.basicConfig(level=logging.INFO)
# function that search amazon products
def search_items(keywords, search_index="All", item_page=1):
    default_api = DefaultApi(
        access_key=AMAZON_ACCESS_KEY,
        secret_key=AMAZON_SECRET_KEY,
        host=AMAZON_HOST,
        region=AMAZON_REGION,
    )

    """ Specify the category in which search request is to be made """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/use-cases/organization-of-items-on-amazon/search-index.html """

    """ Specify item count to be returned in search result """
    item_count = 20

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
        SearchItemsResource.ITEMINFO_FEATURES,
        SearchItemsResource.OFFERS_LISTINGS_PROMOTIONS,
        SearchItemsResource.OFFERS_LISTINGS_CONDITION,
        SearchItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
        SearchItemsResource.OFFERS_SUMMARIES_LOWESTPRICE,
        SearchItemsResource.OFFERS_SUMMARIES_HIGHESTPRICE,
        SearchItemsResource.ITEMINFO_CLASSIFICATIONS,
        SearchItemsResource.ITEMINFO_PRODUCTINFO,
        SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    ]

    """ Forming request """
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=PARTNER_TAG,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
            item_page=item_page,
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    try:
        """Sending request"""
        response = default_api.search_items(search_items_request)
        logging.debug("Response received, total items:", response.search_result.total_result_count)

        if (response.search_result.total_result_count == 0 or response.search_result.items is None):
            return []
        res = parse_response(response)

        if response.errors is not None:
            logging.error("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
            logging.error("Error code", response.errors[0].code)
            logging.error("Error message", response.errors[0].message)
        return res

    except ApiException as exception:
        logging.error("Error calling PA-API 5.0!")
        logging.error("Status code:", exception.status)
        logging.error("Errors :", exception.body)
        logging.error("Request ID:", exception.headers["x-amzn-RequestId"])
        return []

    except TypeError as exception:
        logging.error("TypeError :", exception)

    except ValueError as exception:
        logging.error("ValueError :", exception)

    except Exception as exception:
        logging.error("Exception :", exception)
