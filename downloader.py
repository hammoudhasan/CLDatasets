import time
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import zipfile


class CLDatasets:
    """
    A class for downloading datasets from Google Cloud Storage.
    """

    def __init__(self, dataset: str, directory: str, unzip: bool = True):
        """
        Initialize the CLDatasets object.

        Args:
            dataset (str): The name of the dataset to download.
            directory (str): The directory where the dataset will be saved.
        """
        if dataset not in ['CGLM', 'CLOC', 'ImageNet2K']:
            print("Dataset not found!")
            return
        else:
            self.dataset = dataset
            self.directory = directory

            if not os.path.exists(self.directory):
                os.makedirs(os.path.join(self.directory, 'order_files'))
                os.makedirs(os.path.join(self.directory, 'data'))

            print("Dataset Selected:", dataset)
            self.download_order_files()
            self.download_data_files()

            if unzip:
                self.unzip_data_files(self.directory+"/data")

    def download_order_files(self):
        """
        Download the order files from Google Cloud Storage.
        """
        print("Order files are being downloaded...")
        start_time = time.time()
        download_command = f"gsutil -m cp gs://cl-datasets/{self.dataset}/order_files/* {self.directory}/order_files/ "
        os.system(download_command)
        elapsed_time = time.time() - start_time
        print("Elapsed time:", elapsed_time)

    def download_data_files(self):
        """
        Download the data files from Google Cloud Storage.
        """
        print("Data files are being downloaded...")
        start_time = time.time()
        download_command = f"gsutil -m cp -r gs://cl-datasets/{self.dataset}/data/* {self.directory}/data/ "
        os.system(download_command)
        elapsed_time = time.time() - start_time
        print("Elapsed time:", elapsed_time)

    def unzip_data_files(self, directory: str) -> None:
        """
        Extracts the contents of zip files in a directory into nested folders.

        Args:
            directory: The path to the directory containing the zip files.

        Returns:
            None
        """
        zip_files = [file for file in os.listdir(
            directory) if file.endswith('.zip')]

        def extract_single_zip(zip_file: str) -> None:
            zip_path = os.path.join(directory, zip_file)
            output_dir = os.path.join(directory, os.path.splitext(zip_file)[0])
            os.makedirs(output_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)

        with ThreadPoolExecutor() as executor, tqdm(total=len(zip_files)) as pbar:
            futures_list = []
            for zip_file in zip_files:
                future = executor.submit(extract_single_zip, zip_file)
                future.add_done_callback(lambda p: pbar.update(1))
                futures_list.append(future)

            # Wait for all tasks to complete
            for future in futures_list:
                future.result()

        # Remove zip files
        remove_command = f"rm {self.directory}/data/*.zip"
        os.system(remove_command)


if __name__ == "__main__":
    gcp_cl_datasets = CLDatasets(
        dataset='CGLM', directory='/data/cl_datasets/files/CGLM/')
