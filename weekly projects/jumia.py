import requests
from bs4 import BeautifulSoup
import webbrowser
from notify_run import Notify
import time
import sys

notify = Notify()
CATEGORIES = {
    1: "phones-tablets",
    2: "electronics",
    3: "computing",
    4: "home-office",
    5: "health-beauty",
    6: "grocery",
    7: "gaming",
    8: "baby-products",
    9: "fashion",
    0: "search",
    11: "observe"
}

def display_menu():
    """Display category selection menu"""
    print('\nChoose a category by number:')
    print(f' [1] Phones & Tablets{"  [2] Electronics":>25}{"  [3] Computing":>20}')
    print(f' [4] Home & Office{"  [5] Health & Beauty":>25}{"  [6] Grocery":>20}')
    print(f' [7] Gaming{"  [8] Baby Products":>25}{"  [9] Fashion":>20}')
    print(f' [0] Search whole website{"  [11] Observe product":>20}')
    return get_int_input("Enter choice: ", valid_options=CATEGORIES.keys())

def get_int_input(prompt, valid_options=None):
    """Get validated integer input from user"""
    while True:
        try:
            value = int(input(prompt))
            if valid_options is None or value in valid_options:
                return value
            print(f"Invalid option. Please choose from {list(valid_options)}")
        except ValueError:
            print("Please enter a valid number")

def get_price_input(prompt):
    """Get validated price input"""
    while True:
        try:
            value = input(prompt).replace(',', '').strip()
            return int(value)
        except ValueError:
            print("Invalid price. Please enter numbers only")

def fetch_products(url):
    """Fetch and parse products from given URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        product_container = soup.find(class_="products -mabaya")

        if not product_container:
            print("\nError: No products found with current filters")
            return None

        return product_container.findAll(class_="sku -gallery")
    except Exception as e:
        print(f"\nError fetching products: {str(e)}")
        return None

def parse_products(itemlist):
    """Parse product items into structured data"""
    products = []
    for item in itemlist:
        try:
            title = item.find(class_='title')
            brand = title.find(class_='brand').text.strip()
            description = title.find(class_='name').text.strip()

            price_container = item.find(class_='price-container')
            price = price_container.find(class_='price').text.strip()
            numeric_price = int(''.join(filter(str.isdigit, price.split()[1])))

            link = item.find('a')['href']

            products.append({
                'brand': brand,
                'description': description,
                'price': numeric_price,
                'url': f"https://www.jumia.co.ke"
            })
        except Exception as e:
            print(f"Error parsing product: {str(e)}")
    return products

def select_product(products):
    """Let user select a product from the list"""
    print("\nFound products:")
    for idx, product in enumerate(products, 1):
        print(f"{idx}. {product['brand']} {product['description']} - KSh {product['price']:,}")

    choice = get_int_input("\nSelect product (1-{}): ".format(len(products)),
                          valid_options=range(1, len(products)+1))
    return products[choice-1]

def monitor_product(product, target_price):
    """Background task to monitor price changes"""
    print(f"\nMonitoring: {product['description']}")
    print(f"Current price: KSh {product['price']:,}")
    print(f"Target price: KSh {target_price:,}")
    print(f"Notification endpoint: {notify.endpoint}")

    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(product['url'], headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            price_str: str = soup.find('span', class_='-b').text.strip()
            current_price = int(''.join(filter(str.isdigit, price_str)))

            if current_price <= target_price:
                message = f"PRICE DROP! {product['description']} is now KSh {current_price:,}"
                notify.send(message)
                print(f"\n{message}")
                print("Notification sent! Exiting monitor.")
                return

            print(f"Checked at {time.strftime('%H:%M:%S')} - Current price: KSh {current_price:,}")
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            print(f"Monitoring error: {str(e)}")
            time.sleep(600)  # Wait longer on error

def main():
    """Main program flow"""
    choice = display_menu()

    if choice == 0:  # Search
        query = input("Enter product name: ").strip()
        min_price = get_price_input("Enter minimum price: ")
        max_price = get_price_input("Enter maximum price: ")

        if min_price > max_price:
            print("\nError: Minimum price cannot be higher than maximum price")
            return

        url = f"https://www.jumia.co.ke {query.replace(' ', '%20')}&price={min_price}-{max_price}"
    elif choice == 11:  # Direct product observation
        product_url = input("Enter full product URL: ").strip()
        products = [{
            'url': product_url,
            'description': 'Your Selected Product',
            'price': get_price_input("Enter current price: ")
        }]
        selected_product = products[0]
        target_price = get_price_input("Enter desired price: ")
        monitor_product(selected_product, target_price)
        return
    else:  # Category
        min_price = get_price_input("Enter minimum price: ")
        max_price = get_price_input("Enter maximum price: ")
        url = f"https://www.jumia.co.ke/  {CATEGORIES[choice]}/?price={min_price}-{max_price}"
    # Fetch and parse products
    items = fetch_products(url)
    if not items:
        return

    products = parse_products(items)
    if not products:
        print("\nNo valid products found with current filters")
        return

    # Let user select product
    selected_product = select_product(products)
    target_price = get_price_input("Enter your target price: ")

    # Setup notifications
    notify_url = notify.register().endpoint
    print(f"\nNotification endpoint: {notify_url}")
    webbrowser.open(notify_url)

    if input("\nHave you subscribed to notifications? (Y/N): ").upper() != 'Y':
        print("Please subscribe to notifications first")
        return

    # Start monitoring
    print("\nStarting price monitoring...")
    print("Keep this program running in the background")
    print("Press Ctrl+C to stop monitoring\n")
    monitor_product(selected_product, target_price)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)