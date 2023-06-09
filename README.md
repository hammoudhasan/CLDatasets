# Continual Learning Datasets 📚

Welcome to the Continual Learning Datasets repository! Here, we aim to make large-scale continual learning datasets easily accessible for everyone. Our repository provides a convenient way to download three large scale diverse datasets: CLOC, CGLM, and ImageNet2K. Feel free to explore, experiment, and contribute to our repo!

## Table of Contents 📋

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Citing Our Work](#citing-our-work)
- [Citing Relevant Works](#citing-relevant-works)
- [Contributing](#contributing)
- [License](#license)

## Introduction 🌟

In the world of continual learning, obtaining and working with large-scale datasets can be a challenging task. Our Continual Learning Datasets repository addresses the following issues faced by researchers and practitioners: Setting up large-scale continual learning datasets can often be cumbersome and involve complicated processing steps.

To make your journey smoother, we provide an easy-to-use solution for downloading and working with three prominent continual learning datasets: CLOC, CGLM, and ImageNet2K. These datasets offer a rich variety of real-world scenarios to explore and develop continual learning algorithms.

## Repository Structure 📂

The repository is structured as follows:

```
📦 CLDatasets
 ┣ 📂 src
 ┃ ┣ 📜 downloader.py
 ┃ ┗ 📜 dataloader.py
 ┗ 📜 README.md (You are here!)

```

- **src**: This directory contains the source code for downloading and creating the continual learning datasets.
  - `downloader.py`: Use this script to download any of the three datasets along with their order files.
  - `dataloader.py`: This script allows you to create the dataset easily within your code.

## Getting Started 🚀

To get started with Continual Learning Datasets, follow these simple steps:

1. Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/hammoudhasan/CLDatasets.git
   ```
2. Navigate to the `src` directory:
   ```bash
   cd CLDatasets/src
   ```
3. Use the `downloader.py` script to download your desired dataset. Open your terminal and run the following command:
   ```bash
   python downloader.py --dataset=<dataset_name> --directory=<directory> --unzip
   ```
   Replace `<dataset_name>` with either `CLOC`, `CGLM`, or `ImageNet2K`, depending on the dataset you want to download. `<directory>` should be the path where you want to store the dataset. Additionally, you can include the `--unzip` flag to automatically extract the downloaded files, which is recommended.

   Here's an example of how you could use the script to download the CLOC dataset:
   ```bash
   python downloader.py --dataset='CLOC' --directory='/data/cl_datasets/files/ImageNet2K/' --unzip
   ```

4. Once downloaded, you can use `dataloader.py` to easily incorporate the dataset into your code.

Note that our data could also be found on [this](https://console.cloud.google.com/storage/browser/cl-datasets) GCP Bucket.
****
Feel free to explore the repository further and adapt the code to suit your specific requirements.

## Citing Our Work 📖

This initiative is part of our work found [here](https://arxiv.org/abs/2305.09275). If you find the Continual Learning Datasets repository useful and download any of the datasets using our repo, please cite our work:

```
@misc{hammoud2023rapid,
      title={Rapid Adaptation in Online Continual Learning: Are We Evaluating It Right?}, 
      author={Hasan Abed Al Kader Hammoud and Ameya Prabhu and Ser-Nam Lim and Philip H. S. Torr and Adel Bibi and Bernard Ghanem

},
      year={2023},
      eprint={2305.09275},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

## Citing Relevant Works 🔍

Additionally, when using the individual datasets, please cite the relevant works:

**For CLOC:**
```
@InProceedings{Cai_2021_ICCV,
    author    = {Cai, Zhipeng and Sener, Ozan and Koltun, Vladlen},
    title     = {Online Continual Learning With Natural Distribution Shifts: An Empirical Study With Visual Data},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
    month     = {October},
    year      = {2021},
    pages     = {8281-8290}
}
```

_Suggestion: You could also cite:_

```
@inproceedings{ghunaim2023real,
  title={Real-time evaluation in online continual learning: A new hope},
  author={Ghunaim, Yasir and Bibi, Adel and Alhamoud, Kumail and Alfarra, Motasem and Al Kader Hammoud, Hasan Abed and Prabhu, Ameya and Torr, Philip HS and Ghanem, Bernard},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={11888--11897},
  year={2023}
}
```

**For CGLM:**
```
@InProceedings{Prabhu_2023_CVPR,
    author    = {Prabhu, Ameya and Al Kader Hammoud, Hasan Abed and Dokania, Puneet K. and Torr, Philip H.S. and Lim, Ser-Nam and Ghanem, Bernard and Bibi, Adel},
    title     = {Computationally Budgeted Continual Learning: What Does Matter?},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2023},
    pages     = {3698-3707}
}
```
```
@article{prabhu2023online,
  title={Online Continual Learning Without the Storage Constraint},
  author={Prabhu, Ameya and Cai, Zhipeng and Dokania, Puneet and Torr, Philip and Koltun, Vladlen and Sener, Ozan},
  journal={arXiv preprint arXiv:2305.09253},
  year={2023}
}
```

**For ImageNet2K:**
```
@InProceedings{Prabhu_2023_CVPR,
    author    = {Prabhu, Ameya and Al Kader Hammoud, Hasan Abed and Dokania, Puneet K. and Torr, Philip H.S. and Lim, Ser-Nam and Ghanem, Bernard and Bibi, Adel},
    title     = {Computationally Budgeted Continual Learning: What Does Matter?},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2023},
    pages     = {3698-3707}
}
```


## Contributing 🤝

Contributions are welcome and appreciated! If you have any ideas, suggestions, or improvements, please open an issue or submit a pull request. Together, let's make continual learning more accessible and exciting for everyone!

## License ⚖️

The datasets utilized in this project, namely ImageNet, CLOC, and CGLM, are subject to their respective original licensing terms. These datasets are provided for research purposes only, and you must adhere to the original licensing requirements set forth by their respective owners.

Modifying, redistributing, or sublicensing any part of the ImageNet, CLOC, or CGLM datasets without explicit permission from the original dataset owners is strictly prohibited.

Please refer to the individual dataset sources and their respective licenses for more details on the permissions and restrictions associated with each dataset.

---

Let's embark on a continual learning journey! If you have any questions or need further assistance, feel free to reach out. Happy learning! 🚀✨
