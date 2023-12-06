## INSTALL PYTHON

## Do this in [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)

### Python 3.9

```code
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel
sudo wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
sudo tar xvf Python-3.9.10.tgz
cd Python-*/
./configure --enable-optimizations
sudo make altinstall
```

```code
python3.9 --version
````

### VIRTUAL ENVIRONMENT

```code
cd ~
````

```code
python3.9 -m venv env
````
```code
source env/bin/activate
```
```code 
python --version
```

### CREATION OF FOLDERS FOR LAYERS

```code
mkdir -p Python/lib/python3.9/site-packages
cd python/lib/python3.9/site-packages
````
```code
pip3 install <nanme> -t .
```

### ZIP AND DOWNLOAD THE LIBRARIES

```code
cd ~
zip -r chroma.zip Python/*
```
```code
pwd
```