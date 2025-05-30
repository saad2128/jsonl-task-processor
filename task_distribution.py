import json
import pandas as pd
import os
import math
from pathlib import Path
from datetime import datetime

def jsonl_to_csv(jsonl_file_path, csv_file_path):
    """Convert JSONL file to CSV format"""
    print(f"Converting {jsonl_file_path} to CSV...")
    
    data = []
    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                json_obj = json.loads(line.strip())
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
                continue
    
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)
    print(f"Complete CSV file created: {csv_file_path}")
    return df

def sort_by_repo_name_and_add_serial(df):
    """Sort dataframe by repo_name column and add serial number column at the beginning"""
    print("Sorting data by repo_name...")
    
    if 'repo_name' not in df.columns:
        print("Warning: 'repo_name' column not found. Available columns:", df.columns.tolist())
        return df
    
    # Sort by repo_name
    sorted_df = df.sort_values('repo_name').reset_index(drop=True)
    
    # Add serial number column at the beginning
    sorted_df.insert(0, 'serial_no', range(1, len(sorted_df) + 1))
    
    print(f"Data sorted and serial numbers added. Total rows: {len(sorted_df)}")
    return sorted_df

def get_team_info(num_teams):
    """Get team information from user"""
    teams_info = []
    
    print(f"\n=== Team Information Collection ===")
    for i in range(1, num_teams + 1):
        print(f"\nTeam {i}:")
        lead_name = input(f"Enter lead name for Team {i}: ").strip()
        
        while True:
            try:
                num_developers = int(input(f"Enter number of developers for Team {i}: "))
                if num_developers > 0:
                    break
                else:
                    print("Number of developers must be positive!")
            except ValueError:
                print("Please enter a valid number!")
        
        # Calculate weekly capacity: developers * 5 tasks/day * 5 working days
        weekly_capacity = num_developers * 5 * 5
        
        teams_info.append({
            'team_number': i,
            'lead_name': lead_name,
            'num_developers': num_developers,
            'weekly_capacity': weekly_capacity
        })
        
        print(f"Team {i} - Lead: {lead_name}, Developers: {num_developers}, Weekly Capacity: {weekly_capacity} tasks")
    
    return teams_info

def create_capacity_based_batches(df, teams_info):
    """Create weekly batches based on total team capacity"""
    total_weekly_capacity = sum(team['weekly_capacity'] for team in teams_info)
    total_tasks = len(df)
    
    print(f"\nTotal weekly capacity: {total_weekly_capacity} tasks")
    print(f"Total tasks to distribute: {total_tasks}")
    
    # Calculate number of weeks needed
    weeks_needed = math.ceil(total_tasks / total_weekly_capacity)
    print(f"Estimated weeks needed: {weeks_needed}")
    
    # Create batches based on weekly capacity
    batches = []
    for week in range(weeks_needed):
        start_idx = week * total_weekly_capacity
        end_idx = min((week + 1) * total_weekly_capacity, total_tasks)
        
        if start_idx < total_tasks:
            batch_df = df.iloc[start_idx:end_idx].copy()
            batches.append(batch_df)
    
    return batches

