# Double-Spending Tracker

## Overview
This repository contains code for a simple double-spending tracker implemented using Flask and NetworkX. It simulates a blockchain environment and demonstrates how to detect and track double-spending transactions.

## Installation
1. Clone this repository:

git clone https://github.com/Om-Deshamudre/Double-Spending-Tracker.git


2. Navigate to the project directory:
cd Double-Spending-Tracker

3. Install the required dependencies:
pip install -r requirements.txt

## Usage
1. Run the Flask application:
python app.py

2. Open your web browser and go to `http://127.0.0.1:5000/` to view the blockchain transaction graph.

## Project Structure
- `app.py`: Contains the Flask application code.
- `templates/index.html`: HTML template for rendering the transaction graph.
- `README.md`: Overview and usage instructions for the repository.
- `requirements.txt`: List of Python dependencies required for the project.
- `LICENSE`: License information for the project.

## License
This project is licensed under the [MIT License](LICENSE).

## Credits
- [Flask](https://flask.palletsprojects.com/): Web framework used for building the application.
- [NetworkX](https://networkx.org/): Library used for representing and analyzing the transaction graph.
- [Matplotlib](https://matplotlib.org/): Library used for plotting the transaction graph.
