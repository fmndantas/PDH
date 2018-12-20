# PDH

Plesiochronous Digital Hierarchy automated design for asynchronous multiplexing.

## Installation

If you have a working version of `git` on your system you can simply clone this repo using

    $ git clone https://github.com/fmndantas/PDH.git

or download the ZIP file clicking the green button above.

If you're using any Windows OS, the final `.exe` file will be encountered inside the directory
```/distros/windows/final_executable/dist/PDH.exe```

## Dependencies

This package is built upon `PyQt5` and `numpy` libraries.
If you have Python3 on your system you can install them using pip:
```
pip install numpy
pip install PyQt5
```

## Quick start

After running `PDH.py` or `PDH.exe`, you will be presented
with a simple interface:

![shot1](https://github.com/fmndantas/PDH/blob/master/screenshots/shot1.png?raw=True "Title")

From there one can change the transceptors frequency (default: 15 GHz)
or the number of stations the system will have.
After any of these properties are changed you should click the
"Update properties" button.

For this example, lets keep the default frequency and change
the number of stations to 5.

Lets say we have the following info for our example:

| Path | Distance (km) | Channels |
|------|---------------|----------|
| A-B  | 10            | ---      |
| A-D  | 8             | 420      |
| B-C  | 30            | 300      |
| B-E  | 18            | ---      |
| A-E  | ---           | 300      |
| B-D  | ---           | 480      |
| C-E  | ---           | 120      |

In the "Distance Matrix" we shall input the information
from the Distance column above, and in the "Channels Matrix"
we shall input the corresponding column above. (Private Lines will
be implemented in a future version).

![shot2](https://github.com/fmndantas/PDH/blob/master/screenshots/shot2.png?raw=True "Title")
![shot3](https://github.com/fmndantas/PDH/blob/master/screenshots/shot3.png?raw=True "Title")

There's also the possibility to alter the prices for each
component in the "Prices table"; for this simple example we'll
leave it as it is.

![shot4](https://github.com/fmndantas/PDH/blob/master/screenshots/shot4.png?raw=True "Title")

If everything is updated correctly, in the output tab we
can already have access to the "Channels per path" and
the choice of the transmission medium best suited for each path,
taking in consideration viability and total cost.

![shot5](https://github.com/fmndantas/PDH/blob/master/screenshots/shot5.png?raw=True "Title")
![shot6](https://github.com/fmndantas/PDH/blob/master/screenshots/shot6.png?raw=True "Title")

Lastly, in the "Budget window" one can see the summary of every
component need for the design and their associated costs.

![shot7](https://github.com/fmndantas/PDH/blob/master/screenshots/shot7.png?raw=True "Title")

## Futures updates

* The TL (transmission lines) will be considered
* For now, the obstacle loss per path is not editable and is fixed in 8 dB. The change in those parameters will be considered in future updates.
* The budget screen will have a nicer        desing :)