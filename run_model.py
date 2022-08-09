import os
from os.path import isfile, isdir, join
import json
import shutil
import pandas as pd

def main():
    batch_count = 28
    cwd = os.getcwd()
    MODEL_FOLDER_PATH = "/home/satyaki/luka/DeepWukongCopy"
    MODEL_DATA_FOLDER = join(MODEL_FOLDER_PATH, "data")
    MODEL_CONFIG_PATH = join(MODEL_FOLDER_PATH, "configs/dwk.yaml")

    for i in range(batch_count):
        datasetname = f"devign{i}"
        FIXED_HEADER_FOLDER = f"devign/{datasetname}"
        GROUND_TRUTH_PATH = f"devign/{datasetname}/ground_truth.json"
        RESULTS_PATH = f"devign/{datasetname}/results.json"
        SELECT_RESULTS_PATH = f"devign/{datasetname}/select_results.json"
        
        MODEL_CVE_DATA_FOLDER = join(MODEL_DATA_FOLDER, datasetname)
        DST_W2V_PATH = join(MODEL_CVE_DATA_FOLDER, "w2v.wv")
        ALL_JSON_FILE_PATH = join(MODEL_CVE_DATA_FOLDER, "all.json")
        RESULTS_JSON_FILE_PATH = join(MODEL_CVE_DATA_FOLDER, "results.json")
        DONE_TXT_FILE_PATH = join(MODEL_CVE_DATA_FOLDER, "done.txt")
        MODEL_GROUND_TRUTH_PATH = join(MODEL_CVE_DATA_FOLDER, "ground_truth.json")
        CSV_PATH = join(MODEL_CVE_DATA_FOLDER, "csv")
        XFG_PATH = join(MODEL_CVE_DATA_FOLDER, "XFG")
        SOURCE_CODE_PATH = join(MODEL_CVE_DATA_FOLDER, "source-code")

        # create initial ground truth
        
        ground_truth = dict()

        for filename in os.listdir(FIXED_HEADER_FOLDER):
            if "bad" in filename:
                ground_truth[filename] = [1]
        
        if not isfile(GROUND_TRUTH_PATH):
            os.system(f"touch {GROUND_TRUTH_PATH}")
        
        with open(GROUND_TRUTH_PATH, "w") as f:
            json.dump(ground_truth, f, indent=2)

        folders = [MODEL_CVE_DATA_FOLDER, SOURCE_CODE_PATH]

        for foldername in folders:
            if not os.path.isdir(foldername):
                os.mkdir(foldername)
        
        if not isfile(DST_W2V_PATH):
            SRC_W2V_PATH  = join(MODEL_CVE_DATA_FOLDER.replace(datasetname, "CWE119"), "w2v.wv")
            shutil.copyfile(SRC_W2V_PATH, DST_W2V_PATH)
        
        files = [ALL_JSON_FILE_PATH, RESULTS_JSON_FILE_PATH, DONE_TXT_FILE_PATH]

        for filename in files:
            if isfile(filename):
                command = f"rm {filename}"
                os.system(command)
        
        folders = [CSV_PATH, XFG_PATH]

        for foldername in folders:
            if isdir(foldername):
                command = f"rm -rf {foldername}"
                os.system(command)
        
        cmd = "for f in " + SOURCE_CODE_PATH + "/*; do rm \"$f\"; done"
        os.system(cmd)

        for filename in os.listdir(FIXED_HEADER_FOLDER):
            SRC_PATH = join(FIXED_HEADER_FOLDER, filename)
            DST_PATH = join(SOURCE_CODE_PATH, filename)
            shutil.copyfile(SRC_PATH, DST_PATH)
        
        shutil.copyfile(GROUND_TRUTH_PATH, MODEL_GROUND_TRUTH_PATH)

        with open(MODEL_CONFIG_PATH, "r") as f:
            model_config = f.read()
        
        old_batch_num = i - 1
        old_dataset_name = f"devign{old_batch_num}"
        old_txt = f"name: {old_dataset_name}"

        new_txt = f"name: {datasetname}"

        model_config = model_config.replace(old_txt, new_txt)

        with open(MODEL_CONFIG_PATH, "w") as f:
            f.write(model_config)

        os.chdir(MODEL_FOLDER_PATH)

        os.system(f"PYTHONPATH=\".\" python src/joern/joern-parse.py")
        os.system(f"PYTHONPATH=\".\" python src/data_generator.py")
        os.system(f"PYTHONPATH=\".\" python src/preprocess/dataset_generator.py")
        os.system(f"PYTHONPATH=\".\" python src/evaluate.py --dataset-name {datasetname} DeepWukong")
        
        os.chdir(cwd)

        MODEL_SELECT_RESULTS_PATH = os.path.join(MODEL_FOLDER_PATH, "select_results.json")

        shutil.copyfile(RESULTS_JSON_FILE_PATH, RESULTS_PATH)
        shutil.copyfile(MODEL_SELECT_RESULTS_PATH, SELECT_RESULTS_PATH)

if __name__ == "__main__":
    main()