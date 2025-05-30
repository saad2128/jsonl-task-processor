# Task Distribution System

A comprehensive Python tool for distributing JSONL task data across development teams based on capacity, while maintaining repository integrity and sequential task assignment.

## 🚀 Features

### Core Functionality
- **JSONL to CSV Conversion** - Complete data preservation with clean formatting
- **Repository-Based Sorting** - Logical grouping by repository names
- **Sequential Serial Numbers** - Maintains order from 1 to total tasks
- **Capacity-Based Distribution** - Teams get tasks based on developer count
- **Repository Integrity** - Same repo tasks stay with same team
- **Professional Reporting** - Comprehensive Markdown analytics

### Team Management
- **Interactive Configuration** - Lead names and developer counts
- **Automatic Capacity Calculation** - `developers × 5 tasks/day × 5 working days`
- **Balanced Workload Distribution** - Optimized task assignment
- **Flexible Team Sizes** - Support for varying team configurations

### Output Organization
```
project/
├── input_complete.csv                 # Original JSONL data as CSV
├── input_sorted_with_serial.csv       # Processed data with serial numbers
└── task_distribution/
    ├── week_1/
    │   ├── team_1_John_Smith.csv      # Sequential assignments
    │   ├── team_2_Jane_Doe.csv
    │   └── team_3_Mike_Johnson.csv
    ├── week_2/
    │   └── ...
    └── distribution_report.md          # Comprehensive analytics
```

## 📋 Requirements

```python
pandas>=1.3.0
pathlib
json
math
datetime
```

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/task-distribution-system.git
cd task-distribution-system
```

2. **Install dependencies:**
```bash
pip install pandas
```

3. **Prepare your JSONL file:**
Ensure your JSONL file contains a `repo_name` column for proper task grouping.

## 🚀 Usage

### Basic Command
```bash
python task_distribution.py input.jsonl
```

### Interactive Setup
```bash
# The script will prompt for:
Enter number of teams: 3

Team 1:
Enter lead name for Team 1: John Smith
Enter number of developers for Team 1: 7
Team 1 - Lead: John Smith, Developers: 7, Weekly Capacity: 175 tasks

Team 2:
Enter lead name for Team 2: Jane Doe
Enter number of developers for Team 2: 5
Team 2 - Lead: Jane Doe, Developers: 5, Weekly Capacity: 125 tasks

Team 3:
Enter lead name for Team 3: Mike Johnson
Enter number of developers for Team 3: 6
Team 3 - Lead: Mike Johnson, Developers: 6, Weekly Capacity: 150 tasks
```

## 📊 Sample Output

### Distribution Summary
```
=== Distribution Complete ===
Total tasks processed: 5000
Weekly batches created: 12
Teams configured: 3
Total weekly capacity: 450 tasks
Estimated completion time: 12 weeks

Week 1: 450 tasks (Serial: 1-450)
Week 2: 450 tasks (Serial: 451-900)
Week 3: 450 tasks (Serial: 901-1350)
...
```

### Markdown Report Preview
```markdown
# Task Distribution Report

## Overall Summary
| Metric | Value |
|--------|-------|
| Total Tasks | 5000 |
| Total Weeks | 12 |
| Total Teams | 3 |

