# 🌿 Algae Biomass Growth Simulation — Chilika Lagoon (2015–2024)

**Author:** Sayed Umair Ali
**Date:** July 2025  
**Location:** Chilika Lagoon, Odisha, India

## 📌 Overview

This repository contains the codebase, dataset, and analysis for a decadal simulation of algae biomass growth in the **Chilika Lagoon**, India’s largest brackish water lagoon. The study models how **climate variables** like temperature, sunlight, and nutrients affect three key algae species from 2015 to 2024.

## 🧪 Objective

To evaluate and compare the biomass growth potential of three economically and ecologically important algae species under **real-world climate conditions** using simulation techniques.

## 🌱 Target Algae Species

| Species               | Common Use           | Optimal Conditions (Temp °C / Nutrient / Sun h) |
|----------------------|----------------------|-------------------------------------------------|
| Ulva lactuca         | Food, feed, biofuel  | 30 / 3.0 / 6                                     |
| Hypnea musciformis   | Agar, pharma         | 28 / 2.8 / 7                                     |
| Caulerpa racemosa    | Aquaculture, salad   | 32 / 4.0 / 5                                     |

## 📊 Data Sources

- **Climate Data:** NASA POWER API (2015–2024)
- **Parameters:** Monthly max temperature (°C), sunlight (hrs), and precipitation (mm)
- **Nutrient Levels:** Simulated due to lack of public data

## 🔬 Methodology

- Developed a **linear tolerance-based growth function** for algae
- Simulated cumulative biomass growth using climate-driven scoring
- Plotted monthly biomass trends using Matplotlib and Seaborn

### Growth Equation

```python
biomass = biomass * 0.9 + growth
growth = 80 * temp_score * nut_score * sun_score
