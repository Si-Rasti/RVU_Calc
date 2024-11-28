import pandas as pd

file_path = 'Source.xlsx'  # Source: Original file from our institution
source_df = pd.read_excel(file_path)

# Split the 'CPT' column into multiple columns
split_columns = source_df['CPT'].str.split(', ', expand=True)

# Assign new column names for the split columns
split_columns.columns = [f'CPT_{i+1}' for i in range(split_columns.shape[1])]

# Combine the original dataframe with the new columns
source_df = pd.concat([source_df, split_columns], axis=1)
print("CPTs were split successfully")

reference_df = pd.read_excel('Reference.xlsx')  # Reference: The file published by CMS

source_columns = ["CPT_1", "CPT_2", "CPT_3"] # CPT_1 is applicable to all acquisitions;
# CPT_2 and _3 are newly generated columns for those with multiple acquisitions in a single session
reference_column = 'CPT'

# The columns from the Reference spreadsheet that need to be considered in our analysis
columns_to_append = ['multiple procedure', 'Technical Non-fac PE RVU', 'Technical Facility PE RVU', 'Technical MP RVU', 'Technical Non-fac Total', 'Technical Facility Total',
                  'Professional Work RVU', 'Professional Work RVU', 'Professional Facility PE RVU', 'Professional MP RVU', 'Professional MP RVU',
                  'Professional Facility Total', 'Total Work RVU', 'Total Non-fac PE RVU', 'Total Facility PE RVU', 'Total Facility PE RVU', 'Total Non-fac Total',
                  'Total Non-fac Total']


# Preparing new column names for appended data
appended_columns = [f'{col}{i + 1}' for i in range(3) for col in columns_to_append]

# A list to hold processed rows
processed_rows = []

# Iterate over each row in source_df
for _, source_row in source_df.iterrows():
    for col in source_columns:
        if pd.notna(source_row[col]):
            source_row[col] = str(int(source_row[col])) if isinstance(source_row[col], (int, float)) else str(source_row[col])
    # A dictionary to hold the updated row data
    updated_row = source_row.to_dict()

    # Appending data for each of CPT_1, CPT_2, CPT_3
    for idx, col in enumerate(source_columns):
        if pd.notna(source_row[col]) and source_row[col] in reference_df[reference_column].values:
            matching_row = reference_df[reference_df[reference_column] == source_row[col]].iloc[0]
            for append_col in columns_to_append:
                updated_row[f'{append_col}{idx + 1}'] = matching_row[append_col]

    # Appending the processed row to the list
    processed_rows.append(updated_row)

# Creating a new DataFrame with the processed rows
final_df = pd.DataFrame(processed_rows)

# Adding missing appended columns if no data was appended for some
for col in appended_columns:
    if col not in final_df.columns:
        final_df[col] = None

print("RVUs successfully appended")

# Initializing new columns
final_df["total technical"] = None
final_df["total professional"] = None

# Function to calculate maximum and non-maximum values
def calculate_totals(row):
    # Replacing NaN with 0 for the required columns
    mp1 = row["multiple procedure1"] if not pd.isna(row["multiple procedure1"]) else 0
    mp2 = row["multiple procedure2"] if not pd.isna(row["multiple procedure2"]) else 0
    mp3 = row["multiple procedure3"] if not pd.isna(row["multiple procedure3"]) else 0
    tf1 = row["Technical Facility Total1"] if not pd.isna(row["Technical Facility Total1"]) else 0
    tf2 = row["Technical Facility Total2"] if not pd.isna(row["Technical Facility Total2"]) else 0
    tf3 = row["Technical Facility Total3"] if not pd.isna(row["Technical Facility Total3"]) else 0
    pf1 = row["Professional Facility Total1"] if not pd.isna(row["Professional Facility Total1"]) else 0
    pf2 = row["Professional Facility Total2"] if not pd.isna(row["Professional Facility Total2"]) else 0
    pf3 = row["Professional Facility Total3"] if not pd.isna(row["Professional Facility Total3"]) else 0

    multiple_procedures = [mp1, mp2, mp3]
    technical_totals = [tf1, tf2, tf3]
    professional_totals = [pf1, pf2, pf3]

    # Filter out zeros (indicating missing values or invalid entries)
    valid_indices = [i for i, mp in enumerate(multiple_procedures) if mp == 4]
    valid_technical = [technical_totals[i] for i in valid_indices]
    valid_professional = [professional_totals[i] for i in valid_indices]

    if len(valid_indices) == 3:
        max_technical = max(valid_technical)
        max_professional = max(valid_professional)
        other_technical = sorted(valid_technical)[:2]
        other_professional = sorted(valid_professional)[:2]
        total_technical = max_technical + 0.5 * sum(other_technical)
        total_professional = max_professional + 0.95 * sum(other_professional)
    elif len(valid_indices) == 2:
        max_technical = max(valid_technical)
        max_professional = max(valid_professional)
        other_technical = min(valid_technical)
        other_professional = min(valid_professional)
        total_technical = max_technical + 0.5 * other_technical
        total_professional = max_professional + 0.95 * other_professional
        non_matching_technical = sum(technical_totals) - sum(valid_technical)
        non_matching_professional = sum(professional_totals) - sum(valid_professional)
        total_technical += non_matching_technical
        total_professional += non_matching_professional
    elif len(valid_indices) == 1:
        total_technical = sum(technical_totals)
        total_professional = sum(professional_totals)
    else:
        total_technical = sum(technical_totals)
        total_professional = sum(professional_totals)

    return total_technical, total_professional

# Applying the logic to each row
final_df[["total technical", "total professional"]] = final_df.apply(
    lambda row: pd.Series(calculate_totals(row)), axis=1
)

# Save the updated df to a new Excel file
output_file = 'Final_discount.xlsx'
final_df.to_excel(output_file, index=False)

print("Discounts successfully implemented and saved to:", output_file)