## Team Information
| Team | Lead Name | Developers | Weekly Capacity | Formula |
|------|-----------|------------|-----------------|---------|
| 1 | John Smith | 7 | 175 | 7 × 5 × 5 |
| 2 | Jane Doe | 5 | 125 | 5 × 5 × 5 |
| 3 | Mike Johnson | 6 | 150 | 6 × 5 × 5 |
```

## 🏗️ Algorithm Details

### Sequential Assignment Strategy
1. **Repository Sorting** - Repositories ordered by minimum serial number
2. **Capacity-Based Assignment** - Teams get repositories based on available capacity
3. **Sequential Overflow** - When team reaches capacity, next team continues sequence
4. **Repository Integrity** - Never split repositories between teams

### Capacity Calculation
```
Weekly Capacity = Developers × 5 tasks/day × 5 working days
```

### Example Serial Distribution
```
Team 1: Serial 1-175    (175 tasks, 100% capacity)
Team 2: Serial 176-300  (125 tasks, 100% capacity)  
Team 3: Serial 301-450  (150 tasks, 100% capacity)
```

## 📈 Reporting Features

### Capacity Analysis
- **Utilization Percentages** - Track team efficiency
- **Repository Distribution** - Tasks per repository per team
- **Timeline Estimation** - Project completion forecasting
- **Workload Balance** - Fair distribution metrics

### Professional Tables
- **Team Information** - Leads, developers, capacities
- **Weekly Distribution** - Tasks, serial ranges, utilization
- **Repository Breakdown** - Detailed assignment tracking

## 🔍 Use Cases

### Sprint Planning
- Distribute user stories across teams
- Balance workload based on team size
- Maintain feature ownership per team

### Large-Scale Projects
- Handle thousands of tasks efficiently
- Track progress with serial numbers
- Generate executive-level reports

### Resource Planning
- Calculate project timelines
- Optimize team utilization
- Plan capacity for future sprints

## 🛠️ Configuration Options

### Team Setup
- **Variable Team Sizes** - 1-50+ developers per team
- **Custom Lead Names** - Personalized file naming
- **Flexible Capacity** - Automatic calculation based on team size

### Output Customization
- **Organized Folders** - Week and team-based structure
- **CSV Format** - Compatible with Excel, Google Sheets
- **Markdown Reports** - Professional documentation

## 📝 Data Requirements

### JSONL Format
Your input file must be valid JSONL with a `repo_name` field:
```json
{"task_id": "T001", "repo_name": "frontend-app", "description": "Fix login bug"}
{"task_id": "T002", "repo_name": "backend-api", "description": "Add user endpoint"}
```

### Required Fields
- **repo_name** - Repository identifier (required for grouping)
- **Additional fields** - Preserved in output files

## 📋 Input File Example

Create a sample JSONL file (`tasks.jsonl`):
```json
{"task_id": "T001", "repo_name": "frontend-app", "description": "Implement user authentication", "priority": "high"}
{"task_id": "T002", "repo_name": "backend-api", "description": "Create user endpoint", "priority": "medium"}
{"task_id": "T003", "repo_name": "frontend-app", "description": "Add login form validation", "priority": "medium"}
{"task_id": "T004", "repo_name": "database", "description": "Optimize user table queries", "priority": "low"}
{"task_id": "T005", "repo_name": "backend-api", "description": "Add JWT token validation", "priority": "high"}
```

Then run:
```bash
python task_distribution.py tasks.jsonl
```

## 🚀 Quick Start Example

1. **Create a sample JSONL file:**
```bash
echo '{"task_id": "T001", "repo_name": "frontend", "description": "Task 1"}
{"task_id": "T002", "repo_name": "backend", "description": "Task 2"}
{"task_id": "T003", "repo_name": "frontend", "description": "Task 3"}' > sample_tasks.jsonl
```

2. **Run the distribution:**
```bash
python task_distribution.py sample_tasks.jsonl
```

3. **Follow the prompts:**
```
Enter number of teams: 2
Enter lead name for Team 1: Alice
Enter number of developers for Team 1: 3
Enter lead name for Team 2: Bob
Enter number of developers for Team 2: 2
```

4. **Check the results:**
```bash
ls task_distribution/week_1/
# Output: team_1_Alice.csv  team_2_Bob.csv
```

## 📊 Generated Files Explained

| File | Description | Contains |
|------|-------------|----------|
| `input_complete.csv` | Original JSONL data as CSV | All original fields preserved |
| `input_sorted_with_serial.csv` | Processed data | Original data + serial numbers, sorted by repo |
| `team_X_LeadName.csv` | Team assignments | Tasks assigned to specific team |
| `distribution_report.md` | Analytics report | Capacity analysis, utilization metrics |

## 🔧 Advanced Configuration

### Custom Capacity Settings
To modify the default capacity calculation (5 tasks/day × 5 days), edit the script:
```python
# Change this line in get_team_info():
weekly_capacity = num_developers * 5 * 5  # tasks_per_day * working_days
```

### Output Directory Customization
```python
# Change base output directory:
distribution_report = create_folder_structure_and_save(
    weekly_batches, teams_info, 
    base_output_dir="custom_output_folder"
)
```

## 🐛 Troubleshooting

### Common Issues

1. **"repo_name column not found"**
   - Ensure your JSONL file has a `repo_name` field
   - Check for typos in the field name

2. **"File not found"**
   - Verify the JSONL file path is correct
   - Use absolute path if needed: `python script.py /full/path/to/file.jsonl`

3. **Empty team assignments**
   - Check if total team capacity exceeds available tasks
   - Verify JSONL file is not empty

4. **Invalid JSONL format**
   - Each line must be valid JSON
   - Use online JSON validators to check format

### Debug Mode
Add print statements to see processing details:
```python
# Add this after sorting:
print(f"Sample data: {sorted_df.head()}")
print(f"Repositories found: {sorted_df['repo_name'].unique()}")
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Add tests for new functionality**
4. **Commit your changes:**
   ```bash
   git commit -m "feat: Add amazing feature"
   ```
5. **Push to the branch:**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Submit a pull request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/task-distribution-system.git
cd task-distribution-system

# Install development dependencies
pip install pandas pytest

# Run tests (when available)
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Task Distribution System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🆘 Support

For issues and questions:

### GitHub Issues
1. **Search existing issues** to avoid duplicates
2. **Create a new issue** with detailed description
3. **Include sample data** and error messages
4. **Use issue templates** when available

### Issue Template
```markdown
**Bug Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Run command: `python task_distribution.py file.jsonl`
2. Enter team configuration: ...
3. See error: ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 10, macOS, Ubuntu]
- Python version: [e.g., 3.8.5]
- Pandas version: [e.g., 1.3.0]

**Sample Data:**
```json
{"task_id": "T001", "repo_name": "test", "description": "sample"}
```

**Error Message:**
```
Paste full error traceback here
```
```

### Community Support
- **Discord/Slack** - [Link when available]
- **Email** - support@taskdistribution.com
- **Documentation** - [Wiki link when available]

## 🏆 Acknowledgments

- **Pandas team** - For excellent data manipulation capabilities
- **Python community** - For robust standard library
- **Contributors** - Everyone who helps improve this tool

## 🔮 Roadmap

### Version 2.0 (Planned)
- [ ] **GUI Interface** - Web-based task distribution
- [ ] **Database Integration** - PostgreSQL/MySQL support
- [ ] **API Endpoints** - REST API for integration
- [ ] **Advanced Analytics** - Predictive capacity planning

### Version 1.5 (In Progress)
- [ ] **Excel Output** - Direct .xlsx file generation
- [ ] **Custom Metrics** - Configurable task difficulty weights
- [ ] **Team Templates** - Pre-saved team configurations
- [ ] **Batch Processing** - Multiple JSONL files at once

### Community Requests
- [ ] **Jira Integration** - Direct import from Jira
- [ ] **Slack Notifications** - Team assignment alerts
- [ ] **Docker Support** - Containerized deployment
- [ ] **CI/CD Integration** - GitHub Actions support

---
