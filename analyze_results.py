import os
from os.path import isfile, isdir, join
import json

def main():
    batch_count = 28

    target_and_preds = []
    for i in range(batch_count):
        datasetname = f"devign{i}"
        RESULTS_PATH = f"devign/{datasetname}/results.json"

        with open(RESULTS_PATH, "r") as f:
            results = json.load(f)
        
        for entry in results:
            if "bad" in entry:
                target = 1
            else:
                target = 0
            if 1 in results[entry]:
                pred = 1
            else:
                pred = 0
            
            target_and_preds.append({"target": target, "pred": pred})
    
    total = len(target_and_preds)
    total_pos = 0
    total_neg = 0
    total_correct = 0

    for entry in target_and_preds:
        if entry["target"] == 1:
            total_pos += 1
        else:
            total_neg += 1
        
        if entry["target"] == entry["pred"]:
            total_correct += 1
    
    accuracy = (total_correct / total) * 100

    print(accuracy)

if __name__ == "__main__":
    main()