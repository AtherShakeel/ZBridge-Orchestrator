import os

def generate_transactions(count=100):
    output_path = "data/transactions.txt"
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w") as f:
        for i in range(1, count + 1):
            # 1. T-LOAN-ID-IN (Col 1-10)
            loan_id = f"LN{i:08}"

            # 2. T-BORROWER-IN (Col 11-40)
            name = f"USER {i}".ljust(30)

            # 3. T-AMOUNT-IN (Col 41-49)
            # We vary amounts: some will be > 500k ($500,000.00 = 000500000)
            if i % 10 == 0:
                amount_val = 75000000  # $750,000.00 (Trigger Alert Logic)
            else:
                amount_val = 12500000  # $125,000.00
            amount_str = f"{amount_val:09}"

            # 4. T-STATUS-IN (Col 50) - Initialize as blank
            status = " "

            # 5. T-FILLER-IN (Col 51-79)
            filler = " " * 29

            # 6. T-CODE (Col 80) - ROTATE CODES TO TEST EVALUATE BRANCHING
            # Record 1='A', 2='B', 3='C', 4='A'...
            codes = ['A', 'B', 'C']
            t_code = codes[i % 3]

            # TOTAL MAPPING: 10 + 30 + 9 + 1 + 29 + 1 = 80 BYTES
            line = f"{loan_id}{name}{amount_str}{status}{filler}{t_code}"

            if len(line) == 80:
                f.write(line + "\n")
            else:
                print(f"CRITICAL ALIGNMENT ERROR at Record {i}: {len(line)} chars")

    print(f"Success: 100 records generated with varying T-CODEs (A, B, C).")

if __name__ == "__main__":
    generate_transactions(100)