def distribute_tasks_by_capacity_with_serial_sequence(batch_df, teams_info):
    """Distribute batch data among teams based on capacity while maintaining serial number sequence"""
    print(f"Distributing {len(batch_df)} tasks among teams based on capacity...")
    
    # Group by repo_name to keep repositories together
    repo_groups = batch_df.groupby('repo_name')
    repo_list = []
    
    for repo_name, group in repo_groups:
        repo_list.append({
            'repo_name': repo_name,
            'tasks': group.sort_values('serial_no'),  # Keep serial order within repo
            'task_count': len(group)
        })
    
    # Sort repositories by their minimum serial number to maintain overall sequence
    repo_list.sort(key=lambda x: x['tasks']['serial_no'].min())
    
    # Initialize teams with their capacity info
    teams = []
    for team_info in teams_info:
        teams.append({
            'team_info': team_info,
            'tasks': pd.DataFrame(),
            'assigned_tasks': 0,
            'remaining_capacity': team_info['weekly_capacity'],
            'serial_range': {'min': None, 'max': None}
        })
    
    # Distribute repositories to teams based on capacity while maintaining sequence
    current_team_idx = 0
    
    for repo_info in repo_list:
        # Check if current team can handle this repo
        if teams[current_team_idx]['remaining_capacity'] >= repo_info['task_count']:
            # Assign to current team
            target_team = current_team_idx
        else:
            # Find next team with sufficient capacity
            found_team = False
            for i in range(current_team_idx + 1, len(teams)):
                if teams[i]['remaining_capacity'] >= repo_info['task_count']:
                    target_team = i
                    current_team_idx = i
                    found_team = True
                    break
            
            if not found_team:
                # If no team can handle the repo completely, assign to team with most remaining capacity
                target_team = max(range(len(teams)), key=lambda i: teams[i]['remaining_capacity'])
        
        # Assign repository to the selected team
        if teams[target_team]['tasks'].empty:
            teams[target_team]['tasks'] = repo_info['tasks'].copy()
            teams[target_team]['serial_range']['min'] = repo_info['tasks']['serial_no'].min()
        else:
            teams[target_team]['tasks'] = pd.concat([teams[target_team]['tasks'], repo_info['tasks']], ignore_index=True)
        
        teams[target_team]['serial_range']['max'] = repo_info['tasks']['serial_no'].max()
        teams[target_team]['assigned_tasks'] += repo_info['task_count']
        teams[target_team]['remaining_capacity'] -= repo_info['task_count']
    
    # Sort tasks within each team by serial number to maintain sequence
    for team in teams:
        if not team['tasks'].empty:
            team['tasks'] = team['tasks'].sort_values('serial_no').reset_index(drop=True)
    
    return teams

def create_folder_structure_and_save(batches, teams_info, base_output_dir="task_distribution"):
    """Create folder structure and save team files"""
    print(f"Creating folder structure in '{base_output_dir}'...")
    
    # Create base directory
    Path(base_output_dir).mkdir(exist_ok=True)
    
    distribution_report = {
        'total_tasks': sum(len(batch) for batch in batches),
        'total_weeks': len(batches),
        'teams': teams_info,
        'weekly_distributions': []
    }
    
    for week_num, batch_df in enumerate(batches, 1):
        week_folder = Path(base_output_dir) / f"week_{week_num}"
        week_folder.mkdir(exist_ok=True)
        
        print(f"\nProcessing Week {week_num} ({len(batch_df)} tasks)...")
        
        # Distribute batch among teams based on capacity while maintaining serial sequence
        teams = distribute_tasks_by_capacity_with_serial_sequence(batch_df, teams_info)
        
        week_distribution = {
            'week': week_num,
            'total_tasks': len(batch_df),
            'serial_range': {'min': batch_df['serial_no'].min(), 'max': batch_df['serial_no'].max()},
            'teams': []
        }
        
        # Save team files and collect statistics
        for team_data in teams:
            team_info = team_data['team_info']
            team_num = team_info['team_number']
            
            team_file = week_folder / f"team_{team_num}_{team_info['lead_name'].replace(' ', '_')}.csv"
            team_data['tasks'].to_csv(team_file, index=False)
            
            # Calculate work distribution per developer
            tasks_per_dev = team_data['assigned_tasks'] / team_info['num_developers'] if team_info['num_developers'] > 0 else 0
            days_needed = math.ceil(tasks_per_dev / 5) if tasks_per_dev > 0 else 0
            
            # Get serial number range for this team
            serial_range = team_data['serial_range']
            serial_range_str = f"{serial_range['min']}-{serial_range['max']}" if serial_range['min'] is not None else "No tasks"
            
            print(f"  Team {team_num} ({team_info['lead_name']}): {team_data['assigned_tasks']} tasks -> {team_file}")
            print(f"    Serial Range: {serial_range_str}")
            print(f"    Capacity: {team_info['weekly_capacity']}, Used: {team_data['assigned_tasks']}, Remaining: {team_data['remaining_capacity']}")
            print(f"    Tasks per developer: {tasks_per_dev:.1f}, Days needed: {days_needed}")
            
            # Repository distribution
            repo_counts = {}
            if not team_data['tasks'].empty:
                repo_counts = team_data['tasks']['repo_name'].value_counts()
                print(f"    Repositories: {len(repo_counts)} repos")
            
            # Add to week distribution report
            week_distribution['teams'].append({
                'team_number': team_num,
                'lead_name': team_info['lead_name'],
                'num_developers': team_info['num_developers'],
                'weekly_capacity': team_info['weekly_capacity'],
                'assigned_tasks': team_data['assigned_tasks'],
                'remaining_capacity': team_data['remaining_capacity'],
                'tasks_per_developer': round(tasks_per_dev, 1),
                'days_needed': days_needed,
                'repositories': len(repo_counts),
                'repo_distribution': dict(repo_counts),
                'serial_range': serial_range
            })
        
        distribution_report['weekly_distributions'].append(week_distribution)
    
    return distribution_report

