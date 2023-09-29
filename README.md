# OPRAEL

An auto-tuning approach on parallel I/O tasks by ensemble learning and performance modeling using regression analysis.



# Environment

python         3.7.2

pip install requirements.txt



## IO-tuner

cd IO-tuner

gcc -fPIC -shared -ldl IO_tuner.c -o IO_tuner.so

export LD_PRELOAD=/path/IO_tuner.so



## Running

cd examples

python oprael_s3d.py



## Acknowledgment

The code implementation utilizes some APIs in Openbox.

https://github.com/thomas-young-2013/open-box/