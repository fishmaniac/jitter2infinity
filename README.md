# CPU Jitter Analysis

This project performs CPU jitter analysis using a Python test harness that interacts with a C library. The C library measures jitter, while Python handles testing and analysis. The library is built as a shared object (`.so`) and a dynamic-link library (`.dll`) for Linux and Windows platforms, respectively.

The jitter analysis includes statistical methods to assess the uniformity and randomness of jitter:

- **Shannon Entropy**: Measures the uncertainty in the jitter distribution.
- **Min-Entropy**: Calculates the minimal entropy, identifying the most predictable jitter values.
- **Chi-Square**: A statistical test for uniformity in the jitter distribution.

## Project Structure
```sh
├── build.sh
├── clean.sh
├── LICENSE
├── noise-sources
│   ├── build
│   │   ├── jitter2infinitylib.dll
│   │   └── jitter2infinitylib.so
│   ├── lib.h
│   ├── operations.c
│   └── timer.c
├── README.md
├── requirements.txt
├── run.sh
├── run_wsl.ps1
└── test
    ├── ffi.py
    ├── gui.py
    ├── main.py
    ├── operation.py
    └── statistics.py
```

## Requirements

Before running the project, you will need to have the following dependencies installed:

- Python 3.x
- GCC (for Linux) or `x86_64-w64-mingw32-gcc` (for Windows, via WSL)
- `pip` dependencies listed in `requirements.txt` (Python packages)

### Python Dependencies

To install Python dependencies, run:

```sh
pip install -r requirements.txt
```

### C Compiler Dependencies

For building the shared object and dynamic-link libraries, you'll need GCC or MinGW.

- **Linux**: Install GCC.
- **Windows (via WSL)**: Install `x86_64-w64-mingw32-gcc` (MinGW-w64).

## Build Instructions

To build the shared object (`.so`) for Linux and the dynamic-link library (`.dll`) for Windows, run the following:

### Linux

Run the `build.sh` script:

```sh
./build.sh
```

This will create the required `jitter2infinitylib.so` in the `noise-sources/build` directory.

### Windows (via WSL)

Run the `wsl -- ./build_wsl.ps1` PowerShell script to build the required Windows DLL via WSL. Make sure to have the proper WSL environment set up, including MinGW, before running:
```powershell
wsl -- ./build_wsl.ps1

# If you need to manually build the library, you can use MinGW as follows:
x86_64-w64-mingw32-gcc -O0 -shared -o jitter2infinitylib.dll noise-sources/operations.c noise-sources/timer.c
```

This will create the required `jitter2infinitylib.dll` in the `noise-sources/build` directory.

## Running the Analysis

### Linux / macOS

To run the test harness on Linux or macOS, use the `run.sh` script:

```sh
./run.sh
```

This will build the C library and then execute the Python test harness located in `test/main.py`.

### Windows (via WSL)

To run the test harness on Windows using WSL, use the `run_wsl.ps1` PowerShell script:

```powershell
.\run_wsl.ps1
```

This will build the C library and execute the Python test harness in `test/main.py`.

## Cleaning Up

To remove the generated build files, use the `clean.sh` script:

```sh
./clean.sh
```

This will delete the `noise-sources/build` directory containing the `.so` and `.dll` files.

## License

This project is licensed under the GPL3 License - see the [LICENSE](LICENSE) file for details.
