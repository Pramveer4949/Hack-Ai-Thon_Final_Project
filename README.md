# 💧 AquaGuard – Community Water Quality & Usage Monitor

> A simple Python-based water monitoring system that helps households, schools, and communities monitor water usage and basic water quality.

---

## 📌 Project Overview

**AquaGuard** is a Python-based water monitoring system developed for **Hack-AI-Thon 2026**.

The project records daily water consumption along with basic water-quality observations such as **pH** and **turbidity**. It checks the recorded values against selected thresholds and identifies potentially abnormal or unsafe conditions.

AquaGuard also generates:

- 💧 Water consumption information
- 🧪 Water quality status
- ⚠️ Alerts for abnormal readings
- 📈 Consumption trends
- 💡 Water conservation recommendations
- 📋 A complete monitoring report

---

## 🌍 SDG Alignment

AquaGuard supports two Sustainable Development Goals.

### 🟦 SDG 6 – Clean Water and Sanitation

The project helps monitor basic water-quality observations and identifies potentially unsafe conditions using pH and turbidity readings.

### 🟩 SDG 12 – Responsible Consumption and Production

The project monitors daily water consumption and identifies excessive usage to encourage responsible water use.

---

## ❓ Problem We Are Solving

Water wastage and poor awareness of water quality can become serious problems for households, schools, and communities.

People may not easily notice:

- Excessive daily water usage
- Possible water wastage
- Unusual pH values
- High turbidity
- Changes in water consumption over time

AquaGuard provides a simple way to record these observations and identify conditions that may need attention.

---

## 💡 Our Proposed Solution

AquaGuard uses Python and Object-Oriented Programming to create a simple water monitoring system.

The system:

1. Creates a monitored location.
2. Records the user responsible for the readings.
3. Stores daily water readings.
4. Checks pH, turbidity, and consumption values.
5. Detects abnormal conditions.
6. Generates alerts.
7. Calculates the consumption trend.
8. Provides conservation recommendations.
9. Produces a monitoring report.

---

## ✨ Key Features

### 📍 Location Management

Stores information about the monitored location:

- Location name
- Address
- Location type

### 👤 User Management

Stores information about the person recording the readings:

- User ID
- Name
- Role

### 💧 Water Usage Monitoring

Records daily water consumption in litres.

### 🧪 Water Quality Monitoring

Records:

- pH
- Turbidity

The system then determines whether the water quality is **Safe** or **Unsafe**.

### ⚠️ Abnormal Reading Detection

The system checks readings using project-defined demonstration thresholds.

| Parameter | Selected Threshold |
|---|---:|
| Minimum pH | 6.5 |
| Maximum pH | 8.5 |
| Maximum Turbidity | 5.0 NTU |
| Maximum Consumption | 500 L/day |

> **Note:** These thresholds are selected for the project demonstration. They are not numerical thresholds provided in the Hack-AI-Thon problem statement.

### 🚨 Alerts

AquaGuard generates alerts for abnormal conditions such as:

- Low pH
- High pH
- High turbidity
- High water consumption

### 📈 Consumption Trend

The system compares water consumption readings and identifies whether usage is:

- Increasing
- Decreasing
- Stable
- Not enough data

### 💡 Recommendations

The system provides simple recommendations based on detected conditions, such as:

- Reducing excessive water usage
- Checking for possible leaks
- Further testing of abnormal water-quality readings
- Considering filtration when turbidity is high

### 📋 Monitoring Report

The final report contains:

- Location information
- User information
- Number of readings
- Average consumption
- Consumption trend
- Water-quality status
- Alerts
- Recommendations

---

## 🏗️ OOP Structure

AquaGuard uses four main classes.

### `Location`

Represents the place where water is being monitored.

```text
Location
 ├── name
 ├── address
 └── location_type
```

### `User`

Represents the person recording or generating the water readings.

```text
User
 ├── user_id
 ├── name
 └── role
```

### `WaterReading`

Stores one day's water monitoring data.

```text
WaterReading
 ├── reading_date
 ├── location
 ├── recorded_by
 ├── consumption
 ├── pH
 └── turbidity
```

This class checks the readings, determines water quality, and generates alerts for abnormal values.

### `MonitoringReport`

Generates the complete monitoring report.

It handles:

- Average water consumption
- Consumption trend
- Alerts
- Recommendations
- Final report generation

---

## 🔄 How It Works

```text
        📍 Location
             ↓
          👤 User
             ↓
      💧 Water Reading
             ↓
    ┌────────┼────────┐
    ↓        ↓        ↓
  Usage      pH    Turbidity
    └────────┼────────┘
             ↓
    🔍 Check Thresholds
             ↓
       ⚠️ Detect Alerts
             ↓
       📈 Find Trend
             ↓
       💡 Recommendations
             ↓
       📋 Final Report
```

---

## 🛠️ Technologies Used

- **Python 3**
- **Object-Oriented Programming (OOP)**
- Python Standard Library
- `datetime`
- `typing`

No external libraries, APIs, databases, or internet connection are required.

---

## 📂 Project Structure

