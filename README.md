# DPS_Project2
A project to compare different processing approaches using a provided dataset.

The goal is to compare filtering and sorting speeds using:
1. Sequential Processing
2. Thread Processing
3. Multiprocessing

The dataset can be found [here](https://drive.google.com/file/d/1uz1vKusNfAz4dKYtkerTnLl7IhVCI5_d/view?usp=sharing).

## Methodology
The program will use each processing method to filter and sort the "trip duration" column then measure the time taken to compare the performance of each method.

Each batch of testing will use a sample of the given data that was randomly split into 25%, 50%, 75%, and 100% segements. This is to see if the performance of each method scales linearly or not.

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
