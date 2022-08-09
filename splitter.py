import os
from os.path import isfile, isdir, join

def main():
    SRC_DIR = "devign/just-src-files"
    for idx, filename in enumerate(os.listdir(SRC_DIR)):
        SRC_FILE_PATH = join(SRC_DIR, filename)
        batch_num = idx // 1000
        DST_DIR = SRC_DIR.replace("just-src-files", f"devign{batch_num}")
        
        if not isdir(DST_DIR):
            os.mkdir(DST_DIR)

        DST_FILE_PATH = join(DST_DIR, filename)
        os.system(f"mv {SRC_FILE_PATH} {DST_FILE_PATH}")

if __name__ == "__main__":
    main()