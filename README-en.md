English | [日本語](//github.com/mntone/ShakeScouter/blob/main/README.md)

# ShakeScouter

ShakeScouter is a Python program designed to analyze images from the “Salmon Run Next Wave” and generate telemetry data. This tool is specifically tailored for analyzing video streams from the Salmon Run game mode in the popular video game “Splatoon 3” on the Nintendo Switch.

## Table of contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Contribution](#contribution)
* [License](#license)
* [Acknowledgments](#acknowledgments)
* [Author](#author)
* [Related Projects](#related_projects)

## Features

- **Image Analysis**: ShakeScouter uses advanced image processing techniques to analyze video streams from the “Salmon Run Next Wave” game mode.
- **Telemetry Generation**: The program generates telemetry data based on the analysis results, providing valuable insights into the gameplay statistics.

## Installation

1. Clone the repository: `git clone https://github.com/mntone/ShakeScouter.git`
2. Navigate to the project directory: `cd ShakeScouter`
3. Install Python:
    - Windows: https://www.microsoft.com/store/productId/9NCVDN91XZQP
    - macOS: `brew install python@3.12`
4. Install dependencies: `pip install -r requirements.txt`
5. Install PyTorch: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`

In the future, there is a possibility of adopting analysis programs using CUDA on Windows.

## Usage

```sh
py shakescout.py [options]
```

### Options

- `--development`: Run the program in development mode.
- `-d`, `--device`: Specify the device to use in PyTorch. Available options are `auto`, `cpu`, and `cuda`.
- `-o`, `--outputs`: Specify the output types. Available options are `console`, `json`, and `websocket`.
- `-i`, `--input`: Specify the device ID of the OpenCV input.
- `--width`: Specify the width of the OpenCV input.
- `--hight`: Specify the height of the OpenCV input.
- `-t`, `--timestamp`: Use timestamp as json filename.
- `-H`, `--host`: Specify the hostname for the WebSocket connection.
- `-p`, `--port`: Specify the port number for the WebSocket connection.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the GPLv3 license - see the [LICENSE](//github.com/mntone/ShakeScouter/blob/main/LICENSE) file for details.

## Contact

If you have any questions or need support, please contact me.

- Mastodon: https://mstdn.jp/@mntone

## Acknowledgments

- My heartfelt thanks go out to the creators of the original game, “Splatoon 3.”
- I would like to express my gratitude to [erudot](https://x.com/erudot). He provided me with the opportunity to play Salmon Run Next Wave and became the catalyst for reaching Eggsecutive VP 999.
- Also, I would like to express my heartfelt gratitude to ChatGPT for its support in the development of this software.

## Author

- mntone - Initial work.

## Related Projects

- [Shake StreamKit](//github.com/mntone/shake-streamkit): A tool for overlaying Salmon Run Next Wave streams

