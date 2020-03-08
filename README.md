# PyESP32ret
Python Client for ESP32RET https://github.com/collin80/ESP32RET 

$ python3 ./esp32ret.py 
(heartbeat ) Processing Heartbeat
(CanLogger ) Starting
(CanLogger ) ['-875482268', '-', '2a8', 'S', '0', '8', '2', '0', '0', '0', '0', '0', 'f0', '9c']
(heartbeat ) 1cefaced
(CanLogger ) ['-875482104', '-', '2e1', 'S', '0', '8', '1', '6c', '0', '0', '0', 'ff', 'e5', '3']
(CanLogger ) ['-875481940', '-', '212', 'S', '0', '8', '98', '4', '96', 'd', '1', '0', '2e', '6c']
(CanLogger ) ['-875481772', '-', '252', 'S', '0', '8', '0', '0', '7c', '9', '0', '0', '0', '0']

^C

$ sqlite3 model3-vehicle-bus.db "SELECT count(*) FROM sqlite_master WHERE type='table'"
182

$ sqlite3 model3-vehicle-bus.db ".tables"
102  201  228  261  287  2c3  2f9  320  352  383  3b2  3da  422  545  75d  82 
103  204  22a  262  288  2c4  300  321  359  387  3b3  3db  423  559  76a  c  
113  207  232  263  292  2d1  301  323  360  38a  3bb  3e2  428  666  772
119  20a  241  264  293  2d2  302  332  361  393  3c0  3e3  439  6c8  77a
122  20c  242  272  29d  2d3  303  333  362  398  3c2  3e8  43d  6e8  788
123  212  243  273  2a4  2e1  307  334  363  399  3c3  3ed  448  708  78a
132  213  247  27d  2a8  2e2  310  339  364  39a  3c4  3f2  458  72a  7a8
139  21d  24a  281  2b3  2e3  312  33a  372  3a1  3c8  3f5  473  739  7aa
1f8  221  252  282  2b4  2e8  313  340  379  3a2  3c9  3f9  4e2  743  7c8
1f9  224  253  283  2bd  2f1  318  343  37a  3a3  3d2  405  4e3  744  7e8
1fa  225  25a  284  2c1  2f2  319  345  381  3a4  3d3  41d  528  748  7f1
1fb  227  25d  285  2c2  2f3  31e  34a  382  3aa  3d8  421  53e  752  7ff


$ sqlite3 model3-vehicle-bus.db "select * from \"102\" limit 5"
-890087351|102|S|0|8|22 33 0 0 c6 12 91 9

