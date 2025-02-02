import gzip

def get_drugs():
    drug_names = set()  # Use a set to store unique drug names
    with gzip.open('arcos_all_washpost.tsv.gz', 'rt') as f:
        header = f.readline()  # Read the header row
        drug_column_index = header.strip().split('\t').index('DRUG_NAME')  # Find the index of the DRUG_NAME column
        for line in f:
            drug_names.add(line.strip().split('\t')[drug_column_index])  # Add drug names to the set
    return drug_names

def write_drugs(drug_names):
    with open('drug_names.txt', 'w') as f:
        for drug in sorted(drug_names):  # Sort the drug names alphabetically
            f.write(drug + '\n')  # Write each drug name to the file

drug_names = get_drugs()
write_drugs(drug_names)