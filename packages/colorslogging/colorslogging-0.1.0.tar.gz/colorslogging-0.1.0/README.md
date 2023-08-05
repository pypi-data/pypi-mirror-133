# colorslogging
python3 logging custom


use with default
```
In [1]: from colorslogging import ColoredFormatter

In [2]: logger = ColoredFormatter.GetLogger()

In [3]: logger.success('awesome')
SUCCESS - 2021-12-28 14:18:29,913 - process: 14335 - <ipython-input-3-f8f3e90c31f2> - colorslogging - 1 - <ipython-input-3-f8f3e90c31f2> - awesome
```

use colorslogging in ipython like this:
[![asciicast](https://asciinema.org/a/sMhhU2tGIu9hEtLLZZj3rJujc.svg)](https://asciinema.org/a/sMhhU2tGIu9hEtLLZZj3rJujc)

use with customized level & color
```
In [1]: from colorslogging import ColoredFormatter

In [2]: logger = ColoredFormatter.CusGetLogger(cus_color = 35 ,cus_level = 'NMD' , cus_level_name = 'nmd' , custom_level_num = 29 )

In [3]: logger.nmd('awesome')
NMD - 2021-12-28 14:18:00,023 - process: 14319 - <ipython-input-3-777eaf5b107b> - colorslogging - 1 - <ipython-input-3-777eaf5b107b> - awesome
```

logger add new custom level
```
In [1]: from colorslogging import ColoredFormatter

In [2]: import logging

In [3]: logger = ColoredFormatter.GetLogger()

In [4]: logger.info("test") # default logging level is info
INFO - 2021-12-28 14:20:27,160 - process: 14398 - <ipython-input-4-9110207720aa> - colorslogging - 1 - <ipython-input-4-9110207720aa> - test

In [5]: logger.setLevel(logging.SUCCESS) # set logging level to SUCCESS

In [6]: logger.info("test") # logging.info will ignore

In [7]: logger.success("test") # logging.success will work
SUCCESS - 2021-12-28 14:21:16,475 - process: 14398 - <ipython-input-7-751294c71e00> - colorslogging - 1 - <ipython-input-7-751294c71e00> - test

In [8]: logger = ColoredFormatter.add_level(logger = logger , level_name = 'nmb' ,level_num = 45 , cf_instance=ColoredFormatter() ,  cus_color = 100 ) # add_level fun   ...: c will add custom level , pass the param (logger = logger_instance , level_name='custom_name' , level_num = range(10-50) , cf_instance = ColoredFormatter_inst   ...: ance , cus_color = color_num  ) color_num can find in here : https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux01    

In [9]: logger.nmb('cao')
NMB - 2021-12-28 14:24:39,637 - process: 14398 - <ipython-input-10-1b2a3d296c96> - colorslogging - 1 - <ipython-input-10-1b2a3d296c96> - cao
```
![usage](./pic/pic1.png "usage")
