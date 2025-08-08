   from google.cloud import bigquery
   import pandas as pd

   # Initialize a BigQuery client
   client = bigquery.Client()

   # Define your SQL query
   query = """
   SELECT 
       agent_id,
       team_id,
       performance_metric,
       incentive_metric,
       timestamp
   FROM 
       `your_project.your_dataset.your_table`
   WHERE 
       timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
   """

   # Execute the query and convert to DataFrame
   df = client.query(query).to_dataframe()

   # Perform any necessary data processing
   # For example, calculating averages or totals
   performance_summary = df.groupby(['agent_id', 'team_id']).agg({
       'performance_metric': 'mean',
       'incentive_metric': 'sum'
   }).reset_index()

   # Save the processed data back to BigQuery or a CSV file
   performance_summary.to_gbq('your_project.your_dataset.performance_summary', if_exists='replace')