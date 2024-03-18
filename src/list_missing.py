from dataloader import H5Dataset
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os

def list_missing(split):
    dataset = H5Dataset(
        dataset="CGLM",
        directory="/export/work/cbotos/cldatasets/CGLM/",
        partition=split,
    )
    print(len(dataset))

    from functools import partial

    def check_path_exists(dataset, start_idx, end_idx):
        for i in tqdm(range(start_idx, end_idx), desc=f"Checking from {start_idx} to {end_idx}", leave=False):
            if not os.path.exists(dataset.directory + '/data/' + dataset.image_paths[i].decode("utf-8").strip()):
                raise Exception("Path not found", dataset.directory + '/data/' + dataset.image_paths[i].decode("utf-8").strip())
        

    missing_paths = []
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures_list = []
        chunk_size = 1000
        with tqdm(total=len(dataset)//chunk_size) as pbar:
            for i in range(0, len(dataset), chunk_size):
                future = executor.submit(check_path_exists, dataset, i, i+chunk_size)
                future.add_done_callback(lambda p: pbar.update())
                futures_list.append(future)

            for future in futures_list:
                result = future.result()
                missing_paths.append(result)


    f = open(f"CGLM_{split}_missing_paths.txt", "w")
    
    for i in missing_paths:
        if i is not None:
            print(f"{i[0]},{i[1]}", file=f)
    
    f.close()

if __name__ == "__main__":
    for split in ['train', 'test', 'pretrain', 'pretest', 'preval', 'cls_inc', 'data_inc']:
        print(split)
        try:
            list_missing(split)
        except Exception as e:
            print(e)
            continue
