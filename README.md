# Ship Hydrostatics Toolbox ⚓  

This repository contains a Python-based toolbox for analyzing the **hydrostatics and structural responses of a ship hull**. The main script computes the ship’s **floating equilibrium, load distribution, shear force, and bending moment** based on given hull geometry and weight distribution.  

---

## 🚢 Features
- Reads ship **sectional data** (`SecLine.dat`) to compute hydrostatic properties.  
- Calculates:
  - **Load line** (weight vs buoyancy balance along stations)  
  - **Shear force distribution**  
  - **Bending moment distribution**  
- Iterative trimming and sinkage adjustment to match **LCG–LCB balance**.  
- Supports **weight distribution input** from `Ship_Data_Modified.xlsx`.  
- Plots:
  - Weight, buoyancy, and load line curves  
  - Shear force diagram  
  - Bending moment diagram  

---

## 📂 Repository Structure
```
├── 20NA30025_StructLab_A6.py     # Main driver script
├── HydrostaticsFunc.py           # Hydrostatics calculations (volume, LCB, WPA, etc.)
├── weightdistribution.py         # Ship weight distribution function
├── SecLine.dat                   # Sectional geometry data (input file)
├── hydrostatic.xlsx              # Hydrostatic particulars for interpolation 
```

---

## ▶️ Usage
1. Ensure the following input files are present:
   - `SecLine.dat` → sectional offsets  
   - `Ship_Data_Modified.xlsx` → weight distribution data  
   - `hydrostatic.xlsx` → hydrostatic particulars  

2. Run the main script:
   ```bash
   python 20NA30025_StructLab_A6.py
   ```

3. Output:
   - Converged **equilibrium draft** and **trim condition**  
   - Plots of load line, shear force, and bending moment  

---

## 📊 Example Output
- **Loadline curve**: comparison of buoyancy vs. weight along stations  
- **Shear force diagram**  
- **Bending moment diagram**  

---

## ⚠️ Requirements
- Python 3.x  
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `scipy`  

Install dependencies with:
```bash
pip install numpy pandas matplotlib scipy
```

---

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  
