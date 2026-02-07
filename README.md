# StudentsGo
StudentsGo is a Python command-line tool that helps compare travel options around Taipei City, with a focus on trips near National Taiwan University (NTU). It consolidates MRT, bus, and YouBike choices so users can evaluate cost and time quickly, then stores trip history for later review.

## Features

- Compare travel options by origin, destination, price, and estimated time.
- View a running travel history with total cost and time per session.
- Built-in CSV data for transport info and station listings.

## Project Structure

- `Main.py`: CLI application entry point.
- `transport_info.csv`: Route and mode data used for travel options.
- `station_list.csv`: Reference list of stations.
- `travel_history.csv`: Generated history file saved by the app.
- `MRTFares.pdf`: Reference fares document.

## Requirements

- Python 3.8+ (standard library only)

## Getting Started

1. Ensure the data files (`transport_info.csv`, `station_list.csv`) are in the same directory as `Main.py`.
2. Run the application:

```bash
python Main.py
```

## Usage

1. Choose **Start a new travel** to select an origin, destination, and transport mode.
2. Review the trip recap, including total cost and time.
3. Choose **View Travel History** to see past sessions and totals.

The app writes session history to `travel_history.csv` in the project directory.

## Data Notes

- Pricing data is stored in `transport_info.csv` and read at runtime.
- Time values are stored as minutes in the CSV and formatted for display.

## License

MIT License

Copyright (c) 2025 StudentsGo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
