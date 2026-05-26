"""
Batch Test Runner for FastBox Delivery System
==============================================
Runs all test cases and generates a summary report.
"""

import os
import sys
import json
import time

# Add the current directory to the path to import the simulator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main simulator functions
from delivery_simulator import load_data, assign_packages_to_agents, simulate_deliveries, generate_report

def run_single_test(test_file):
    """
    Run a single test case.
    
    Args:
        test_file: Path to the test case JSON file
    
    Returns:
        Dictionary with test results
    """
    try:
        # Load data
        data = load_data(test_file)
        
        # Assign packages
        agent_assignments = assign_packages_to_agents(data)
        
        # Simulate deliveries
        results = simulate_deliveries(data, agent_assignments)
        
        # Generate output filename
        base_name = os.path.basename(test_file)
        test_name = os.path.splitext(base_name)[0]
        output_file = f"reports/report_{test_name}.json"
        
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        # Generate report
        generate_report(results, output_file)
        
        # Get best agent from results
        best_agent = None
        best_efficiency = float('inf')
        for agent_id, stats in results.items():
            if stats['packages_delivered'] > 0:
                if stats['efficiency'] < best_efficiency:
                    best_efficiency = stats['efficiency']
                    best_agent = agent_id
        
        return {
            'test_case': base_name,
            'status': 'Success',
            'best_agent': best_agent if best_agent else 'N/A',
            'report_file': output_file
        }
    
    except Exception as e:
        return {
            'test_case': os.path.basename(test_file),
            'status': f'Error: {str(e)}',
            'best_agent': 'N/A',
            'report_file': 'N/A'
        }


def run_all_tests():
    """
    Run all test cases and generate a summary report.
    """
    print("="*80)
    print("🚀 Running All Test Cases - FastBox Delivery System")
    print("="*80)
    
    test_cases_dir = "test_cases"
    
    if not os.path.exists(test_cases_dir):
        print(f"✗ Error: Directory '{test_cases_dir}' not found!")
        return
    
    test_files = sorted([f for f in os.listdir(test_cases_dir) if f.endswith('.json')])
    
    if not test_files:
        print(f"✗ No test case files found in {test_cases_dir}/ directory!")
        return
    
    print(f"\nFound {len(test_files)} test cases")
    print("-"*80)
    
    results_summary = []
    start_time = time.time()
    
    for i, test_file in enumerate(test_files, 1):
        test_path = os.path.join(test_cases_dir, test_file)
        print(f"\n[{i}/{len(test_files)}] Running {test_file}...")
        
        result = run_single_test(test_path)
        results_summary.append(result)
        
        if result['status'] == 'Success':
            print(f"  ✓ {test_file} completed successfully - Best Agent: {result['best_agent']}")
        else:
            print(f"  ✗ {test_file} failed: {result['status']}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Print summary
    print("\n" + "="*80)
    print("📊 BATCH TEST SUMMARY")
    print("="*80)
    
    success_count = sum(1 for r in results_summary if r['status'] == 'Success')
    
    print(f"\nTotal Test Cases: {len(test_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(test_files) - success_count}")
    print(f"Execution Time: {elapsed_time:.2f} seconds")
    
    print("\nDetailed Results:")
    print("-"*80)
    for result in results_summary:
        status_icon = "✓" if result['status'] == 'Success' else "✗"
        print(f"{status_icon} {result['test_case']:<25} | Best Agent: {result['best_agent']:<5} | {result['status']}")
    
    # Save summary to JSON
    os.makedirs('reports', exist_ok=True)
    summary_path = "reports/batch_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_tests': len(test_files),
            'successful': success_count,
            'failed': len(test_files) - success_count,
            'execution_time': elapsed_time,
            'results': results_summary
        }, f, indent=2)
    
    print(f"\n✓ Summary saved to: {summary_path}")
    print("="*80)
    
    # Print all reports created
    if success_count > 0:
        print("\n📁 Generated Reports:")
        for result in results_summary:
            if result['status'] == 'Success':
                print(f"  - {result['report_file']}")


if __name__ == "__main__":
    run_all_tests()