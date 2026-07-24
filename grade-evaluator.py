import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
     # ── a) Score validation ──────────────────────────────────────────────────
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        print("\n[VALIDATION ERROR] The following assignments have scores outside 0-100:")
        for a in invalid_scores:
            print(f"  - {a['assignment']}: {a['score']}")
        sys.exit(1)
    print("[✓] All scores are within the valid range (0–100).")
 
    # ── b) Weight validation ─────────────────────────────────────────────────
    total_weight = sum(a['weight'] for a in data)
    formative_weight = sum(a['weight'] for a in data if a['group'].lower() == 'formative')
    summative_weight = sum(a['weight'] for a in data if a['group'].lower() == 'summative')
 
    weight_errors = []
    if total_weight != 100:
        weight_errors.append(f"Total weight is {total_weight}, expected 100.")
    if formative_weight != 60:
        weight_errors.append(f"Formative weight is {formative_weight}, expected 60.")
    if summative_weight != 40:
        weight_errors.append(f"Summative weight is {summative_weight}, expected 40.")
 
    if weight_errors:
        print("\n[VALIDATION ERROR] Weight validation failed:")
        for err in weight_errors:
            print(f"  - {err}")
        sys.exit(1)
    print("[✓] Weight validation passed (Total=100, Formative=60, Summative=40).")
 
    # ── c) Weighted grade & GPA ──────────────────────────────────────────────
    formative_assignments = [a for a in data if a['group'].lower() == 'formative']
    summative_assignments = [a for a in data if a['group'].lower() == 'summative']
 
    # Weighted score within each group as a percentage of that group's total weight
    formative_earned  = sum(a['score'] * a['weight'] for a in formative_assignments)
    summative_earned  = sum(a['score'] * a['weight'] for a in summative_assignments)
 
    formative_score   = formative_earned  / formative_weight   # score out of 100 for formative
    summative_score   = summative_earned  / summative_weight   # score out of 100 for summative
 
    # Overall grade: sum of (score * weight / 100) across all assignments
    total_grade = sum(a['score'] * (a['weight'] / 100) for a in data)
    gpa = (total_grade / 100) * 5.0
 
    # ── Print grade breakdown ────────────────────────────────────────────────
    print("\n--- Grade Breakdown ---")
    print(f"{'Assignment':<40} {'Group':<12} {'Score':>6} {'Weight':>7} {'Weighted':>10}")
    print("-" * 78)
    for a in data:
        weighted = a['score'] * (a['weight'] / 100)
        print(f"{a['assignment']:<40} {a['group']:<12} {a['score']:>6.1f} {a['weight']:>7.1f} {weighted:>10.2f}")
    print("-" * 78)
    print(f"\n{'Formative Score:':<35} {formative_score:>6.2f}%")
    print(f"{'Summative Score:':<35} {summative_score:>6.2f}%")
    print(f"{'Overall Grade:':<35} {total_grade:>6.2f}%")
    print(f"{'GPA:':<35} {gpa:>6.2f} / 5.0")
 
    # ── d) Pass/Fail ─────────────────────────────────────────────────────────
    passed_formative  = formative_score  >= 50
    passed_summative  = summative_score  >= 50
    passed_overall    = passed_formative and passed_summative
 
    # ── e) Resubmission logic ────────────────────────────────────────────────
    failed_formative = [a for a in formative_assignments if a['score'] < 50]
 
    resubmit_candidates = []
    if failed_formative:
        max_weight = max(a['weight'] for a in failed_formative)
        resubmit_candidates = [a for a in failed_formative if a['weight'] == max_weight]
 
    # ── f) Final output ───────────────────────────────────────────────────────
    print("\n--- Final Decision ---")
    if passed_overall:
        print("STATUS: ✅  PASSED")
        print(f"  (Formative: {formative_score:.2f}% ✓  |  Summative: {summative_score:.2f}% ✓)")
    else:
        print("STATUS: ❌  FAILED")
        reasons = []
        if not passed_formative:
            reasons.append(f"Formative score {formative_score:.2f}% is below 50%")
        if not passed_summative:
            reasons.append(f"Summative score {summative_score:.2f}% is below 50%")
        for r in reasons:
            print(f"  → {r}")
 
    print("\n--- Resubmission Eligibility ---")
    if not failed_formative:
        print("No failed formative assignments. No resubmission required.")
    else:
        print("Failed formative assignments eligible for resubmission "
              f"(highest weight = {max_weight}):")
        for a in resubmit_candidates:
            print(f"  • {a['assignment']} (Score: {a['score']}, Weight: {a['weight']})")
 
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)