#!/usr/bin/env python3
"""
Process and analyze session information from the NLP Healthcare Summit 2025.
"""
import argparse
import os
import sys
from pathlib import Path
import re
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def extract_session_data(org_file):
    """
    Extract session data from an org file.
    
    Args:
        org_file (Path): Path to the org file containing session data
        
    Returns:
        list: List of dictionaries containing session data
    """
    sessions = []
    
    if not org_file.exists():
        print(f"File not found: {org_file}")
        return sessions
    
    content = org_file.read_text()
    
    # Simple regex-based extraction for demonstration
    # In a real implementation, proper org-mode parsing would be better
    session_blocks = re.findall(r'\*\*\* Session Information(.*?)(?=\*\*\* |$)', 
                               content, re.DOTALL)
    
    for block in session_blocks:
        session = {}
        
        # Extract basic information
        title_match = re.search(r'- Title: (.*?)$', block, re.MULTILINE)
        if title_match:
            session['title'] = title_match.group(1).strip()
            
        track_match = re.search(r'- Track: (.*?)$', block, re.MULTILINE)
        if track_match:
            session['track'] = track_match.group(1).strip()
            
        date_match = re.search(r'- Date: (.*?)$', block, re.MULTILINE)
        if date_match:
            session['date'] = date_match.group(1).strip()
        
        # Skip empty templates
        if session and session.get('title'):
            sessions.append(session)
    
    return sessions

def generate_session_graph(sessions, output_file=None):
    """
    Generate a graph visualization of sessions and their relationships.
    
    Args:
        sessions (list): List of dictionaries containing session data
        output_file (Path, optional): Path to save the output graph
        
    Returns:
        nx.Graph: The session graph
    """
    G = nx.Graph()
    
    # Add nodes for each session
    for session in sessions:
        if 'title' in session:
            G.add_node(session['title'])
    
    # Add edges based on track (sessions in the same track are connected)
    for i, session1 in enumerate(sessions):
        for j, session2 in enumerate(sessions):
            if i < j:  # Avoid duplicate edges
                if (session1.get('track') == session2.get('track') and 
                    session1.get('track') and 
                    'title' in session1 and 
                    'title' in session2):
                    G.add_edge(session1['title'], session2['title'])
    
    # Visualize
    if G.nodes and output_file:
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', 
                node_size=1500, edge_color='gray', font_size=8)
        plt.savefig(output_file)
        plt.close()
    
    return G

def main():
    """Main function to process sessions."""
    parser = argparse.ArgumentParser(description='Process NLP Summit sessions')
    parser.add_argument('--output', '-o', type=str, 
                        default='sessions_analysis', 
                        help='Output prefix for generated files')
    args = parser.parse_args()
    
    # Find the repository root
    repo_path = Path(__file__).resolve().parent.parent.parent
    sessions_dir = repo_path / 'sessions'
    
    # Output directory
    output_dir = repo_path / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    # Process all session org files
    sessions = []
    for org_file in sessions_dir.glob('*.org'):
        sessions.extend(extract_session_data(org_file))
    
    if not sessions:
        print("No sessions found or all are template placeholders")
        return
    
    # Generate outputs
    print(f"Found {len(sessions)} sessions")
    
    # Export to CSV
    df = pd.DataFrame(sessions)
    csv_path = output_dir / f"{args.output}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Exported session data to {csv_path}")
    
    # Export to JSON
    json_path = output_dir / f"{args.output}.json"
    with open(json_path, 'w') as f:
        json.dump(sessions, f, indent=2)
    print(f"Exported session data to {json_path}")
    
    # Generate graph
    graph_path = output_dir / f"{args.output}_graph.png"
    generate_session_graph(sessions, graph_path)
    print(f"Generated session graph at {graph_path}")

if __name__ == "__main__":
    main()
