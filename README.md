# Inventory Forecasting

There is an abundance of AI based projects that one could think of in e-commerce. Imagine a food based retailer, one of the major issue that a retailer usually faces is with the supply chain. Groceries are short-lived products. If a retailer under stocks, this will mean that they are at the risk of losing customers, but if they overstock, they are wasting money on excessive storage in addition to waste. We could leverage AI to help retailer better stock the products that they sell. Since the problem is very broad, we break it down to a specific business problem statement.

## Problem Statement

Based on the data provided, can we accurately predict the stock levels of products?

## Project Architecture

![Project_Architecture](/img/IMG-20240718-WA0008.jpg)

## Requirements

| Library                        | Description                                                             |
| ------------------------------ | ----------------------------------------------------------------------- |
| `mysql-connector-python`       | A library that provides connectivity to MySQL databases.                |
| `pandas`                       | A library for data manipulation and analysis.                           |
| `python-dotenv`                | A library for working with environment variables stored in a .env file. |
| `argparse`                     | A library for parsing command line arguments.                           |
| `os`                           | A library for interacting with the operating system.                    |
| `gspread`                      | A library for working with Google Sheets.                               |
| `oauth2client.service_account` | A library for authenticating with Google APIs using a service account.  |
| `prophet`                      | library for time series forecasting developed by Facebook.              |
| `boto3`                        | A library for interacting with AWS services using Python.               |

## PROJECT STRUCTURE

`NOTE: Anything in CAPS below are folder directories. `

```
├── README.md
├── DATA
│   ├── <all data>
├── SRC
│   ├── __init__.py
│   ├── <python scripts>
├── TESTS
│   ├── __init__.py
│   ├── <all test files>
├── CONFIG
│   ├── config.yml
│   ├── config_template.yml
├── .GITHUB
│   ├── pull_request_template.md
│   ├── WORKFLOW
│       ├── github-actions.yml
├── Docker
├── Makefile
├── requirements.txt
├── .gitignore
```

## Giving Credit

If you make changes to the code, it's important to give credit to the original project's author. You can do this by adding a note or comment to your code, or by including the original author's name and a link to the project in your documentation.

For example, if you add a new feature to the code, you could include a comment like this:

` // New feature added by [your name]. Original code by [original author name].`

`// Link to original project: [link to original project]`

## Working with the Code

Once you have cloned the repository, you can start working with the code. Here are some tips to get you started:

- Read the [User Guide](https://github.com/KshitizRana/Inventory-Forecasting#open_book-user-guide) and code comments to understand how the code works.
- Make changes to the code as needed, testing your changes to ensure they work correctly.
- If you want to contribute your changes back to the original project, create a pull request on Github. Be sure to include a detailed description of your changes and why they are important or necessary.

## User Guide

#### STEP - :one: : Navigate to the project directory in the terminal by running

```
cd <file location>
```

#### This step is necessary to ensure that you are in the correct directory where the project files are located.

#### STEP - :two: : Create a environment for project by running

```
conda create -n <your_env_name>
```

#### Once created activate the project environment

```
conda activate <your_env_name>
```

#### This step is necessary to activate the Conda environment that wil contain all the required [libraries and dependencies](https://github.com/KshitizRana/Inventory-Forecasting/blob/main/requirements.txt) for the project.

#### STEP- :: : Install all the requirements from the `requirements.txt`

```
pip install -r requirements.txt
```

#### STEP - :three: : Create the database by running the below code

```

```

#### This step creates the database with the specified name. The -cd argument specifies whether to create or drop the database, and -nd specifies the name of the database.

#### STEP - :four: : Load the data into the database by running

` `

#### This step loads the raw data into the database. The -nd argument specifies the name of the database, and -id specifies the operation to be performed (in this case, uploading data to the database).

#### STEP - :five: : Run the ETL script to transform the data by running

` `

#### This step performs the ETL (Extract-Transform-Load) process to transform the raw data into a format suitable for modeling.

#### STEP - :six: : Create the cleaned database by running

` `

#### This step creates a new database with the cleaned data.

#### STEP - :seven: : Load the cleaned data into the database by running

` `

#### This step loads the cleaned data into the database.

#### STEP - :eight: : Run main.py with task parameter

` `

#### This will execute the "main.py" script with the "sql_python" task parameter, triggering the SQL query and export process resulting output file (df) should be uploaded to the specified S3 bucket after the script completes execution.

#### STEP - :nine: : Run the final modeling script by running the code

` `

#### This step runs the final modeling script to build a predictive model based on the cleaned data. The -t argument specifies the type of script to run, and "modeling_final" is the name of the script and uploads the Predictions to a Google Sheet

## Contributing Guide

If you would like to contribute to this project, please create a pull request on an other branch so that we don't mess up main code: [Pull Request](https://github.com/KshitizRana/Inventory-Forecasting/compare)

## Conclusion

This project showcases the ability to handle real-world data and solve a problem using data science techniques. The project can be used as a reference for building similar projects in the future. Feel free to use the code and make modifications as per your requirements and don't forget to give credit.

## Created and Contributed by

[Kshitiz Rana](https://www.linkedin.com/in/kshitiz-rana-264457226)

[Data To Production (Mitul Patel Msc - Mentor)](https://www.linkedin.com/in/mitul-patel2393/)
