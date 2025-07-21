# Pump and Pipeline Correction Toolkit - Detailed Description

This project consists of a set of Python applications with graphical interfaces (Tkinter) for pump curve correction based on the ANSI/HI 9.6.7 standard and flow calculation in pressurized pipelines.

## Application Descriptions

### 1. Pump Correction - Example 1 (`app_01_pump_correction.py`)

- **Source:** Based on Example 1 from the ANSI/HI 9.6.7 manual.
- **Purpose:** Corrects the pump curve originally obtained with water for operating conditions with viscous fluids, using parameters such as flow rate, total head, rotation speed, kinematic viscosity, and efficiency.
- **Inputs:** Best Efficiency Point (BEP) flow rate, total head, rotation speed (RPM), water efficiency, fluid viscosity, specific gravity.
- **Outputs:** Corrected curves of head, efficiency, and power for various flow rates, as well as intermediate parameters (parameter B, correction factors Cq, Ch, Ceta).
- **Tools used:** The `pump_correction_tools.py` library contains the mathematical functions for calculations according to the ANSI/HI standard.

### 2. Pump Correction - Example 2 (`app_02_pump_correction.py`)

- **Source:** Based on Example 2 from the ANSI/HI 9.6.7 manual.
- **Purpose:** Performs the inverse correction where viscous fluid operating conditions are known, and the equivalent water performance is desired.
- **Inputs:** Flow rate and head operated with viscous fluid, viscosity, specific gravity, and water efficiency.
- **Outputs:** Parameter B, equivalent water flow and head, corrected efficiency, and power.
- **Difference:** The user inputs operational data and obtains corrections to interpret results in terms of water.

### 3. Pressurized Pipeline Flow Calculation (`app_03_pressurized_flow.py`)

- **Source:** Flow calculations for pressurized pipelines applied to industrial systems.
- **Purpose:** Calculates Reynolds number, friction factor (using an iterative method for Colebrook-White formula, pressure drop per meter, maximum pipe length based on pressure limits, total head, velocity, and mass flow rate.
- **Inputs:** Gravity, dynamic viscosity, density, maximum and minimum pressure, pressure drop divisor coefficient, volumetric flow rate, pipe diameter, pipe roughness.
- **Outputs:** Reynolds number, friction factor, pressure drop per meter, maximum pipe length, total head, mass flow rate, and velocity.
- **Tools used:** The `flow_resistance.py` library implements classical hydraulic calculations.

## Supporting Files

- **`pump_correction_tools.py`**: Implements mathematical functions based on ANSI/HI 9.6.7 standard for calculation of parameter B, correction factors for flow, head, and efficiency, power, and inverse parameters for pump performance analysis with viscous fluids.
  
- **`flow_resistance.py`**: Contains functions to calculate Reynolds number, friction factor by iterative method, and pressure drop using the Colebrook-White formula, applied to pipe flow.

## How to Use

- Run the `main_launcher.py` file to open a graphical menu allowing you to select which application to run.
- Or run the application files directly:  
  - `python app_01_pump_correction.py`  
  - `python app_02_pump_correction.py`  
  - `python app_03_pressurized_flow.py`  

- After entering the data in the interfaces, you will get graphs and results displayed.
- You can save the graphs and reports as PNG files in the `plots` folder.

## Requirements

- Python 3.8 or higher
- Libraries: `numpy`, `matplotlib`, `tkinter` (usually included with Python)

---

## About the Author

Created by **Gustavo Molin Dagostini**  
Version: **1.0.0**  
Contact: [gustavomolindagostini@gmail.com](mailto:gustavomolindagostini@gmail.com)

Final project for **EMC410235 – Programação Científica para Engenharia e Ciência Térmicas (2024/2), POSMEC/UFSC**. 

**EMC410235 – Scientific Programming for Engineering and Thermal Sciences (2024/2), POSMEC/UFSC**.

Supervised by **Prof. Dr. Rafael Lázaro de Cerqueira**  
Contact: [rafael.cerqueira@ufsc.br](mailto:rafael.cerqueira@ufsc.br)
---

## License

This project is currently unlicensed. You may choose any open source license or keep it proprietary as you wish.  

---

If you find this project useful or have questions, please feel free to reach out to the author.
