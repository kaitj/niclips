<!-- prettier ignore -->
<h1> Niclips </h1>

![Python3](https://img.shields.io/badge/python->=3.11-blue.svg)
[![stability-alpha](https://img.shields.io/badge/stability-alpha-f4d03f.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#alpha)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/childmindresearch/niclips/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/childmindresearch/niclips)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/childmindresearch/niclips/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/documentation-8CA1AF?logo=readthedocs&logoColor=fff)](https://childmindresearch.github.io/niclips)

Niclips is an image and video generator for visualizing (neuroimaging) datasets.

## Installation

> [!TIP]
> For stability, Niclips should be installed in its own environment. For example, to
> install Niclips using `virtualenv`:
>
> ```sh
> python -m venv Niclips
> source niclips/venv/activate
> ```

Niclips can be installed using pip:

```sh
pip install -U pip
pip install git+https://github.com/childmindresearch/niclips.git
```

<!-- ## Usage

To get started, try using the boilerplate command:

```sh
niftyone <bids_directory> <output_directory> <analysis_level>
```

> [!TIP]
> To see all arguments, run:
>
> ```sh
> niftyone --help
> ```

### Quick-start

1. Generate figures for each participant

   ```sh
   niftyone <bids_directory> <output_directory> participant
   ```

2. Collect participant figures into a compatible dataset

   ```sh
   niftyone <bids_directory> <output_directory> group
   ```

3. Launch FiftyOne app

   ```sh
   niftyone <bids_directory> <output_directory> launch
   ``` -->

<!-- ## Documentation

For detailed information, including advanced usage, please visit our [documentation]. -->

## Contributing

Contributions to Niclips are welcome! Please refer to the
[Contributions] page for information on how to contribute, report issues, or submit
pull requests.

## License

Niclips is distributed under the [MIT license].

## Support

If you encounter any issues or have questions, please open an issue on the
[issue tracker].

<!-- Links -->

[Contributions]: https://github.com/childmindresearch/Niclips/blob/main/CONTRIBUTING.md
[MIT license]: https://github.com/childmindresearch/Niclips/blob/main/LICENSE
[issue tracker]: https://github.com/childmindresearch/Niclips/issues
