import os
from os.path import isfile, isdir, join
import pandas as pd

def main():
    SRC_PATH = "devign/devign.csv"

    df = pd.read_csv(SRC_PATH)

    labels = ["good", "bad"]

    DST_DIR = "devign/just-src-files"

    if not isdir(DST_DIR):
        os.mkdir(DST_DIR)

    cmd = "for f in " + DST_DIR + "/*; do rm \"$f\"; done"
    os.system(cmd)
    
    all_filenames = []
    file_extension = ".c"

    incomplete_cnt = 0
    
    for row in df.itertuples():
        filename = f"{row.project}_{row.commit_id}_{labels[row.target]}{file_extension}"
        cnt = 0
        file_ending = f"{file_extension}"
        while filename in all_filenames:
            offset = -1 * len(file_ending)
            filename = f"{filename[:offset]}{cnt}{file_extension}"
            file_ending = f"{cnt}{file_extension}"
            cnt += 1
        
        DST_PATH = join(DST_DIR, filename)
        if not isfile(DST_PATH):
            os.system(f"touch {DST_PATH}")
        
        src_code = str(row.processed_func).strip()
        if not src_code.endswith("}"):
            src_code = f"{src_code}\n}}"
            incomplete_cnt += 1
        with open(DST_PATH, "w") as f:
            f.write(src_code)
        all_filenames.append(filename)
    
    print(f"Fixed {incomplete_cnt} broken codes")


if __name__ == "__main__":
    main()