def generate_distribution_report_md(distribution_report, base_output_dir="task_distribution"):
    """Generate a comprehensive distribution report in Markdown format"""
    print("\nGenerating distribution report in Markdown format...")
    
    report_file = Path(base_output_dir) / "distribution_report.md"
    
    with open(report_file, 'w') as f:
        f.write("# Task Distribution Report\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall Summary
        f.write("## Overall Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total Tasks | {distribution_report['total_tasks']} |\n")
        f.write(f"| Total Weeks | {distribution_report['total_weeks']} |\n")
        f.write(f"| Total Teams | {len(distribution_report['teams'])} |\n\n")
        
        # Team Information
        f.write("## Team Information\n\n")
        f.write("| Team | Lead Name | Developers | Weekly Capacity | Formula |\n")
        f.write("|------|-----------|------------|-----------------|----------|\n")
        
        total_capacity = 0
        for team in distribution_report['teams']:
            formula = f"{team['num_developers']} × 5 × 5"
            f.write(f"| {team['team_number']} | {team['lead_name']} | {team['num_developers']} | {team['weekly_capacity']} | {formula} |\n")
            total_capacity += team['weekly_capacity']
        
        f.write(f"\n**Total Weekly Capacity:** {total_capacity} tasks\n\n")
        
        # Weekly Distribution Details
        f.write("## Weekly Distribution Details\n\n")
        
        for week_dist in distribution_report['weekly_distributions']:
            f.write(f"### Week {week_dist['week']}\n\n")
            f.write(f"**Total Tasks:** {week_dist['total_tasks']} | ")
            f.write(f"**Serial Range:** {week_dist['serial_range']['min']}-{week_dist['serial_range']['max']}\n\n")
            
            f.write("| Team | Lead | Assigned Tasks | Capacity Usage | Tasks/Dev | Days Needed | Serial Range | Repositories |\n")
            f.write("|------|------|----------------|----------------|-----------|-------------|--------------|-------------|\n")
            
            for team in week_dist['teams']:
                capacity_usage = f"{(team['assigned_tasks']/team['weekly_capacity']*100):.1f}%" if team['weekly_capacity'] > 0 else "0%"
                serial_range = f"{team['serial_range']['min']}-{team['serial_range']['max']}" if team['serial_range']['min'] is not None else "None"
                
                f.write(f"| {team['team_number']} | {team['lead_name']} | {team['assigned_tasks']}/{team['weekly_capacity']} | {capacity_usage} | {team['tasks_per_developer']} | {team['days_needed']}/5 | {serial_range} | {team['repositories']} |\n")
            
            f.write("\n")
            
            # Repository Distribution for each team
            for team in week_dist['teams']:
                if team['repo_distribution']:
                    f.write(f"#### Team {team['team_number']} - {team['lead_name']} Repository Distribution\n\n")
                    f.write("| Repository | Tasks |\n")
                    f.write("|------------|-------|\n")
                    for repo, count in sorted(team['repo_distribution'].items()):
                        f.write(f"| {repo} | {count} |\n")
                    f.write("\n")
        
        # Capacity Analysis
        f.write("## Capacity Analysis\n\n")
        f.write("| Week | Tasks Assigned | Total Capacity | Utilization |\n")
        f.write("|------|----------------|----------------|-------------|\n")
        
        overall_assigned = 0
        overall_capacity = 0
        
        for week_num, week_dist in enumerate(distribution_report['weekly_distributions'], 1):
            total_assigned = sum(team['assigned_tasks'] for team in week_dist['teams'])
            total_capacity = sum(team['weekly_capacity'] for team in week_dist['teams'])
            utilization = f"{(total_assigned / total_capacity * 100):.1f}%" if total_capacity > 0 else "0%"
            
            f.write(f"| {week_num} | {total_assigned} | {total_capacity} | {utilization} |\n")
            
            overall_assigned += total_assigned
            overall_capacity += total_capacity
        
        overall_utilization = f"{(overall_assigned / overall_capacity * 100):.1f}%" if overall_capacity > 0 else "0%"
        f.write(f"| **Total** | **{overall_assigned}** | **{overall_capacity}** | **{overall_utilization}** |\n\n")
        
        # Project Statistics
        f.write("## Project Statistics\n\n")
        f.write("### Key Metrics\n\n")
        f.write(f"- **Serial Number Sequence:** Maintained across all teams and weeks\n")
        f.write(f"- **Repository Integrity:** Each repository assigned to single team\n")
        f.write(f"- **Workload Balance:** Distributed based on team capacity\n")
        f.write(f"- **Average Utilization:** {overall_utilization}\n")
        f.write(f"- **Estimated Completion:** {distribution_report['total_weeks']} weeks\n\n")
        
        f.write("### Distribution Strategy\n\n")
        f.write("1. **Capacity-Based:** Tasks distributed according to team size\n")
        f.write("2. **Repository Consolidation:** Same repo stays with same team\n")
        f.write("3. **Sequential Assignment:** Serial numbers maintained in order\n")
        f.write("4. **Balanced Workload:** ~5 tasks per developer per day\n")
        f.write("5. **5-Day Work Week:** Planning based on standard work schedule\n\n")
    
    print(f"Distribution report saved: {report_file}")
    return report_file

def main():
    print("=== JSONL Task Distribution Tool ===\n")
    
    # Get file path from command line arguments
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py input.jsonl")
        return
    
    jsonl_file = sys.argv[1]
    
    if not os.path.exists(jsonl_file):
        print(f"Error: File '{jsonl_file}' not found!")
        return
    
    print(f"Processing file: {jsonl_file}")
    
    try:
        num_teams = int(input("Enter number of teams: "))
    except ValueError:
        print("Error: Please enter a valid number!")
        return
    
    # Output file paths
    csv_file = jsonl_file.replace('.jsonl', '_complete.csv')
    
    try:
        # Step 1: Convert JSONL to CSV (Complete file)
        df = jsonl_to_csv(jsonl_file, csv_file)
        
        # Step 2: Sort by repo_name and add serial number column
        sorted_df = sort_by_repo_name_and_add_serial(df)
        
        # Save the sorted CSV with serial numbers
        sorted_csv_file = jsonl_file.replace('.jsonl', '_sorted_with_serial.csv')
        sorted_df.to_csv(sorted_csv_file, index=False)
        print(f"Sorted CSV with serial numbers saved: {sorted_csv_file}")
        
        # Step 3: Get team information
        teams_info = get_team_info(num_teams)
        
        # Step 4: Create capacity-based batches
        weekly_batches = create_capacity_based_batches(sorted_df, teams_info)
        
        # Step 5: Create folder structure and team distribution
        distribution_report = create_folder_structure_and_save(weekly_batches, teams_info)
        
        # Step 6: Generate comprehensive markdown report
        report_file = generate_distribution_report_md(distribution_report)
        
        print(f"\n=== Distribution Complete ===")
        print(f"Total tasks processed: {len(df)}")
        print(f"Weekly batches created: {len(weekly_batches)}")
        print(f"Teams configured: {num_teams}")
        print(f"Output directory: task_distribution/")
        print(f"Complete CSV file: {csv_file}")
        print(f"Sorted CSV with serials: {sorted_csv_file}")
        print(f"Distribution report: {report_file}")
        
        # Summary statistics
        total_capacity = sum(team['weekly_capacity'] for team in teams_info)
        print(f"\n=== Capacity Summary ===")
        print(f"Total weekly capacity: {total_capacity} tasks")
        print(f"Estimated completion time: {math.ceil(len(df) / total_capacity)} weeks")
        
        for week_num, batch in enumerate(weekly_batches, 1):
            serial_min = batch['serial_no'].min()
            serial_max = batch['serial_no'].max()
            print(f"Week {week_num}: {len(batch)} tasks (Serial: {serial_min}-{serial_max})")
    
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
