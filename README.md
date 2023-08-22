# Lagos Air Quality Monitoring System

The **Lagos Air Quality Monitoring System** is a Python application that retrieves and visualizes air quality data from the Astra database or a local CSV file. The application includes a graphical user interface (GUI) to interactively select and display different plots based on user preferences.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/your-repo.git



2. Install the required libraries:
pip install pandas matplotlib cassandra-driver tkinter



3. Place the `secure-connect-dcbdms-lag.zip` and `babaniyilawal@yahoo.com-token.json` files in the same directory as the script.

## Usage

Run the script by executing:
python lagos_air_quality_monitoring.py




The GUI will open, allowing you to select different parameters and plot types to visualize air quality data.

## Functionality

The application performs the following tasks:

1. Retrieves data from the Astra database using the Cassandra driver.
2. If Astra retrieval fails, falls back to reading data from a local CSV file.
3. Displays a GUI for user interaction:
   - Select a year, attribute, and plot type.
   - Generates plots based on user selections: Time Series, Scatter Plot, or Box Plot.
   - Displays summary statistics for the selected attribute.

## Dependencies

The application relies on the following libraries:

- `pandas`: Data manipulation and analysis.
- `matplotlib`: Plotting and visualization.
- `cassandra-driver`: Cassandra database interaction.
- `tkinter`: GUI framework for creating the graphical interface.

## License

This project is licensed under the [MIT License](LICENSE).

