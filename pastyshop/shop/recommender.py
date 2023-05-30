import redis 
from django.conf import settings

from .models import Product


# connect to redis
r = redis.Redis(
    host="redis-14569.c250.eu-central-1-1.ec2.cloud.redislabs.com",
    port=14569,
    password=f"{settings.REDIS_PASSWORD}",
)

class Recommender:
    def get_products_ids(self, products):
        """
        The get_products_ids function takes a list of products and returns a list of their ids.
        
        :param self: Represent the instance of the class
        :param products: Get the id of each product in the products list
        :return: A list of product ids
        """
        return [product.id for product in products]

    def get_product_key(self, id):
        """
        The get_product_key function takes in a product id and returns the key for that product's purchased_with field.
        The purchased_with field is a set of all products that have been bought with this one.
        
        :param self: Access the instance of the class
        :param id: Get the product key
        :return: A key that is used to store the ids of products purchased with a given product
        """
        return f"product:{id}:purchased_with"
    
    def products_bought(self, products):
        """
        The products_bought function takes a list of products and increments 
        the score for each product purchased together.
        
        :param self: Represent the instance of the class
        :param products: Pass in a list of products that were bought together
        :return: The products that were bought together
        """
        products_ids = self.get_products_ids(products)
        for product_id in products_ids:
            for with_id in products_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id),
                            1,
                            with_id)
                    
    def suggest_products_for(self, products, max_results=6):
        """
        The suggest_products_for function takes a list of products and returns 
        a list of suggested products. The function uses the Redis sorted set data 
        structure to store product ids as keys, and their scores as values.
        The score is calculated by adding up the number of times each product 
        has been purchased together with other products in the same order.
        If only one product is passed to suggest_products_for, it will return 
        all other products that have been purchased together with it (descending order). 
        If more than one product is passed, it will return all other products that have 
        been purchased together with any of them (descending order).
        
        :param self: Make the function a method of the recommender class
        :param products: Get the products that we want to recommend similar products for
        :param max_results: Limit the number of results returned
        :return: A list of suggested products
        """
        product_ids = self.get_products_ids(products)
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1,
                                    desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products
    
    def clear_purchases(self):
        """
        The clear_purchases function clears the purchases for a given user.
        It does this by deleting all keys in Redis that start with the prefix 'purchases:'.
        
        
        :param self: Refer to the object that is calling the function
        :return: Nothing
        """
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
            