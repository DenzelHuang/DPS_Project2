# DPS_Project2
A project to compare different processing approaches using a provided dataset.

The goal is to compare filtering and sorting speeds using:
1. Sequential Processing
2. Thread Processing
3. Multiprocessing

## Methodology
The script will use each processing method to filter and sort the "trip duration" column then measure the time taken to compare the performance of each method.

Each batch of testing will use a sample of the given data that was randomly split into 25%, 50%, 75%, and 100% segments. This is to see if the performance of each method scales linearly or not.

## Usage
Download the dataset from this [link](https://drive.google.com/file/d/1uz1vKusNfAz4dKYtkerTnLl7IhVCI5_d/view?usp=sharing) and extract to the main project directory with the Dockerfile. Rename the CSV file to `data.csv`.

To use the script, you must have Docker installed.

If you already have Docker installed open the directory with the Dockerfile and open a terminal there then run the following command to build the Docker image:

`docker build -t trip-benchmark`

After building, run the following command to run the script:

`docker run -it --rm -v "$(pwd)/output":/app/output trip-benchmark`

Upon running the script, the user will be prompted to enter a filter method and its threshold, for example: le (less than or equal to) and 1000 (trip distance).

The outputs are written into three CSV files within the /output directory and the total time elapsed will be printed in the terminal.

## System Specifications
System 1 specs:
* CPU: [Ryzen 7 5800H](https://www.techpowerup.com/cpu-specs/ryzen-7-5800h.c2368)
  * Cores/Threads: 8/16
  * Base Clock Speed: 3.2 GHz
  * Boost Clock Speed: 4.4 GHz
* RAM: 16 (8x2) GB
  * Speed: 3200 MT/s
  * CL: 22
  * Type: DDR4
  * Form Factor: SODIM
