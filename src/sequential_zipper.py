import os
import argparse
import time
import zipfile
from io import BytesIO

from dataloader import H5Dataset
# from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import ProcessPoolExecutor as Pool
from tqdm import tqdm

def compress_single_zip(src_list: list, archive_list: list, target_zip: str, in_memory: bool = True) -> None:
    """
    Zips the files in the src_list into a single zip file.

    Args:
        src_list: A list of files to be zipped.
        archive_list: A list of archive names for the files in src_list.
        target_zip: The name of the zip file to be created.
        in_memory: Whether to create the zip file in memory first or on disk directly.
            (this uses more memory but is faster because it avoids incremental writes to disk)

    Returns:
        None
    """
    if not in_memory:
        with zipfile.ZipFile(target_zip, 'w') as zip_ref:
            for file, arc_name in zip(src_list, archive_list):
                zip_ref.write(file, arc_name)
    else:
        memory_zip = BytesIO()
        with zipfile.ZipFile(memory_zip, 'w') as zip_ref:
            for file, arc_name in zip(src_list, archive_list):
                zip_ref.write(file, arc_name)
        with open(target_zip, 'wb') as f:
            f.write(memory_zip.getvalue())

def extract_single_zip(directory: str, zip_file: str) -> None:
    zip_path = os.path.join(directory, zip_file)
    output_dir = os.path.join(
        directory, os.path.splitext(zip_file)[0])

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def zip_data_files(dataset, num_images, num_chunks, target_dir, parallel=True):
    """
    Zips the first N images from the dataset into M zip files.
    """

    os.makedirs(target_dir, exist_ok=True)
    
    # Get the list of file paths to be zipped
    src_list = [
        os.path.join(dataset.directory, "data", p.decode('utf-8').strip())
        for p in dataset.image_paths[:num_images]
    ]

    # Get the corresponding list of archive paths (relative to the dataset directory)
    archive_list = [
        p.decode('utf-8').strip()
        for p in dataset.image_paths[:num_images]
    ]

    chunk_size = num_images // num_chunks
    if parallel:
        with Pool() as executor, tqdm(total=num_chunks) as pbar:
            futures_list = []
            for i in range(num_chunks):
                start = i * chunk_size
                end = (i + 1) * chunk_size
                target_zip = os.path.join(target_dir, f"images_{i:04}.zip")
                future = executor.submit(compress_single_zip, src_list[start:end], archive_list[start:end], target_zip)
                future.add_done_callback(lambda p: pbar.update(1))
                futures_list.append(future)

            # Wait for all tasks to complete
            for future in futures_list:
                future.result()
    else:
        for i in range(num_chunks):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            target_zip = os.path.join(target_dir, f"images_{i:04}.zip")
            compress_single_zip(src_list[start:end], archive_list[start:end], target_zip)

def unzip_data_files(directory):
    zip_files = [file for file in os.listdir(
        directory) if file.endswith('.zip')]

    with Pool(max_workers=8) as executor, tqdm(total=len(zip_files)) as pbar:
        futures_list = []
        for zip_file in zip_files:
            # pbar.update(1)
            # extract_single_zip(directory, zip_file)
            future = executor.submit(extract_single_zip, directory, zip_file)
            future.add_done_callback(lambda p: pbar.update(1))
            futures_list.append(future)

        # Wait for all tasks to complete
        for future in futures_list:
            future.result()



if __name__ == "__main__":
    print("""
    This script will zip the first N images from the CLOC dataset
    so it can be copied efficiently on the compute node for experimentation.

    This script is meant to be run before any of the experiments start.
    The experiments won't be expected to run to completion, just to N images.
    """)
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="CLOC")
    parser.add_argument("--directory", type=str, default="/export/work/cbotos/cldatasets/CLOC")
    parser.add_argument("--split", type=str, default="train")
    parser.add_argument("--num-images", type=int, default=300000 * 128)
    parser.add_argument("--num-chunks", type=int, default=1024)
    parser.add_argument("--unzip", action="store_true")
    args = parser.parse_args()

    if args.unzip:
        unzip_data_files(args.directory)
        exit()
    
    target_dir = os.path.join(args.directory, "data", "sequentially_zipped", f"first_{args.num_images:010d}_images")

    dataset = H5Dataset(dataset=args.dataset, directory=args.directory, partition=args.split)
    zip_data_files(dataset, args.num_images, args.num_chunks, target_dir, parallel=True)
    print(f"The sequentially zipped files can be found in: {target_dir}")
    