# Statements
    This spider is used to crawl the data of investment strategy from the applet investment manager in the Tiantian Fund app of Dongfang Wealth. If no proxy is configured, frequent crawling may result in IP blocking



# Environment

python 3.10.7+

windows 10




# Directory structure
    │  fundSpider.py			// core spider file
    │  init.bat					// initialize environment
    │  loggers.py				// log moduler
    │  ReadMe.md				// english documentation		
    │  requirements.txt			// dependent packages
    │  start.bat				// start spider
    |  utils.py					// utils methods
    │  使用说明.txt				 // chinese documentation
    │  
    │
    ├─.idea			// auto generated					
    │  
    │    
    │      
    ├─fundData		// data directory
    │ 
    |
    ├─log			// log files 
    |
    │          
    ├─venv			
    │  │              
    │  └─Scripts	// virtual environment scripts
    │      
    │              
    └─__pycache__	// python cache files



# Instruction

```
To run the spider, double click 'start.bat'. The crawled data is saved in the folder 'fundData' under the project root directory. Log files could be found in the folder 'log'.
```

