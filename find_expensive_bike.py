import csv

def find_most_expensive_bike(file_path):
    """
    Reads a CSV file containing bicycle prices and returns the most expensive bike.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        dict: Dictionary containing the most expensive bike's details
    """
    try:
        with open(file_path, 'r') as file:
            # Skip header line
            next(file)
            
            # Initialize variables to track most expensive bike
            most_expensive = None
            highest_price = 0
            
            # Read each line
            for line in file:
                # Split line by comma
                model, bike_type, price = line.strip().split(',')
                
                # Convert price to float
                price = float(price.replace('$', '').replace('USD', ''))
                
                # Update most expensive bike if this one is more expensive
                if price > highest_price:
                    highest_price = price
                    most_expensive = {
                        'model': model,
                        'type': bike_type,
                        'price': price
                    }
            
            return most_expensive
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    file_path = 'bicycle_prices_csv_format.txt'
    most_expensive = find_most_expensive_bike(file_path)
    
    if most_expensive:
        print(f"The most expensive bike is:")
        print(f"Model: {most_expensive['model']}")
        print(f"Type: {most_expensive['type']}")
        print(f"Price: ${most_expensive['price']:.2f} USD")
    else:
        print("No bikes found or error occurred.")

if __name__ == "__main__":
    main()
