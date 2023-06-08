import os
from typing import Callable, Optional, Tuple

import h5py
from PIL import Image


class BaseDataClass:
    """Base class for a data class."""

    def __init__(self, dataset: str, directory: str):
        """
        Initialize the BaseDataClass.

        Args:
            dataset (str): Name of the dataset.
            directory (str): Path to the directory containing the data.

        Raises:
            FileNotFoundError: If 'order_files' or 'data' directories are not found.
        """
        self.dataset = dataset
        self.directory = directory

        # Check that 'order_files' and 'data' directories exist in the directory
        if not os.path.exists(os.path.join(self.directory, 'order_files')):
            raise FileNotFoundError("order_files directory not found!")

        if not os.path.exists(os.path.join(self.directory, 'data')):
            raise FileNotFoundError("data directory not found!")

        print(
            f"Found 'order_files' and 'data' directories for {self.dataset}!")

    def __getitem__(self, index):
        """
        Get an item from the data class.

        Args:
            index: Index of the item to retrieve.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def __len__(self):
        """
        Get the length of the data class.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


class H5Dataset(BaseDataClass):
    def __init__(self, dataset: str, directory: str, partition: str, transform: Optional[Callable] = None):
        """
        Initialize the H5Dataset.

        Args:
            dataset (str): Dataset name.
            dir (str): Directory path.
            partition (str): train, test, or pretrain.
            transform (callable, optional): Transform to apply to the samples. Defaults to None.

        Raises:
            FileNotFoundError: If any of the required files is not found.
        """
        super().__init__(dataset=dataset, directory=directory)
        self.directory = directory
        self.image_paths = h5py.File(
            f"{directory}/order_files/{partition}_image_paths.hdf5", "r")["store_list"]
        self.labels = h5py.File(
            f"{directory}/order_files/{partition}_labels.hdf5", "r")["store_list"]
        self.transform = transform

        assert len(self.image_paths) == len(self.labels)

    def __getitem__(self, index: int) -> Tuple[Image.Image, int]:
        """
        Get an item from the H5Dataset.

        Args:
            index (int): Index of the item to retrieve.

        Returns:
            tuple: A tuple containing the sample and label.
        """
        img_path = self.directory + '/data/' + \
            self.image_paths[index].decode("utf-8").strip()
        label = self.labels[index]
        sample = Image.open(img_path)

        if self.transform is not None:
            sample = self.transform(sample)

        return sample, label

    def __len__(self) -> int:
        """
        Get the length of the H5Dataset.

        Returns:
            int: Length of the dataset.
        """
        return len(self.image_paths)


if __name__ == "__main__":
    BaseDataClass(dataset='CGLM', directory='/data/cl_datasets/files/CGLM/')

    dataset = H5Dataset(
        dataset='CGLM', directory="/data/cl_datasets/files/CGLM/", partition='pretrain')
    print(len(dataset))
    dataset[0][0].show()
