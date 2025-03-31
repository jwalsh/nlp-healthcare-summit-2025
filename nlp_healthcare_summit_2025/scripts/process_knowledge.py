#!/usr/bin/env python3
"""
Process and analyze knowledge base information from the NLP Healthcare Summit 2025.
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
from collections import Counter

def extract_topic_data(org_file):
    """
    Extract topic data from an org file.
    
    Args:
        org_file (Path): Path to the org file containing topic data
        
    Returns:
        list: List of dictionaries containing topic data
    """
    topics = []
    
    if not org_file.exists():
        print(f"File not found: {org_file}")
        return topics
    
    content = org_file.read_text()
    
    # Simple regex-based extraction for demonstration
    # In a real implementation, proper org-mode parsing would be better
    topic_blocks = re.findall(r'\*\*\* Topic Information(.*?)(?=\*\*\* |$)', 
                             content, re.DOTALL)
    
    for block in topic_blocks:
        topic = {}
        
        # Extract basic information
        name_match = re.search(r'- Name: (.*?)$', block, re.MULTILINE)
        if name_match:
            topic['name'] = name_match.group(1).strip()
            
        category_match = re.search(r'- Category: (.*?)$', block, re.MULTILINE)
        if category_match:
            topic['category'] = category_match.group(1).strip()
            
        related_sessions_match = re.search(r'- Related Sessions: (.*?)$', block, re.MULTILINE)
        if related_sessions_match:
            sessions_text = related_sessions_match.group(1).strip()
            if sessions_text:
                topic['related_sessions'] = [s.strip() for s in sessions_text.split(',')]
            
        related_contacts_match = re.search(r'- Key Contacts: (.*?)$', block, re.MULTILINE)
        if related_contacts_match:
            contacts_text = related_contacts_match.group(1).strip()
            if contacts_text:
                topic['key_contacts'] = [c.strip() for c in contacts_text.split(',')]
        
        # Skip empty templates
        if topic and topic.get('name'):
            topics.append(topic)
    
    return topics

def generate_knowledge_graph(topics, output_file=None):
    """
    Generate a knowledge graph visualization of topics and their relationships.
    
    Args:
        topics (list): List of dictionaries containing topic data
        output_file (Path, optional): Path to save the output graph
        
    Returns:
        nx.Graph: The knowledge graph
    """
    G = nx.Graph()
    
    # Add nodes for each topic
    for topic in topics:
        if 'name' in topic:
            category = topic.get('category', 'Unknown')
            G.add_node(topic['name'], category=category)
    
    # Add edges for topics that share related sessions or contacts
    for i, topic1 in enumerate(topics):
        for j, topic2 in enumerate(topics):
            if i < j:  # Avoid duplicate edges
                if 'name' not in topic1 or 'name' not in topic2:
                    continue
                    
                # Check for shared sessions
                shared_sessions = False
                if 'related_sessions' in topic1 and 'related_sessions' in topic2:
                    for session in topic1['related_sessions']:
                        if session in topic2['related_sessions']:
                            shared_sessions = True
                            break
                
                # Check for shared contacts
                shared_contacts = False
                if 'key_contacts' in topic1 and 'key_contacts' in topic2:
                    for contact in topic1['key_contacts']:
                        if contact in topic2['key_contacts']:
                            shared_contacts = True
                            break
                
                # Add edge if there's any connection
                if shared_sessions or shared_contacts:
                    G.add_edge(topic1['name'], topic2['name'])
    
    # Visualize
    if G.nodes and output_file:
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # Define colors for different categories
        category_colors = {
            'NLP': 'skyblue',
            'Healthcare': 'lightgreen',
            'Research': 'salmon',
            'Technology': 'purple',
            'Unknown': 'gray'
        }
        
        # Group nodes by category
        category_nodes = {}
        for category in category_colors:
            category_nodes[category] = [
                node for node, attrs in G.nodes(data=True) 
                if attrs.get('category', 'Unknown').startswith(category)
            ]
        
        # Draw nodes by category
        for category, nodes in category_nodes.items():
            if nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                                      node_color=category_colors.get(category, 'gray'), 
                                      node_size=1000, alpha=0.8,
                                      label=category)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.legend()
        plt.savefig(output_file)
        plt.close()
    
    return G

def main():
    """Main function to process knowledge base topics."""
    parser = argparse.ArgumentParser(description='Process NLP Summit knowledge base')
    parser.add_argument('--output', '-o', type=str, 
                        default='knowledge_analysis', 
                        help='Output prefix for generated files')
    args = parser.parse_args()
    
    # Find the repository root
    repo_path = Path(__file__).resolve().parent.parent.parent
    kb_dir = repo_path / 'kb'
    
    # Output directory
    output_dir = repo_path / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    # Process all knowledge base org files
    topics = []
    for org_file in kb_dir.glob('*.org'):
        topics.extend(extract_topic_data(org_file))
    
    if not topics:
        print("No topics found or all are template placeholders")
        return
    
    # Generate outputs
    print(f"Found {len(topics)} topics")
    
    # Export to CSV
    df = pd.DataFrame(topics)
    csv_path = output_dir / f"{args.output}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Exported topic data to {csv_path}")
    
    # Export to JSON
    json_path = output_dir / f"{args.output}.json"
    with open(json_path, 'w') as f:
        json.dump(topics, f, indent=2)
    print(f"Exported topic data to {json_path}")
    
    # Generate knowledge graph
    graph_path = output_dir / f"{args.output}_graph.png"
    generate_knowledge_graph(topics, graph_path)
    print(f"Generated knowledge graph at {graph_path}")
    
    # Generate category distribution
    categories = [topic.get('category', 'Unknown') for topic in topics]
    category_counts = Counter(categories)
    
    plt.figure(figsize=(10, 6))
    plt.bar(category_counts.keys(), category_counts.values())
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Distribution of Topic Categories')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    category_path = output_dir / f"{args.output}_categories.png"
    plt.savefig(category_path)
    plt.close()
    print(f"Generated category distribution at {category_path}")

if __name__ == "__main__":
    main()
