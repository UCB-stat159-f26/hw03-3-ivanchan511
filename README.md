# HW3) Python Package `tenplayer_plot`

This is a continuation of HW1 and HW2, which examined and replicated the graphic featured in the [New York Times article](https://www.nytimes.com/interactive/2022/08/28/sports/tennis/serena-age-opponents.html).    

For this assignment, I developed a Python Package called `tenplayer_plot`. The package retrieves a tennis player's career match records from [tennisabstract.com](https://www.tennisabstract.com/) and generates a scatter plot similar to the New York Times data visualization replicated in HW2, without the original article's annotations.

The package is designed to work with different professional tennis players, including Serena Williams and Rafael Nadal. It contains two main public functions: `get_player_data` and `plot_payer_data`.

The package uses Python and the following libraries:
* `pandas`: Data manipulation and DataFrame processing.
* `numpy`: Numerical operations and axis configuration.
* `requests`: Retrieving player data from Tennis Abstract.
* `matplotlib`: Creating and customizing scatter plots.

## Package Main Functions
The package provides two main public functions:
1. `get_player_data`
2. `plot_payer_data` 

The following sections explain how to use each function.
### Function Usage and Guide
#### 1. `get_player_data(player_name)`
* Input: Player Name **(str)**
    * Some acceptable input formats include: 
        * `"serena williams"`, `"Serena Williams"`, `"SerenaWilliams"`, `"rafael nadal"`, `"Rafael Nadal"`
    * **Note:** Concatenated names should preserve capitalization (e.g., "SerenaWilliams"). 
        * Lowercase concatenated names such as **"serenawilliams"** are not recognized because the function cannot determine where name boundaries occur.
    * If the player cannot be found, the function raises a `ValueError` error message:
    ```
    Player 'CakeBake' not found. Please Type in a Valid Player Name.
    ```
* Output: **`pandas.DataFrame`**  
The returned DataFrame contains the following columns:
| **Column** | **Description** |
|:---:|:---:|
| match_date | Date of the match, stored as a datetime object |
| win/loss | Match result (W or L) |
| opponent_name | Opponent's name |
| player_age_at_match | Player's age when the match took place |
| opponent_age_at_match | Opponent's age when the match took place |
| age_difference | Difference between the player's age and opponent's age |
    * An additional column, `opponent_dob`, is included for **female players** because their original career match records provide the opponent's date of birth rather than their age at the time of the match.
    * The package handles this difference by calculating the opponent's age from their date of birth and the match date. For male players, the opponent's age is already available in the original match records.

#### 2. `plot_payer_data(player_df, player_name = "")`
* **Required Input:** Player DataFrame **(`pandas.DataFrame`)**
    * Ideally, this should be the DataFrame returned by `get_player_data`.
    * The function checks whether the input DataFrame contains the required columns before generating the plot:
        * `"match_date"`, `"win/loss"`, `"player_age_at_match"`, `"age_difference"`
            * **Column names must match exactly.** 
    * If any required columns are missing, the function raises a `ValueError` error message identifying the missing columns.
    ```
    Missing required columns: ... 
    ```
* **Optional Input:** Player Name **(str)**
    * This argument is used to customize the plot title. By default, it is an empty string.
    * The title follows these formats:
        * Without a player name: `Player Professional Matches, Age {age_min} to {age_max}`
        * With a player name: `{player_name}'s Professional Matches, Age {age_min} to {age_max}`.
    * Here, `age_min` and `age_max` represent the youngest and oldest ages recorded in the player's match data.
* Output: fig, ax 
    * The function returns the `Matplotlib` figure and axes objects. 
    * This allows users to further customize the visualization or save the plot in different formats.

### Example Usage
The following example demonstrates how to retrieve a player's career data and generate a corresponding scatter plot.
```
import tenplayer_plot

# Retrieve career match data
serena_df = get_player_data("Serena Williams")

# Generate scatter plot
fig, ax = plot_player_data(serena_df, "Serena Williams")

# Save the figure
fig.savefig("serena_graph.png", dpi=300, bbox_inches="tight")
``` 
The same functions can be used with other players:
```
# Retrieve Rafael Nadal's career match data
rafael_df = get_player_data("Rafael Nadal")

# Generate scatter plot
fig, ax = plot_player_data(rafael_df, "Rafael Nadal")
```

## Package Installation
To install the package, follow these steps:

1. **Install the package from GitHub**  
* Run the following command in your terminal or notebook:
```
pip install git+https://github.com/UCB-stat159-f26/hw03-3-ivanchan511.git
```
2. **Import the package**  
```
import tenplayer_plot
```
3. **Retrieve player data and generate a plot**   
* Refer to the Function Usage and Guide section above for examples.

## Reflection
I feel that the main challenge of this assignment was developing the `get_player_data()` function. The overall workflow was quite different from HW1 and HW2 because I was moving away from working with a single player's data toward building a package that could retrieve and process data for different players on Tennis Abstract. This meant I had to account for differences in the data structures between male and female players. Handling this difference was not difficult once I understood the structure of the data. 

However, retrieving the player's own date of birth took me considerably longer. Initially, I thought I would need to scrape the player's birthday from the profile webpage. Eventually, I discovered that Tennis Abstract provides a separate JavaScript file containing player information, including their date of birth. Finding this file significantly simplified the process.

Another important thing I learned was separating different components of a program into individual functions. By organizing the code into smaller helper functions, I was able to keep the main functions cleaner and make the overall package easier to maintain. It also allowed me to test individual helper functions independently rather than having to run the entire workflow every time I wanted to check whether a particular component worked correctly.

Overall, this assignment gave me experience working with a project structure that involves writing helper functions in one Python file and importing them into another. Previously, I had done most of my coding in Jupyter notebooks, so organizing code across multiple files and developing a reusable Python package was a new experience for me. I also gained more experience with package organization and writing test cases. Most importantly, it was rewarding to turn work developed for a single visualization into a package that can retrieve and visualize data for different tennis players.

## Project Structure
The following diagram illustrates the overall file structure of the project:
```
.
├── tenplayer_plot/
│   ├── __init__.py               # Initializes the package
│   ├── main_func.py              # Main public functions
│   └── private_func.py           # Helper functions for the main functions
│
├── tests/
│   ├── js_for_testing/           # Test Files to avoid hitting live servers
│   │   ├── FemalePlayerCareer.js
│   │   └── MalePlayerCareer.js
│   └── test_cases.py             # Automated tests for data cleaning and processing
│
├── README.md
├── instructions.md
└── pyproject.toml
```