import pandas as pd

# Read the Excel file
file_path = "raw.xlsx"
df = pd.read_excel(file_path, sheet_name="表單回應 1")

# Extract all functional and dysfunctional question columns
functional_cols = [col for col in df.columns if col.startswith("1. ") and "[" in col]
dysfunctional_cols = [col for col in df.columns if col.startswith("2. ") and "[" in col]

# Extract feature names from column headers
def extract_feature_name(col):
    start = col.find('[')
    end = col.find(']')
    return col[start+1:end]

functional_keys = [extract_feature_name(col) for col in functional_cols]
dysfunctional_keys = [extract_feature_name(col) for col in dysfunctional_cols]

# Keep only features that appear in both functional and dysfunctional questions
features_match = set(functional_keys) & set(dysfunctional_keys)

# Kano classification lookup table
kano_mapping = {
    ("喜歡", "喜歡"): "Q",
    ("喜歡", "應該的"): "A",
    ("喜歡", "無所謂"): "A",
    ("喜歡", "能忍受"): "A",
    ("喜歡", "不喜歡"): "O",
    ("應該的", "喜歡"): "R",
    ("應該的", "應該的"): "I",
    ("應該的", "無所謂"): "I",
    ("應該的", "能忍受"): "I",
    ("應該的", "不喜歡"): "M",
    ("無所謂", "喜歡"): "R",
    ("無所謂", "應該的"): "I",
    ("無所謂", "無所謂"): "I",
    ("無所謂", "能忍受"): "I",
    ("無所謂", "不喜歡"): "M",
    ("能忍受", "喜歡"): "R",
    ("能忍受", "應該的"): "I",
    ("能忍受", "無所謂"): "I",
    ("能忍受", "能忍受"): "I",
    ("能忍受", "不喜歡"): "M",
    ("不喜歡", "喜歡"): "R",
    ("不喜歡", "應該的"): "R",
    ("不喜歡", "無所謂"): "R",
    ("不喜歡", "能忍受"): "R",
    ("不喜歡", "不喜歡"): "Q",
}

# Aggregate classification results
results = {}

for feature in features_match:
    func_col = next(col for col in functional_cols if feature in col)
    dysf_col = next(col for col in dysfunctional_cols if feature in col)
    
    func_answers = df[func_col]
    dysf_answers = df[dysf_col]
    
    kano_result = []
    for f, d in zip(func_answers, dysf_answers):
        label = kano_mapping.get((f.strip(), d.strip()), "Q")
        kano_result.append(label)

    result_series = pd.Series(kano_result).value_counts()
    results[feature] = result_series

# Convert to DataFrame and fill missing columns
result_df = pd.DataFrame(results).fillna(0).astype(int).T
result_df = result_df.reindex(columns=["A", "O", "M", "I", "R", "Q"], fill_value=0)

# Add Result column: the most frequent classification
result_df["Result"] = result_df[["A", "O", "M", "I", "R", "Q"]].idxmax(axis=1)

# Add SI (Satisfaction Increment) = (A + O) / (A + O + M + I)
denominator = result_df[["A", "O", "M", "I"]].sum(axis=1)
result_df["SI"] = (result_df["A"] + result_df["O"]) / denominator

# Add DSI (Dissatisfaction Increment) = (O + M) / (A + O + M + I) * -1
result_df["DSI"] = -1 * (result_df["O"] + result_df["M"]) / denominator

# Reorder features to match the original functional column order
ordered_features = [extract_feature_name(col) for col in functional_cols if extract_feature_name(col) in result_df.index]
result_df = result_df.loc[ordered_features]

# Print and export results
print(result_df)
result_df.to_excel("Kano_outcome.xlsx")
