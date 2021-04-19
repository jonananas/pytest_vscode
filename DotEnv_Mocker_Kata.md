# DotEnv Mocker Kata

We are going to create a utility that helps editing .env files, without writing or reading from disk.
We rely on the FileIO utility class for that, feel free to check [test_fileio.py](mocks/test_fileio.py) to understand what it does.
See [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args) for help on Mock.
The kata:

1. Create ```class DotEnv``` with a constructor that takes ```FileIO``` as parameter, 
		ie ```__init__(self, fileIO=FileIO())```

2. DotEnv read method should take a path to the file and return a dict, 
	1. When path is ".env", return "KEY=VALUE" from fileIO
 		- Use ```mock.<method>.return_value``` to tell fileIO what to return
 		- assert that the dict returned by DotEnv is correct, ie get("KEY") should be "VALUE"
  	2. Assert that the lines ["KEY=VALUE", "KEY2=VALUE2"] returns a dict with the keys KEY and KEY2.
	3. Make sure exception is propagated when path cannot be found.
		- Use ```mock.<method>.side_effect``` to tell fileIO to throw an exception
 
3. DotEnv write method should take a path to the file and a dict.
	1. Make sure ```fileio.writeLines``` is called from ```DotEnv.write```
		- Use ```mock.<method>.called```
	2. Make sure path is passed to ```fileio.writeLines```
 		- Use ```mock.<method>.call_args```
	3. Make sure the lines ["KEY=VALUE", "KEY2=VALUE2"] is passed to writeLines for a dict {"KEY": "VALUE", "KEY2": "VALUE2"}
	4. Make sure exceptions is propagated when path cannot be written to.

You are done! You may optionally run an integration test to prove the file is read and written correctly.
