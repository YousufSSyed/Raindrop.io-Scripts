# This documentation is outdated and I'm no longer updating it nor my scripts


# Raindrop.io-Scripts
Python scripts to interact with the raindrop.io Bookmarking Service. They require python-raindropio, which can be installed like so:

    pip install python-raindropio
First, create a copy of the repo:

    git clone https://github.com/YousufSSyed/Raindrop.io-Scripts.git

## API Key
An API key is required to use the scripts
* On raindrop.io under Settings > Integrations > For Developers (at the bottom), click "Create new app" & Give it any name and click "I accept."
* Click the new app, and copy into `APIKey` in `rdsettings.py` and click "Create test token" (the python-raindropi.io package seems to only support test tokens.**

## Scripts
* `rdsettings.py`, A file where you specify your API key, and a string array of tags.
* `add.py` - You can enter or copy & paste in multiple links. And enter in numbers corresponding to each of your tags specified in `settings.py` (much faster than typing them in manually, & if you use this script all the time, it becomes habit / muscle memory)
	* You can just keep this window open in your terminal and add new links whenever you have them.
	* To quickly access the script in bash, create an alias like this one:
	* `alias rd='/path/to/add.py'`
	* If you have any errors, just restart the script and try the links again
