# kalindro-custom-loguru-logger

Hi, it's my custom logger. Loguru is great, I just made few changes, done through inheritance, 
to simplify for my use case, still returns the Loguru logger so everything is compatible.

Install using Pip:
```shell
pip install "git+https://github.com/Kalindro/kalindro-custom-loguru-logger.git"
```
Install using Poetry:
```shell
poetry add "git+https://github.com/Kalindro/kalindro-custom-loguru-logger.git"
```
After installing just use as:
```shell
from kalindro_custom_loguru_logger import default_logger as logger
```