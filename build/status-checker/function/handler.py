import os
import csv
from datetime import datetime
import json

def handle(event, context):
    try:
        base_path = "/home/app/function"
        output_file = os.path.join(base_path, "Depot", "output.csv")

        if not os.path.exists(output_file):
            return json.dumps({
                "status": "error",
                "message": f"File {output_file} not found"
            }, indent=2)

        invalid_lines = []
        with open(output_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, 1):
                processed_date = row.get("Processed-Date")
                try:
                    # Teste le format de la date :
                    datetime.strptime(processed_date, "%Y-%m-%d %H:%M:%S")
                except:
                    invalid_lines.append({
                        "line": i,
                        "row": row,
                        "error": f"Invalid or missing Processed-Date: {processed_date}"
                    })

        if invalid_lines:
            return json.dumps({
                "status": "error",
                "message": "Invalid lines found",
                "invalid_lines": invalid_lines
            }, indent=2)
        else:
            return json.dumps({
                "status": "success",
                "message": "All lines are valid in output.csv"
            }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        }, indent=2)
