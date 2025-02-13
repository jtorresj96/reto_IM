#%%
import requests
from typing import List, Dict

class ProductAPIClient:
    BASE_URL: str = "https://dummyjson.com/products"

    def __init__(self) -> None:
        pass

    def get_all_products(self, min_price: float = 0, max_price: float = float('inf')) -> List[Dict[str, any]]:
        try:
            response: requests.Response = requests.get(self.BASE_URL)
            response.raise_for_status()
            data: Dict[str, any] = response.json()
            products = data.get("products", [])
            filtered_products = [
                {"id": p["id"], "title": p["title"], "price": p["price"], "description": p["description"]}
                for p in products
                if min_price <= p["price"] <= max_price
            ]
            return filtered_products
        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            return []
        
    def get_product_by_id(self, product_id: int) -> Dict[str, any]:
        try:
            response: requests.Response = requests.get(f"{self.BASE_URL}/{product_id}")
            response.raise_for_status()
            product: Dict[str, any] = response.json()
            return product
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product: {e}")
            return {}
        

if __name__ == "__main__":
    client: ProductAPIClient = ProductAPIClient()
    products: List[Dict[str, any]] = client.get_all_products(min_price=10, max_price=50)


# %%
