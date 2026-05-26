"""
FastBox Delivery System Simulator
==================================
A logistics simulator that assigns packages to delivery agents and 
calculates optimal delivery routes.

Author: [Your Name]
Date: May 2026
"""

import json
import math
import sys
import os
from typing import Dict, List, Tuple, Any



def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Formula: distance = √((x2-x1)² + (y2-y1)²)
    
    Args:
        point1: Tuple of (x, y) coordinates
        point2: Tuple of (x, y) coordinates
    
    Returns:
        Float representing the Euclidean distance
    
    Example:
        >>> calculate_distance((0, 0), (3, 4))
        5.0
    """
    x1, y1 = point1
    x2, y2 = point2
    
    # Apply Euclidean distance formula
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distance




def load_data(filepath: str) -> Dict[str, Any]:
    """
    Load and parse JSON data from file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        Dictionary containing warehouses, agents, and packages data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        print(f"✓ Successfully loaded data from {filepath}")
        print(f"  - Warehouses: {len(data['warehouses'])}")
        print(f"  - Agents: {len(data['agents'])}")
        print(f"  - Packages: {len(data['packages'])}")
        
        return data
    
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found!")
        sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON format - {e}")
        sys.exit(1)


def assign_packages_to_agents(data: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Assign each package to the nearest agent based on distance from agent to warehouse.
    
    Logic:
    - For each package, find which warehouse it's stored at
    - Calculate distance from each agent to that warehouse
    - Assign package to the agent with minimum distance
    
    Args:
        data: Dictionary containing warehouses, agents, and packages
    
    Returns:
        Dictionary mapping agent IDs to their assigned packages
        Example: {'A1': [package1, package2], 'A2': [package3]}
    """
    warehouses = data['warehouses']
    agents = data['agents']
    packages = data['packages']
    
    # Initialize assignment dictionary for each agent
    agent_assignments = {agent_id: [] for agent_id in agents.keys()}
    
    print("\n📦 Assigning packages to agents...")
    
    # Process each package
    for package in packages:
        package_id = package['id']
        warehouse_id = package['warehouse']
        warehouse_location = warehouses[warehouse_id]
        
        # Find nearest agent to this warehouse
        min_distance = float('inf')
        nearest_agent = None
        
        for agent_id, agent_location in agents.items():
            distance = calculate_distance(agent_location, warehouse_location)
            
            if distance < min_distance:
                min_distance = distance
                nearest_agent = agent_id
        
        # Assign package to nearest agent
        agent_assignments[nearest_agent].append(package)
        
        print(f"  {package_id} at {warehouse_id} → Agent {nearest_agent} (distance: {min_distance:.2f})")
    
    return agent_assignments



def simulate_deliveries(data: Dict[str, Any], agent_assignments: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """
    Simulate delivery process and calculate distances for each agent.
    
    Process for each agent:
    1. Start at agent's initial position
    2. For each assigned package:
       - Travel from current position to warehouse
       - Travel from warehouse to destination
       - Update current position to destination
    3. Calculate total distance and efficiency
    
    Args:
        data: Dictionary containing warehouses, agents, and packages
        agent_assignments: Dictionary mapping agents to their packages
    
    Returns:
        Dictionary with delivery statistics for each agent
    """
    warehouses = data['warehouses']
    agents = data['agents']
    
    results = {}
    
    print("\n🚚 Simulating deliveries...")
    
    for agent_id, assigned_packages in agent_assignments.items():
        # Start at agent's initial position
        current_position = agents[agent_id]
        total_distance = 0.0
        packages_delivered = len(assigned_packages)
        
        print(f"\n  Agent {agent_id} starting at {current_position}")
        
        # Deliver each package
        for package in assigned_packages:
            warehouse_id = package['warehouse']
            warehouse_location = warehouses[warehouse_id]
            destination = package['destination']
            
            # Distance from current position to warehouse
            distance_to_warehouse = calculate_distance(current_position, warehouse_location)
            
            # Distance from warehouse to destination
            distance_to_destination = calculate_distance(warehouse_location, destination)
            
            # Total distance for this delivery
            delivery_distance = distance_to_warehouse + distance_to_destination
            total_distance += delivery_distance
            
            print(f"    {package['id']}: {current_position} → {warehouse_id}{warehouse_location} → {destination} = {delivery_distance:.2f}")
            
            # Update agent's current position to the destination
            current_position = destination
        
        # Calculate efficiency (average distance per package)
        efficiency = total_distance / packages_delivered if packages_delivered > 0 else 0
        
        # Store results for this agent
        results[agent_id] = {
            'packages_delivered': packages_delivered,
            'total_distance': round(total_distance, 2),
            'efficiency': round(efficiency, 2)
        }
        
        print(f"  Agent {agent_id} total: {total_distance:.2f} units, efficiency: {efficiency:.2f}")
    
    return results



def find_best_agent(results: Dict[str, Dict]) -> str:
    """
    Find the most efficient agent (lowest efficiency score).
    
    Efficiency = Total Distance / Packages Delivered
    Lower efficiency = Better performance
    
    Args:
        results: Dictionary with delivery statistics for each agent
    
    Returns:
        Agent ID of the best performing agent
    """
    best_agent = None
    best_efficiency = float('inf')
    
    for agent_id, stats in results.items():
        # Only consider agents who delivered packages
        if stats['packages_delivered'] > 0:
            if stats['efficiency'] < best_efficiency:
                best_efficiency = stats['efficiency']
                best_agent = agent_id
    
    return best_agent



def generate_report(results: Dict[str, Dict], output_path: str) -> None:
    """
    Generate and save the delivery report as JSON.
    
    Args:
        results: Dictionary with delivery statistics for each agent
        output_path: Path where the report JSON will be saved
    """
    # Find the best agent
    best_agent = find_best_agent(results)
    
    # Create report structure
    report = results.copy()
    report['best_agent'] = best_agent
    
    # Save to JSON file
    with open(output_path, 'w') as file:
        json.dump(report, file, indent=2)
    
    print(f"\n✓ Report saved to: {output_path}")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 DELIVERY SUMMARY")
    print("="*50)
    
    for agent_id, stats in results.items():
        print(f"\n{agent_id}:")
        print(f"  Packages Delivered: {stats['packages_delivered']}")
        print(f"  Total Distance: {stats['total_distance']:.2f} units")
        print(f"  Efficiency: {stats['efficiency']:.2f} units/package")
    
    print(f"\n🏆 Best Agent: {best_agent}")
    print("="*50)



def visualize_routes_ascii(data: Dict[str, Any], agent_assignments: Dict[str, List[Dict]], results: Dict[str, Dict]) -> str:
    """
    Create an ASCII visualization of the delivery routes.
    
    Args:
        data: Dictionary containing warehouses, agents, and packages
        agent_assignments: Dictionary mapping agents to their packages
        results: Delivery statistics for each agent
    
    Returns:
        String containing the ASCII visualization
    """
    # Find grid boundaries
    all_points = []
    
    # Add warehouse positions
    for location in data['warehouses'].values():
        all_points.append(location)
    
    # Add agent positions
    for location in data['agents'].values():
        all_points.append(location)
    
    # Add package destinations
    for package in data['packages']:
        all_points.append(package['destination'])
    
    # Calculate grid size
    max_x = max(point[0] for point in all_points) + 5
    max_y = max(point[1] for point in all_points) + 5
    
    # Scale down for ASCII (fit in ~80 columns and ~30 rows)
    scale_x = 70 / max_x if max_x > 70 else 1
    scale_y = 25 / max_y if max_y > 25 else 1
    scale = min(scale_x, scale_y)
    
    # Create grid
    grid_width = int(max_x * scale) + 5
    grid_height = int(max_y * scale) + 5
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
    
    # Plot warehouses
    for warehouse_id, location in data['warehouses'].items():
        x = int(location[0] * scale)
        y = int(location[1] * scale)
        if 0 <= y < grid_height and 0 <= x < grid_width:
            grid[y][x] = 'W'
    
    # Plot agents
    for agent_id, location in data['agents'].items():
        x = int(location[0] * scale)
        y = int(location[1] * scale)
        if 0 <= y < grid_height and 0 <= x < grid_width:
            grid[y][x] = 'A'
    
    # Plot destinations
    for package in data['packages']:
        destination = package['destination']
        x = int(destination[0] * scale)
        y = int(destination[1] * scale)
        if 0 <= y < grid_height and 0 <= x < grid_width:
            grid[y][x] = 'D'
    
    # Convert grid to string
    visualization = "\n" + "="*80 + "\n"
    visualization += "🗺️  DELIVERY ROUTE VISUALIZATION\n"
    visualization += "="*80 + "\n"
    visualization += "Legend: W=Warehouse, A=Agent, D=Destination, .=Empty space\n"
    visualization += "-"*80 + "\n"
    
    for row in reversed(grid):  # Reverse to show correct orientation
        visualization += ''.join(row) + '\n'
    
    visualization += "-"*80 + "\n"
    
    return visualization

def export_to_csv(results: Dict[str, Dict], output_path: str) -> None:
    """
    Export agent performance data to CSV format.
    
    Args:
        results: Dictionary with delivery statistics for each agent
        output_path: Path where the CSV will be saved
    """
    import csv
    
    # Prepare CSV data
    csv_data = []
    for agent_id, stats in results.items():
        csv_data.append({
            'Agent ID': agent_id,
            'Packages Delivered': stats['packages_delivered'],
            'Total Distance': stats['total_distance'],
            'Efficiency': stats['efficiency']
        })
    
    # Sort by efficiency (best to worst)
    csv_data.sort(key=lambda x: x['Efficiency'] if x['Packages Delivered'] > 0 else float('inf'))
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Agent ID', 'Packages Delivered', 'Total Distance', 'Efficiency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✓ CSV export saved to: {output_path}")

def main():
    """
    Main function to run the FastBox delivery simulation with bonus features.
    
    Usage:
        python delivery_simulator.py <input_json_file> [options]
    
    Options:
        --visualize     Generate ASCII route visualization
        --export-csv    Export results to CSV format
        --no-display    Suppress terminal output (quiet mode)
    
    Example:
        python delivery_simulator.py test_cases/test_case_1.json --visualize --export-csv
    """
    print("="*80)
    print("🚀 FastBox Delivery System Simulator")
    print("="*80)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n✗ Error: No input file provided!")
        print("\nUsage: python delivery_simulator.py <input_json_file> [options]")
        print("\nOptions:")
        print("  --visualize     Generate ASCII route visualization")
        print("  --export-csv    Export results to CSV format")
        print("  --no-display    Suppress detailed output")
        print("\nExample: python delivery_simulator.py test_cases/test_case_1.json --visualize")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Parse options
    visualize = '--visualize' in sys.argv
    export_csv_flag = '--export-csv' in sys.argv
    quiet_mode = '--no-display' in sys.argv
    
    # Load data from JSON file
    data = load_data(input_file)
    
    # Assign packages to agents
    agent_assignments = assign_packages_to_agents(data)
    
    # Simulate deliveries
    results = simulate_deliveries(data, agent_assignments)
    
    # Generate output filenames
    base_name = os.path.basename(input_file)
    test_name = os.path.splitext(base_name)[0]
    
    # Create output directories if they don't exist
    os.makedirs('reports', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Generate JSON report
    output_file = f"reports/report_{test_name}.json"
    generate_report(results, output_file)
    
    # Bonus Feature 1: ASCII Visualization
    if visualize:
        print("\n" + "="*80)
        print("🎨 Generating ASCII Visualization...")
        print("="*80)
        visualization = visualize_routes_ascii(data, agent_assignments, results)
        
        # Display visualization
        if not quiet_mode:
            print(visualization)
        
        # Save visualization to file
        viz_output = f"outputs/visualization_{test_name}.txt"
        with open(viz_output, 'w', encoding='utf-8') as f:
            f.write(visualization)
        print(f"✓ Visualization saved to: {viz_output}")
    
    # Bonus Feature 2: CSV Export
    if export_csv_flag:
        print("\n" + "="*80)
        print("📊 Exporting to CSV...")
        print("="*80)
        csv_output = f"outputs/performance_{test_name}.csv"
        export_to_csv(results, csv_output)
    
    # Performance Summary
    print("\n" + "="*80)
    print("📈 PERFORMANCE METRICS")
    print("="*80)
    
    total_packages = sum(stats['packages_delivered'] for stats in results.values())
    total_distance = sum(stats['total_distance'] for stats in results.values())
    active_agents = sum(1 for stats in results.values() if stats['packages_delivered'] > 0)
    
    print(f"\nSystem Overview:")
    print(f"  Total Packages Delivered: {total_packages}")
    print(f"  Total Distance Traveled: {total_distance:.2f} units")
    print(f"  Active Agents: {active_agents}/{len(results)}")
    print(f"  Average Distance per Package: {total_distance/total_packages:.2f} units" if total_packages > 0 else "  N/A")
    
    print("\n✅ Simulation completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()