```text
AquaGuard/
│
├── main.py
├── README.md
└── screenshots/
    ├── output.png
    └── report.png
```

### `main.py`

Contains the complete AquaGuard Python program, including the classes, sample data, calculations, alerts, recommendations, and report generation.

### `README.md`

Contains the project documentation and instructions for running the project.

### `screenshots/`

Contains screenshots of the program output and monitoring report.

---

## ▶️ How to Run

### Requirements

- Python 3.8 or newer
- Any Python code editor or IDE
- Command Prompt / Terminal

No additional packages are required.

### Run the Project

Open the AquaGuard project folder in a terminal and run:

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

The program will display the AquaGuard monitoring report in the terminal.

---

## 📊 Sample Data

The project uses sample data to demonstrate the monitoring system.

### 📍 Location

```text
House 12B
Green Park Colony
Household
```

### 👤 User

```text
U101
Priya Sharma
Resident
```

### 💧 Water Readings

| Date | Consumption | pH | Turbidity |
|---|---:|---:|---:|
| 2026-09-10 | 320 L | 7.1 | 2.3 NTU |
| 2026-09-11 | 450 L | 6.2 | 6.8 NTU |
| 2026-09-12 | 510 L | 7.4 | 3.1 NTU |

The sample data demonstrates both normal and abnormal conditions.

---

## 🖼️ Screenshots

### 💻 Program Output

> 📸 **INSERT YOUR PROGRAM OUTPUT SCREENSHOT HERE**

![AquaGuard Program Output](screenshots/output.png)

---

### 📋 Monitoring Report

> 📸 **INSERT YOUR MONITORING REPORT SCREENSHOT HERE**

![AquaGuard Monitoring Report](screenshots/report.png)

---

## 🧪 Testing

AquaGuard was tested using representative sample data.

### ✅ Normal Reading

```text
Consumption: 320 L
pH: 7.1
Turbidity: 2.3 NTU
```

Expected result:

```text
Quality: Safe
```

### ⚠️ Abnormal Water Quality

```text
Consumption: 450 L
pH: 6.2
Turbidity: 6.8 NTU
```

Expected result:

```text
Quality: Unsafe
```

The system generates alerts for low pH and high turbidity.

### 🚨 Excessive Consumption

```text
Consumption: 510 L
```

Expected result:

```text
High consumption alert
```

---

## ⚠️ Limitations

The current version is a simple functional prototype.

- Data is currently stored directly in the Python program.
- No database is used.
- No physical water sensors are connected.
- No internet or external APIs are used.
- Only pH and turbidity are monitored for water quality.
- Trend analysis uses a simple first-reading vs last-reading comparison.
- Thresholds are project-defined demonstration values.

---

## 🚀 Future Improvements

The project could be improved in the future by adding:

- 🖥️ A graphical user interface
- 🗄️ Database storage
- 📡 Real-time water sensors
- 🧪 More water-quality parameters
- 📊 Advanced trend analysis
- 📈 Charts and dashboards
- 🏘️ Multiple household/location support
- 🤖 Automatic data collection

These features are outside the scope of the current prototype.

---

## 🎯 Project Objectives

The main objectives of AquaGuard are to:

1. Monitor daily water consumption.
2. Record basic water-quality observations.
3. Detect abnormal conditions.
4. Generate useful alerts.
5. Identify consumption trends.
6. Encourage responsible water usage.
7. Demonstrate Python fundamentals and Object-Oriented Programming.
8. Support SDG 6 and SDG 12.

---

## 👥 Intended Users

AquaGuard can be adapted for:

- 🏠 Households
- 🏫 Schools
- 🏘️ Communities

The current demonstration uses a household example.

---

## 📌 Hack-AI-Thon Requirements Covered

| Requirement | AquaGuard |
|---|---|
| `Location/User` class | ✅ |
| `WaterReading` class | ✅ |
| `MonitoringReport` class | ✅ |
| Daily consumption | ✅ |
| pH | ✅ |
| Turbidity | ✅ |
| Abnormal reading detection | ✅ |
| Alerts | ✅ |
| Recommendations | ✅ |
| Consumption trends | ✅ |
| Monitoring report | ✅ |
| Python + OOP | ✅ |

---

## 🌱 SDG Impact

### SDG 6 – Clean Water and Sanitation

AquaGuard helps users become more aware of basic water-quality conditions by identifying abnormal pH and turbidity readings.

### SDG 12 – Responsible Consumption and Production

AquaGuard encourages responsible water consumption by identifying excessive usage and providing conservation recommendations.

---

## 📌 Project Information

**Project Name:** AquaGuard – Community Water Quality & Usage Monitor

**Event:** Hack-AI-Thon 2026

**Theme:** Python Fundamentals + Object-Oriented Programming + Sustainable Development Goals

**SDGs:**

- SDG 6 – Clean Water and Sanitation
- SDG 12 – Responsible Consumption and Production

**Programming Language:** Python 3

**Project Type:** Functional Python Prototype

---

# 💧 AquaGuard

### Monitor Water • Detect Problems • Conserve Resources

**Built for Hack-AI-Thon 2026**

**SDG 6 • SDG 12**
