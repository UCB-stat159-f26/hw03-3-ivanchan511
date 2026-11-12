# HW3) Python Package `tenplayer_plot`

In this homework assignment, I continued from our previous assignment, which examined whether we could replicate the graphic featured in the [New York Times article](https://www.nytimes.com/interactive/2022/08/28/sports/tennis/serena-age-opponents.html).    

We began with the [raw data JavaScript file](https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js), which contains Serena Williams's professional match records. First, we wrote `01_download_data.py` to download the raw data file. Next, we wrote `02_clean_data.py`to clean the raw data and export it as `clean_serena.csv` in the cleaned data directory. Finally, we wrote `03_replicate_graphic.py` to recreate the graphic and save it as a PNG file, shown below.  

Overall, I would consider the graphic replicable because we were able to clean the raw data into a cleaned dataset and produce a graph that closely resembles the original New York Times graphic. Furthermore, we could use our `Makefile` to automate the process of downloading, cleaning, and visualizing the data, making the workflow repeatable.  

The project uses `Python`, `pandas`, `numpy`, `requests`, and `matplotlib` for data processing and visualization.

## Dataset
The source of the data is the **Tennis Abstract's Record on Serena Williams's Professional Matches**:
<https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js>. 

To download the datasets, there are **three** ways:
1. **Recommended:** In the terminal, cd to this directory, and run `make data/raw/raw_serena.js`. This should automatically download the data file to the `data/raw/` folder.
2. Run the `01_download_data.py` script under the `script/` folder; this will automatically download the datasets in `data/raw/`.  
3. You could also directly download the `raw_serena.js` dataset in the `data/raw/` folder.  

## Package Installation
To install the package, you could follow these steps:

1. Clone the repository
```
conda env create -f environment.yml
conda activate hw02-env
```
2. Make sure to have the designated data file in the `data/raw/` folder. If not, please download the data using one of the [methods](https://github.com/UCB-stat159-f26/hw02-3-ivanchan511/tree/main#datasets) mentioned above. 
3. Run `Make` Commands <br> 
This homework is designed to automatically complete all tasks within one make command. In your terminal, under this repository directory, run `make all`; this will automatically run all the script files, export the graphic in PNG format, and render the report in HTML and PDF format.
4. View the output and report <br>
The replicated figure is saved as a PNG in the `outputs/` directory.  
The project report is located in the `report/` directory.

## Project Structure
Here's a diagram that depicts the overall file structure of the project:
```
.
├── tenplayer_plot/
│   ├── __init__.py (File to initiate the package)
│   ├── main_func.py (Main Functions for the package)
│   └── private_func.py (Helper Functions for the main functions)
│
├── tests/
│   ├── js_for_testing/ (Special Created Files to avoid hitting live servers)
│   │   ├── FemalePlayerCareer.js
│   │   └── MalePlayerCareer.js
│   └── test_cases.py (Test Cases for the Functions)
│
├── README.md
├── instructions.md
└── pyproject.toml
```