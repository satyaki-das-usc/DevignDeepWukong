filpath = "dwk.yaml"

with open(filpath, "r") as f:
    data = f.read()

batch_num = 1
dataset_name = f"devign{batch_num}"
old_txt = f"name: {dataset_name}"

batch_num += 1
dataset_name = f"devign{batch_num}"
new_txt = f"name: {dataset_name}"

data = data.replace(old_txt, new_txt)

with open(filpath, "w") as f:
    f.write(data)