import csv
from heapq import nsmallest

def find_cheapest_bikes(file_path, n=3):
    """
    Reads a CSV file containing bicycle prices and returns the n cheapest bikes.
    
    Args:
        file_path (str): Path to the CSV file
        n (int): Number of cheapest bikes to find
        
    Returns:
        list: List of dictionaries containing the cheapest bikes' details
    """
    try:
        with open(file_path, 'r') as file:
            # Skip header line
            next(file)
            
            # Read all bikes into a list
            bikes = []
            
            # Read each line
            for line in file:
                # Split line by comma
                model, bike_type, price = line.strip().split(',')
                
                # Convert price to float
                price = float(price.replace('$', '').replace('USD', ''))
                
                # Add bike to list
                bikes.append({
                    'model': model,
                    'type': bike_type,
                    'price': price
                })
            
            # Find the n cheapest bikes using heapq
            cheapest_bikes = nsmallest(n, bikes, key=lambda x: x['price'])
            
            return cheapest_bikes
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    file_path = 'bicycle_prices_csv_format.txt'
    cheapest_bikes = find_cheapest_bikes(file_path, 3)
    
    print("The 3 cheapest bikes are:")
    for i, bike in enumerate(cheapest_bikes, 1):
        print(f"\n#{i}:")
        print(f"Model: {bike['model']}")
        print(f"Type: {bike['type']}")
        print(f"Price: ${bike['price']:.2f} USD")

if __name__ == "__main__":
    main()
