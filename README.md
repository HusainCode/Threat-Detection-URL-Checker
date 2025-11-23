## Project Status

[![Project Status](https://img.shields.io/badge/status-completed-brightgreen)]()

# Threat Detection URL Checker

Threat Detection URL Checker is a Python-based tool that analyzes URLs using the Google Web Risk API, logs categorized results into CSV files, and visualizes threat data. It is designed with modular components, supports automation through CI/CD, and includes full documentation.


## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Core Components](#core-components)
- [Project Structure](#project-structure)
- [Testing & CI](#automated-testing--ci)
- [Installation](#installation)
- [Output](#output)
- [Technologies Used](#technologies-used)
- [Documentation](#documentation)
- [Video Explanation](#video-explanation)
- [Author](#author)

## Features

- Asynchronous URL scanning using the Google Web Risk API
- Categorizes results into threat types or safe
- Logs and saves results to CSV
- Generates a threat distribution chart using matplotlib
- Structured logging for debugging and traceability
- Unit tested using `unittest`
- GitHub Actions CI for automatic test runs
- Public documentation hosted on Confluence
- Video walkthrough available on YouTube

---

# 🏗️ Architecture Overview

Below is the **architecture design** of the project, which outlines the **core components** and their **interactions**.

![image](https://github.com/user-attachments/assets/f8643f1e-f990-4dd0-8c62-9f93ecbbea34)

---

## 📦 Core Modules

| Component         | Responsibility |
|------------------|----------------|
| `APIHandler`     | Interacts with Google Web Risk API to analyze URLs for threats. Manages concurrency and async processing. |
| `CSVHandler`     | Loads input URLs from CSV and saves threat analysis results. Also calculates threat-type percentages. |
| `Logger`         | Handles centralized logging of info, warnings, and errors to a log file. |
| `ThreatAnalyzer` | Reads results and generates visual charts (pie chart of threat types) using `matplotlib`. |
| `main.py`        | Entry point. Orchestrates the entire analysis flow  loading data, calling the API, saving results, and generating charts. |

---

## 🧪 Testing Modules

| Test File                  | Description |
|---------------------------|-------------|
| `test_api_handler.py`     | Tests the initialization and threat-type config of `APIHandler`. |
| `test_csv_writer.py`      | Tests CSV read/write and percentage logic in `CSVHandler`. |
| `test_threat_analyzer.py` | Tests chart generation and empty-data handling in `ThreatAnalyzer`. |

---

## 🔁 Component Interactions

1. `main.py` initializes:
   - `Logger`
   - `CSVHandler`
   - `APIHandler`
   - `ThreatAnalyzer`

2. `APIHandler`:
   - Uses `CSVHandler` to load URLs
   - Uses `Logger` to log the scanning process
   - Sends requests to **Google Web Risk API**

3. After scanning:
   - Results are saved via `CSVHandler`
   - `ThreatAnalyzer` reads results and generates a pie chart

4. Logs, results, and chart are stored in the `resources/` folder.

---

> 💡 All environment variables and paths are defined in `.env` for centralized configuration.


### Core Components

- `APIHandler` → Fetches the list of public API URLs from a CSV file  
- `ThreatAnalyzer` → Sends URLs to the Google Web Risk API and determines their status  
- `CSVHandler` → Saves results into `results.csv` and calculates threat percentages  
- `Logger` → Logs errors, API failures, and other issues for debugging

---

## Project Structure

```text
Multithreaded-URL-Checker/
├── threat_analyzer/
│   ├── api_handler.py
│   ├── csv_handler.py
│   ├── logger.py
│   ├── threat_analyzer.py
│   └── test/
│       ├── test_api_handler.py
│       ├── test_csv_writer.py
│       └── test_threat_analyzer.py
├── resources/
│   ├── key.json
│   ├── results.csv
│   └── threat_analysis_chart.png
├── data/
│   └── PublicAPIslist.csv
├── .github/workflows/
│   └── python-tests.yml
├── .env
├── Dockerfile
├── requirements.txt
└── README.md
```

## Automated Testing & CI
- Note: GitHub Actions is configured but currently inactive due to free tier CI usage limits.
- Tests are written using Python's built in unittest module
- GitHub Actions automatically runs tests on every push and pull request to main

Run tests locally:

```bash
python -m unittest discover -s threat_analyzer/test
```

## CI Status

![CI](https://github.com/HusainCode/Threat-Detection-URL-Checker/actions/workflows/python-tests.yml/badge.svg)

## Technologies Used

- Python 3.10+
- Google Web Risk API
- pandas
- asyncio
- matplotlib
- unittest
- GitHub Actions
- Docker (optional)

## Video Explanation

Watch the full walkthrough of this project on YouTube:
(in progress)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Threat-Detection-URL-Checker.git
cd Threat-Detection-URL-Checker
```

Create a .env file:

```env
CSV_FILE=data/PublicAPIslist.csv
RESULTS_FILE=resources/results.csv
CHART_FILE=resources/threat_analysis_chart.png
GOOGLE_API_KEY=your_api_key
GOOGLE_APPLICATION_CREDENTIALS=resources/key.json
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python threat_analyzer/main.py
```

## Output

- resources/results.csv → Results of all URL scans
- resources/threat_analysis_chart.png → Threat type distribution chart


## Author


