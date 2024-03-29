Introduction
This repository contains code for parallel execution of tests across different browsers using Selenium and Python. The code is structured into three main components:

test:  -test.py: Contains the test suite for parallel execution.
logic: -logic.py: Defines the logic for navigating through the website.
infra: -config.json, config_loader.py, page_base.py, browser_wrapper.py: Contains infrastructure-related code for setting up WebDriver and loading configurations.
Setup Instructions:
To set up and run the code, follow these steps:

Clone this repository to your local machine.
Ensure you have Python installed (version 3.6 or above).
Install the required dependencies using pip install -r requirements.txt.
Make sure you have compatible WebDriver executables (ChromeDriver, GeckoDriver, etc.) installed and available in your system PATH.
Adjust configurations in config.json as needed, specifying browser types and grid settings.

Contributing
Contributions are welcome! If you find any issues or would like to enhance the codebase, feel free to open an issue or submit a pull request.
