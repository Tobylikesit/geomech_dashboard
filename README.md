

<p align="center">
  <h3 align="center">README GEOMECH DASHBOARD</h3> <!-- EDIT -->
  <p align="center">
    Pandas and streamlit backed web application for my internship data analysis. <!-- EDIT -->
  </p>
</p>

<!-- EDIT: TABLE OF CONTENTS -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Run App](#run-app)
  - [Excel file requirements](#Excel-file-requirements)
- [Preview](#preview)
  - [Screenshot](#Screenshot)

<!-- EDIT: ABOUT THE PROJECT -->

## About The Project

Core data analysis datasheets combined on depth and well values for further correlations between columns.<!-- EDIT -->

### Built With

<!-- EDIT -->
- streamlit
- pandas
- numpy
- altair
- matplotlib

## Getting Started

<!-- EDIT -->
To get a local copy up and running follow these simple steps.

### Prerequisites

<!-- EDIT -->
Python3 installed on your local machine.

### Installation

#### 1. Clone the repo

```sh
git clone https://github.com/toqrul2000/geomech_dashboard
cd /toqrul2000/geomech_dashboard
```

#### 2. Install dependencies

```sh
pip install requirements.txt
```

## Usage
Choose columns for correlation, analyse interactive graphs and see regression coefficients.

### Run App

```sh
streamlit run main.py
```

### Excel file requirements
1. Excel file should contain multiple datasheets. (Due to the bug, will be fixed soon)
2. Each sheet should contain 'depth' and 'well' columns.
3. Order of sheets merging for combined/compiled data-table is the same as sheets order in original excel file.
4. Since join and merge methods are used related columns in different sheets should have the same column name.
5. Avoid having extra data(/charts) below or in the side of your table in excel file.
6. Load_data method uses data window resampling with 1 unit scale. (eg. 1234.5,1234.9 are combined into one 1234.0)

### Preview

You can check out a live preview at: [Demo Link](https://share.streamlit.io/toqrul2000/geomech_dashboard/main/main.py)

### Screenshot

![preview](https://github.com/toqrul2000/geomech_dashboard/blob/main/screencapture-share-streamlit-io-toqrul2000-geomech-dashboard-main-main-py-2021-08-22-04_40_08.png?raw=true)
