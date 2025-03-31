#!/usr/bin/env python3
"""
Process and analyze contact information from the NLP Healthcare Summit 2025.
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

def extract_contact_data(org_file):
    """
    Extract contact data from an org file.
    
    Args:
        org_file (Path): Path to the org file containing contact data
        
    Returns:
        list: List of dictionaries containing contact data
    """
    contacts = []
    
    if not org_file.exists():
        print(f"File not found: {org_file}")
        return contacts
    
    content = org_file.read_text()
    
    # Simple regex-based extraction for demonstration
    # In a real implementation, proper org-mode parsing would be better
    contact_blocks = re.findall(r'\*\*\* Contact Information(.*?)(?=\*\*\* |$)', 
                               content, re.DOTALL)
    
    for block in contact_blocks:
        contact = {}
        
        # Extract basic information
        name_match = re.search(r'- Name: (.*?)$', block, re.MULTILINE)
        if name_match:
            contact['name'] = name_match.group(1).strip()
            
        org_match = re.search(r'- Organization: (.*?)$', block, re.MULTILINE)
        if org_match:
            contact['organization'] = org_match.group(1).strip()
            
        role_match = re.search(r'- Role: (.*?)$', block, re.MULTILINE)
        if role_match:
            contact['role'] = role_match.group(1).strip()
        
        # Skip empty templates
        if contact and contact.get('name'):
            contacts.append(contact)
    
    return contacts

def generate_contact_network(contacts, output_file=None):
    """
    Generate a network visualization of contacts and their organizations.
    
    Args:
        contacts (list): List of dictionaries containing contact data
        output_file (Path, optional): Path to save the output network visualization
        
    Returns:
        nx.Graph: The contact network
    """
    G = nx.Graph()
    
    # Add person nodes
    for contact in contacts:
        if 'name' in contact:
            G.add_node(contact['name'], type='person')
    
    # Add organization nodes and connect people to their organizations
    for contact in contacts:
        if 'name' in contact and 'organization' in contact and contact['organization']:
            org = contact['organization']
            # Add org node if it doesn't exist
            if org not in G:
                G.add_node(org, type='organization')
            # Connect person to organization
            G.add_edge(contact['name'], org)
    
    # Visualize
    if G.nodes and output_file:
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # Draw organization nodes
        org_nodes = [node for node, attrs in G.nodes(data=True) 
                    if attrs.get('type') == 'organization']
        nx.draw_networkx_nodes(G, pos, nodelist=org_nodes, 
                              node_color='lightgreen', node_size=2000, alpha=0.8)
        
        # Draw person nodes
        person_nodes = [node for node, attrs in G.nodes(data=True) 
                       if attrs.get('type') == 'person']
        nx.draw_networkx_nodes(G, pos, nodelist=person_nodes, 
                              node_color='skyblue', node_size=1000, alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.savefig(output_file)
        plt.close()
    
    return G

def main():
    """Main function to process contacts."""
    parser = argparse.ArgumentParser(description='Process NLP Summit contacts')
    parser.add_argument('--output', '-o', type=str, 
                        default='contacts_analysis', 
                        help='Output prefix for generated files')
    args = parser.parse_args()
    
    # Find the repository root
    repo_path = Path(__file__).resolve().parent.parent.parent
    contacts_dir = repo_path / 'contacts'
    
    # Output directory
    output_dir = repo_path / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    # Process all contact org files
    contacts = []
    for org_file in contacts_dir.glob('*.org'):
        contacts.extend(extract_contact_data(org_file))
    
    if not contacts:
        print("No contacts found or all are template placeholders")
        return
    
    # Generate outputs
    print(f"Found {len(contacts)} contacts")
    
    # Export to CSV
    df = pd.DataFrame(contacts)
    csv_path = output_dir / f"{args.output}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Exported contact data to {csv_path}")
    
    # Export to JSON
    json_path = output_dir / f"{args.output}.json"
    with open(json_path, 'w') as f:
        json.dump(contacts, f, indent=2)
    print(f"Exported contact data to {json_path}")
    
    # Generate network
    network_path = output_dir / f"{args.output}_network.png"
    generate_contact_network(contacts, network_path)
    print(f"Generated contact network at {network_path}")

if __name__ == "__main__":
    main()
