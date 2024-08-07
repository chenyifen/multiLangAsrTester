import os
import glob
import jiwer
from datetime import datetime
import csv

def calculate_wer(reference_file, hypothesis_file):
    with open(reference_file, 'r', encoding='utf-8') as ref_file:
        reference = ref_file.read().strip()
    with open(hypothesis_file, 'r', encoding='utf-8') as hyp_file:
        hypothesis = hyp_file.read().strip()
    return jiwer.wer(reference, hypothesis)

def process_folder(folder_path, lang):
    wer_results = {}
    detailed_wer_results = {}
    for txt_file in glob.glob(os.path.join(folder_path, '*.txt')):
        print(f"txt_file = {txt_file}")
        if 'standard' in txt_file:
            continue  # Skip reference files

        # Extract model identifier
        model_name = '_'.join(txt_file.split('_model_')[1].split('.')[:-1])
        testcase_name = txt_file.split('/')[-1].split('_model_')[0]  # Extract testcase name

        # Find corresponding standard file
        standard_file = os.path.join(folder_path, f"{testcase_name}_standard.txt")
        
        if not os.path.exists(standard_file):
            print(f"Standard file missing for {testcase_name}, standard_file = {standard_file}")
            continue
        
        print(f"Calculating For Case  {testcase_name}, model: {model_name}")

        # Calculate WER
        wer = calculate_wer(standard_file, txt_file) * 100  # Convert to percentage
        print(f"Calculating For Case  {testcase_name}, model: {model_name}: WER = {wer:.2f}%")

        # Accumulate results
        if model_name not in wer_results:
            wer_results[model_name] = []
        wer_results[model_name].append(wer)

        # Store detailed results
        if model_name not in detailed_wer_results:
            detailed_wer_results[model_name] = {}
        detailed_wer_results[model_name][testcase_name] = wer

    # Compute average WER per model
    average_wer_results = {model: sum(wers) / len(wers) for model, wers in wer_results.items()}

    # Ensure wer_results directory exists
    results_dir = 'wer_results'
    os.makedirs(results_dir, exist_ok=True)

    # Generate file names with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_file_md = os.path.join(results_dir, f"wer_results_{lang}_{timestamp}.md")
    results_file_csv = os.path.join(results_dir, f"wer_results_{lang}_{timestamp}.csv")

    # Write results to markdown file
    with open(results_file_md, 'w', encoding='utf-8') as result_file:
        result_file.write(f"# WER Results for {lang.capitalize()}\n\n")
        result_file.write(f"## Summary\n\n")
        result_file.write(f"| Model | Average WER (%) |\n")
        result_file.write(f"|-------|-----------------|\n")
        for model, average_wer in average_wer_results.items():
            result_file.write(f"| {model} | {average_wer:.2f} |\n")
        
        result_file.write(f"\n## Detailed Results\n\n")
        for model, testcases in detailed_wer_results.items():
            result_file.write(f"### Model: {model}\n\n")
            result_file.write(f"| Test Case | WER (%) |\n")
            result_file.write(f"|-----------|---------|\n")
            for testcase_name, wer in testcases.items():
                result_file.write(f"| {testcase_name} | {wer:.2f} |\n")

    # Write results to CSV file
    with open(results_file_csv, 'w', encoding='utf-8', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        # Write summary
        csv_writer.writerow(["Model", "Average WER (%)"])
        for model, average_wer in average_wer_results.items():
            csv_writer.writerow([model, f"{average_wer:.2f}"])
        # Write detailed results
        csv_writer.writerow([])
        csv_writer.writerow(["Model", "Test Case", "WER (%)"])
        for model, testcases in detailed_wer_results.items():
            for testcase_name, wer in testcases.items():
                csv_writer.writerow([model, testcase_name, f"{wer:.2f}"])

    print(f"Results saved to {results_file_md} and {results_file_csv}")

def process_all_folders():
    base_path = '.'  # Change this to the directory where the folders are located if different
    for folder in glob.glob(os.path.join(base_path, 'asr_result_lang_*')):
        lang = folder.split('_')[-1]  # Extract language
        process_folder(folder, lang)

# Usage
process_all_folders()
