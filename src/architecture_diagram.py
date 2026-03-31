import graphviz

# Create a Directed Graph with professional styling
dot = graphviz.Digraph('Architecture', comment='Data Pipeline Flow')
dot.attr(rankdir='LR', size='10,6', ratio='fill') # Left-to-Right layout

# Global styles for nodes and edges
dot.attr('node', shape='box', style='filled', fontname='Helvetica', fontsize='12')
dot.attr('edge', fontname='Helvetica', fontsize='10', color='#555555')

# --- 1. DATA SOURCES (External APIs) ---
with dot.subgraph(name='cluster_sources') as c:
    c.attr(label='1. External Data Sources (APIs)', style='filled', color='#E1F5FE', fontname='Helvetica-Bold')
    c.node('hubspot', 'HubSpot CRM\n(Deals, Contacts)', fillcolor='#FF7043', fontcolor='white')
    c.node('ga4', 'Google Analytics 4\n(Marketing Events)', fillcolor='#FFCA28')
    c.node('mailster', 'Mailster (WP)\n(Email Campaigns)', fillcolor='#81D4FA')
    c.node('postgres', 'PostgreSQL\n(Operational Data)', fillcolor='#90CAF9')

# --- 2. INGESTION & ETL (Python) ---
with dot.subgraph(name='cluster_etl') as c:
    c.attr(label='2. Automated ETL (Python)', style='filled', color='#F1F8E9', fontname='Helvetica-Bold')
    c.node('orchestrator', 'ETL Orchestrator\n(data_pipeline_main.py)', shape='diamond', fillcolor='#8BC34A', style='filled,bold')
    c.node('connector_hs', 'hubspot_ingestion.py', fillcolor='#AED581')
    c.node('connector_ga', 'ga4_extractor.py', fillcolor='#AED581')
    c.node('connector_ml', 'mailster_connector.py', fillcolor='#AED581')

# --- 3. AUTOMATION & LOGGING ---
dot.node('cron', 'Cron Job\n(2:00 AM)', shape='septagon', fillcolor='#CE93D8', style='filled')
dot.node('logs', 'Execution Logs', shape='note', fillcolor='#E0E0E0')

# --- 4. STORAGE & MODELING ---
with dot.subgraph(name='cluster_storage') as c:
    c.attr(label='3. Storage & SQL Modeling', style='filled', color='#FFF3E0', fontname='Helvetica-Bold')
    c.node('data_lake', 'Data Storage\n(.csv / Database)', shape='cylinder', fillcolor='#FFCC80')
    c.node('sql_logic', 'marketing_attribution.sql\n(ROI Analysis)', fillcolor='#FFE082')

# --- 5. VISUALIZATION (BI) ---
dot.node('powerbi', 'Power BI / Looker\nDashboards', shape='parallelogram', fillcolor='#66BB6A', style='filled,bold', fontcolor='white')

# --- DEFINING THE FLOW (Edges) ---

# Automation trigger
dot.edge('cron', 'orchestrator', 'Triggers')

# Ingestion Flow
dot.edge('orchestrator', 'connector_hs', 'Calls')
dot.edge('orchestrator', 'connector_ga', 'Calls')
dot.edge('orchestrator', 'connector_ml', 'Calls')

dot.edge('hubspot', 'connector_hs', 'REST API')
dot.edge('ga4', 'connector_ga', 'Reporting API')
dot.edge('mailster', 'connector_ml', 'REST API')
dot.edge('postgres', 'orchestrator', 'SQL Query')

# Flattening and Saving
dot.edge('connector_hs', 'data_lake', 'Flattened JSON')
dot.edge('connector_ga', 'data_lake', 'Reports')
dot.edge('connector_ml', 'data_lake', 'Campaign Data')
dot.edge('orchestrator', 'logs', 'Writes Status')

# Modeling & BI
dot.edge('data_lake', 'sql_logic', 'Joins Data')
dot.edge('sql_logic', 'powerbi', 'Semantic Layer')
dot.edge('data_lake', 'powerbi', 'Direct Data')

# Save and render the diagram
print("Generating Architecture Diagram...")
dot.render('architecture_map', format='png', cleanup=True)
print("✅ Done! 'architecture_map.png' has been saved.")
