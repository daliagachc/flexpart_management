- here i will try the example described [here](
https://www.flexpart.eu/wiki/FpLimitedareaWrf
)

- the test case input data links are:
  - https://www.flexpart.eu/downloads/flexwrf_v31_testcases.tar.gz  
  - https://www.flexpart.eu/downloads/flexwrf_v30_testcases.tar.gz
  
- the wrf input files are: 
  - https://www.flexpart.eu/downloads/Wrfdata.tar.gz
  - https://www.flexpart.eu/downloads/Wrfdata.tar.gz\
  they are similar here. 
  
- make sure you use the example provided by version 3.3.1 input since otherwise you will get the pathname error
  - solution for that error was provided by Victoria's [post](https://www.flexpart.eu/ticket/167)
  - copy data file from version 3.3
  - if error "calcpar - richardson" 
    - init time needs to be changed. see info [here](https://www.flexpart.eu/ticket/171) 
