# Customer-Segmentation-Churn-Pattern-Analytics-in-European-Banking

“Hello everyone.

Welcome to my project: Customer Segmentation and Churn Pattern Analytics in European Banking.

This project analyzes customer churn patterns in a European banking dataset containing 10,000 customer records. The objective is to identify customer segments with elevated churn risk and translate the findings into actionable retention and policy recommendations.

The project was developed using Python, Pandas, NumPy, and Streamlit. Python and Pandas were used for data loading, cleaning, validation, customer segmentation, and exploratory data analysis. Streamlit was used to create an interactive dashboard for live exploration of the churn patterns.

The workflow began with data validation. I checked the dataset structure, data types, missing values, and binary variables such as customer activity status and churn status. The dataset had no missing values, and the churn variable was validated as a binary outcome where Exited equals one represents a customer leaving the bank.

Next, I created segmentation variables for age, credit score, tenure, balance level, geography, and customer activity. I also defined premium customers as those whose account balance falls in the top 25 percent of the dataset.

The analysis found an overall churn rate of 20.37%. Germany showed the highest churn rate at 32.44%. Customers aged 46 to 60 recorded the highest churn rate, at more than 51%. Inactive members had a churn rate of 26.85%, compared with 14.27% among active members.

The analysis also highlights potential high-value customer risk. Premium-balance customers had a churn rate of 23.68%, showing that churn is not limited to low-value accounts.

This repository includes three main deliverables: a research paper with exploratory data analysis and recommendations, an executive summary for government and supervisory stakeholders, and a Streamlit dashboard with dynamic filters and interactive visualizations.

The dashboard allows users to explore churn by geography, age group, gender, tenure, account balance, activity level, and product holdings. It also supports drill-down analysis for premium customers.

The key recommendations are to develop early-warning systems for inactive and high-balance customers, investigate country-specific churn drivers in Germany, improve retention strategies for higher-risk age segments, and apply fairness and human oversight when using customer segmentation for decision-making.

This project is exploratory and descriptive. It does not establish causality. Future improvements could include transaction history, complaint data, product fees, monthly customer activity, and predictive machine-learning models.

Thank you for visiting the project. Please explore the dashboard, review the report, and feel free to share feedback or suggestions.”
