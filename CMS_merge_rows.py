import pandas as pd


df = pd.read_excel('CMS.xlsx')

# Create an empty DataFrame to store the merged data
merged_data = {}

# Group rows by the 'CPT' column
for cpt_value, group in df.groupby('CPT'):
    # Flatten all row values for the group into a single list
    flattened_values = group.drop(columns=['CPT']).values.flatten()
    # Remove NaN values (if any) and store in the merged_data dictionary
    merged_data[cpt_value] = [x for x in flattened_values if pd.notna(x)]

# Convert the merged data dictionary back to a DataFrame
result_df = pd.DataFrame.from_dict(merged_data, orient='index')

# Reset the index to make 'CPT' a column again
result_df.reset_index(inplace=True)
result_df.rename(columns={'index': 'CPT'}, inplace=True)

# Save the result back to an Excel file
output_file_path = 'Reference.xlsx'
result_df.to_excel(output_file_path, index=False)

print(f"Data has been successfully merged and saved to {output_file_path}.")
