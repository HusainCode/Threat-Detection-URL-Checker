![Project Status](https://img.shields.io/badge/status-in_progress-yellow)

# Threat Detection URL Checker 🚀  

**Threat Detection URL Checker** is a Python tool that retrieves a list of public API URLs, checks if they are classified as **threats or safe** using the **Google Web Risk API**, and logs the results into separate **CSV files**.

For more details, refer to the official Google Web Risk API documentation:  
[Google Web Risk API Samples](https://cloud.google.com/web-risk/docs/samples)


## 📌 Features  
✅ Fetches and processes multiple URLs using **multithreading**.  
✅ Sends URLs to **Google Web Risk API** for threat analysis.  
✅ Categorizes results into **"threat"** and **"safe"** CSV files.  
✅ Handles **timeouts, connection failures**, and logs errors efficiently.  

## 📜 Initial Design  
Below is the initial design of the project, which includes the core components and their interactions:  

![image](https://github.com/user-attachments/assets/b696c095-b182-4159-b536-4562942b82df)

### **Core Components**  
- **`URLChecker`** → Manages the overall process of checking URLs.  
- **`APIHandler`** → Fetches the list of public API URLs from a CSV file.  
- **`ThreatAnalyzer`** → Sends URLs to the **Google Web Risk API** and determines their status.  
- **`CSVWriter`** → Saves results into **safe_urls.csv** and **threat_urls.csv**.  
- **`Logger`** → Logs errors, API failures, and other issues for debugging.  

⚠️ **Note:** This is the **initial design**, and modifications may be made as the project evolves.  

## 📦 Installation  

