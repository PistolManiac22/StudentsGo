import csv
import os
from datetime import datetime
import math

# Define the directory path and ensure the working directory is set
files_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(files_dir)

def load_database_from_csv(filename):
    """
    Load the transport data from the CSV into a dictionary format.
    The dictionary structure will be {origin: [{destination, mode, price, time_needed}, ...]}.
    """
    data = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origin = row['Origin']
            destination = row['Destination']
            mode = row['Mode']
            price = row['Price']
            time_needed = row['Time_Needed']

            if origin not in data:
                data[origin] = []
            data[origin].append({
                'destination': destination,
                'mode': mode,
                'price': price,
                'time_needed': time_needed
            })
    return data

def format_time(minutes):
    """Convert time in minutes to hours and minutes format."""
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours} hour{'' if hours == 1 else 's'}, {minutes} minute{'' if minutes == 1 else 's'}"
    else:
        return f"{minutes} minute{'' if minutes == 1 else 's'}"

def save_history_to_csv(history, session_date, filename='travel_history.csv'):
    """
    Save the current session's trip history to the CSV file.
    Each record includes the session date, total cost, and total time.
    """
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Session Date', 'Origin', 'Destination', 'Price', 'Time', 'Mode', 'Total Cost', 'Total Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new
        if os.stat(filename).st_size == 0:
            writer.writeheader()

        total_cost = 0
        total_time = 0
        for trip in history:
            for record in trip:
                price = float(record[3].replace(" NTD", "").replace("$", "").strip())
                time = int(record[4])

                total_cost += price
                total_time += time

                writer.writerow({
                    'Session Date': session_date,
                    'Origin': record[0],
                    'Destination': record[1],
                    'Price': record[3],
                    'Time': record[4],
                    'Mode': record[2],
                    'Total Cost': total_cost,
                    'Total Time': format_time(total_time)
                })

def load_history_from_csv(filename='travel_history.csv'):
    history = {}
    if os.path.exists(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                session_date = row['Session Date']
                if session_date not in history:
                    history[session_date] = []
                history[session_date].append((
                    row['Origin'],
                    row['Destination'],
                    row['Mode'],
                    row['Price'],
                    row['Time']
                ))
    return history

def main():
    trip_history = load_history_from_csv()

    if not os.path.exists('transport_info.csv'):
        print("Error: transport_info.csv not found!")
        return

    transport_database = load_database_from_csv('transport_info.csv')

    session_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_history = []

    while True:
        print("\n=== Main Menu ===")
        print("1. Start a new travel")
        print("2. View Travel History")
        print("3. Exit Program")

        try:
            main_choice = int(input("Select an option: "))

            if main_choice == 3:
                print("\nThank you for using the program. Goodbye!")
                if session_history:
                    save_history_to_csv(session_history, session_date)
                    print("\nSession history saved successfully.")
                return

            elif main_choice == 2:
                if not trip_history:
                    print("\nNo travel history found.")
                else:
                    print("\n--- Complete Travel History ---")
                    for session, trips in trip_history.items():
                        total_cost = 0
                        total_time = 0
                        print(f"\nSession Date: {session}")
                        for trip in trips:
                            price = float(trip[3].replace(" NTD", "").replace("$", "").strip())
                            time = int(trip[4].split()[0].strip())

                            total_cost += price
                            total_time += time
                            print(f"  - From {trip[0]} to {trip[1]} (Price: {trip[3]}, Time: {trip[4]}, Transport: {trip[2]})")

                        print(f"Total Cost: ${total_cost} NTD")
                        print(f"Total Time: {format_time(total_time)}")
                continue

            elif main_choice == 1:
                print("\nAvailable Starting Locations:")
                origins = list(transport_database.keys())
                for idx, origin in enumerate(origins, 1):
                    print(f"{idx}. {origin}")
                print(f"{len(origins) + 1}. Back to Main Menu")

                origin_choice = int(input("Select an option: "))

                if origin_choice == len(origins) + 1:
                    continue
                elif 1 <= origin_choice <= len(origins):
                    origin = origins[origin_choice - 1]
                    print(f"\nYou selected: {origin}")

                    destinations = {entry['destination'] for entry in transport_database[origin]}
                    print("\nAvailable Destinations:")
                    for idx, dest in enumerate(destinations, 1):
                        print(f"{idx}. {dest}")
                    print(f"{len(destinations) + 1}. Back to Starting Location Menu")

                    destination_choice = int(input("Select a destination: "))

                    if destination_choice == len(destinations) + 1:
                        continue
                    elif 1 <= destination_choice <= len(destinations):
                        chosen_dest = list(destinations)[destination_choice - 1]
                        print(f"\nYou selected: {chosen_dest}")

                        selected_transports = [
                            entry for entry in transport_database[origin] if entry['destination'] == chosen_dest
                        ]
                        print(f"\nAvailable Transportation Methods to {chosen_dest}:")
                        for idx, transport in enumerate(selected_transports, 1):
                            print(f"{idx}. {transport['mode']} (Price: {transport['price']}, Time: {transport['time_needed']})")
                        print(f"{len(selected_transports) + 1}. Back to Destination Menu")

                        transport_choice = int(input("Select a transportation method: "))

                        if transport_choice == len(selected_transports) + 1:
                            continue
                        elif 1 <= transport_choice <= len(selected_transports):
                            selected_transport = selected_transports[transport_choice - 1]
                            session_history.append([(
                                origin,
                                chosen_dest,
                                selected_transport['mode'],
                                selected_transport['price'],
                                selected_transport['time_needed']
                            )])

                            total_cost = float(selected_transport['price'].replace(" NTD", "").replace("$", "").strip())
                            total_time = int(selected_transport['time_needed'].split()[0].strip())
                            print(f"\n--- Trip Recap ---")
                            print(f"Origin: {origin}")
                            print(f"Destination: {chosen_dest}")
                            print(f"Transport Mode: {selected_transport['mode']}")
                            print(f"Price: {selected_transport['price']}")
                            print(f"Time: {selected_transport['time_needed']}")
                            print(f"Total Cost: ${total_cost} NTD")
                            print(f"Total Time: {format_time(total_time)}")

                            save_history_to_csv(session_history, session_date)
                            print("\nTrip information saved successfully.")
                            session_history = []

                        else:
                            print("\nInvalid selection. Please try again.")
                    else:
                        print("\nInvalid selection. Please try again.")
                else:
                    print("\nInvalid selection. Please choose a valid option.")

            else:
                print("\nInvalid selection. Please choose a valid option.")

        except ValueError:
            print("\nInvalid input. Please enter a number.")

if __name__ == "__main__":
    main()
