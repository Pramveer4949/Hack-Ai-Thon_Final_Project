# 💧 AquaGuard
### Community Water Quality & Usage Monitor

<p align="center">

  <strong>Monitor Water • Detect Problems • Understand Trends • Take Action</strong>

  <br><br>

  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-00B4D8?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/OOP-Implemented-00C896?style=for-the-badge" alt="OOP">
  <img src="https://img.shields.io/badge/SDG-6%20%7C%2012-0B7285?style=for-the-badge" alt="SDG">
  <img src="https://img.shields.io/badge/Status-Functional%20Prototype-22C55E?style=for-the-badge" alt="Status">

</p>

---

## 🌊 What is AquaGuard?

**AquaGuard** is a Python-based community water monitoring application designed to help households and communities understand their **daily water consumption** and basic **water-quality observations**.

Instead of simply storing numbers, AquaGuard converts water readings into meaningful information:

> **Input → Validation → Analysis → Alerts → Recommendations → Report**

The system allows users to record:

- 💧 Daily water consumption
- 🧪 pH value
- 🌫️ Turbidity
- 📍 Location
- 👤 User/recorded-by information
- 📅 Reading date

AquaGuard then checks the readings against predefined thresholds and identifies potentially abnormal conditions.

---

# 🎯 Problem We Are Solving

Water-related problems are not always immediately visible.

A household may:

- use more water than expected,
- experience increasing consumption,
- receive water with unusual pH,
- encounter high turbidity,
- or repeatedly record abnormal readings.

Without a simple monitoring system, these observations can remain disconnected pieces of data.

### AquaGuard solves this by creating a simple monitoring loop:

```text
       WATER DATA
           │
           ▼
   ┌─────────────────┐
   │ Record Reading  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Check Thresholds│
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Detect Anomaly   │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Generate Alerts  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Recommendations  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Monitoring Report│
   └─────────────────┘
