# FastBox Delivery System 📦

A logistics simulator for FastBox delivery company that optimizes package delivery using intelligent agent assignment.

## 👤 Author Information
- **Name:** Rohan Sonawane
- **Email:** rohannso14@gmail.com
- **GitHub:** @rohannso
- **Submission Date:** May 26, 2026

## 📋 Project Overview

This project simulates one day of delivery operations for FastBox, a fictional delivery company. The system assigns packages to the nearest delivery agents, simulates delivery routes, calculates total distances and efficiency metrics, and generates comprehensive reports.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

### Installation & Running

1. **Clone the repository**
```bash
   git clone https://github.com/rohannso/fastbox-delivery-system.git
   cd fastbox-delivery-system
```

2. **Create virtual environment (optional)**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Run a single test case**
```bash
   python delivery_simulator.py test_cases/test_case_1.json
```

4. **Run with bonus features**
```bash
   python delivery_simulator.py test_cases/test_case_1.json --visualize --export-csv
```

5. **Run all test cases at once**
```bash
   python run_all_tests.py
```

## 📊 Features Implemented

### Core Requirements ✅
- ✅ JSON parsing and data loading
- ✅ Euclidean distance calculation
- ✅ Nearest-agent package assignment
- ✅ Complete delivery simulation
- ✅ JSON report generation
- ✅ Best agent identification

### Bonus Features ✅
- ✅ ASCII route visualization (`--visualize`)
- ✅ CSV export for agent performance (`--export-csv`)
- ✅ Batch processing (all test cases)
- ✅ Comprehensive error handling
- ✅ Detailed code comments
- ✅ Performance metrics

## 📁 Project Structure

```
fastbox-delivery-system/
│
├── delivery_simulator.py       # Main simulation engine
├── run_all_tests.py            # Batch test runner
│
├── test_cases/                 # Input JSON test files (10 files)
│   └── test_case_*.json
│
├── reports/                    # Generated JSON reports
│   ├── report_*.json
│   └── batch_summary.json
│
├── outputs/                    # CSV exports & visualizations
│   ├── visualization_*.txt
│   └── performance_*.csv
│
├── README.md                   # Project documentation
├── ASSUMPTIONS.md              # Design decisions        
└── .gitignore                  # Git ignore rules
```
## 🧮 Algorithm Design

### Package Assignment Logic
For each package, the system calculates the Euclidean distance from every agent to the package's warehouse and assigns it to the nearest agent.

### Delivery Simulation
Each agent follows this route:
1. Start at initial position
2. Travel to warehouse to pick up package
3. Travel from warehouse to destination
4. Update position to destination (for next delivery)

### Efficiency Calculation
Efficiency = Total Distance Traveled / Number of Packages Delivered

Lower efficiency = Better performance

## 📈 Test Results

All 10 test cases passed successfully:
- ✅ test_case_1.json - Best Agent: A1
- ✅ test_case_2.json - Best Agent: A1
- ✅ test_case_3.json - Best Agent: A3
- ✅ test_case_4.json - Best Agent: A3
- ✅ test_case_5.json - Best Agent: A3
- ✅ test_case_6.json - Best Agent: A3
- ✅ test_case_7.json - Best Agent: A3
- ✅ test_case_8.json - Best Agent: A1
- ✅ test_case_9.json - Best Agent: A3
- ✅ test_case_10.json - Best Agent: A4

**Total Execution Time:** < 1 second

## 📝 Assumptions & Design Decisions

See `ASSUMPTIONS.md` for detailed documentation of all assumptions made during development.

Key assumptions:
- Distance calculated from agent to warehouse (not destination)
- Agent position updates after each delivery
- Packages delivered in order they appear in JSON
- Tie-breaking: first agent in data structure wins
- Only active agents (delivered ≥1 package) eligible for "best agent"



## 🛠️ Technologies Used

- **Language:** Python 3.12
- **Libraries:** 
  - `json` - Data parsing
  - `math` - Distance calculations
  - `csv` - CSV export
  - `sys`, `os` - File operations
  - `time` - Performance metrics

## 📞 Contact

For any questions or clarifications:
- Email: rohannso14@gmai.com
- GitHub: @rohannso

