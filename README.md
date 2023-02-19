# ChatGPT_Hackathon

This is a Streamlit website to communicate with data in Snowflake database through inputing natual language and generating SQL query in ChatGPT interface.
Please heck out the instructions below to get set up and run the application.



## 1. Run Streamlit app on Windows
Streamlit's officially-supported environment manager on Windows is [Anaconda Navigator](https://docs.anaconda.com/navigator/).


### Install Anaconda
If you don't have Anaconda install yet, follow the steps provided on the [Anaconda installation page](https://docs.anaconda.com/anaconda/install/windows/).


### Create a new environment with Streamlit
Next you'll need to set up your environment.

1. Follow the steps provided by Anaconda to [set up and manage your environment](https://docs.anaconda.com/navigator/getting-started/#managing-environments) using the Anaconda Navigator.

2. Select the "▶" icon next to your new environment. Then select "Open terminal". If terminal can't opened by click, just open cmd, and type conda to run in Anaconda environment and activate the new new environment you created.
```sh
conda
```
```sh
activate <your new environment>
```

3. In the terminal that appears, type:
```sh
pip install streamlit
```

4. Test that the installation worked:
```sh
streamlit hello
```
Streamlit's Hello app should appear in a new tab in your web browser!

5. Install other required libraries in the new environment
```sh
pip install snowflake-connector-python
```
```sh
pip instal openai
```
```sh
pip instal pandas
```


### run the app in your new environment
1. In the terminal that appears, navigate to the project folder, use Streamlit as usual:
```sh
streamlit run app.py
```
To stop the Streamlit server, press `ctrl-C`.

2. When you're done using this environment, just type `exit` or press `ctrl-D` to return to your normal shell.





## 2. Run Streamlit app on macOS/Linux
Streamlit's officially-supported environment manager for macOS and Linux is [Pipenv](https://pypi.org/project/pipenv/). See instructions on how to install and use it below.


### Install Pipenv
1. Install `pip`. More details about installing `pip` can be found in [pip documentation](https://pip.pypa.io/en/stable/installation/#supported-methods).

On a macOS:
```sh
python -m ensurepip --upgrade
```

On Ubuntu with Python 3:
```sh
sudo apt-get install python3-pip
```

For other Linux distributions, see [How to install PIP for Python](https://www.makeuseof.com/tag/install-pip-for-python/).

2. Install `pipenv`.
```sh
pip install pipenv
```


### Install Xcode command line tools on macOS
On macOS, you'll need to install Xcode command line tools. They are required to compile some of Streamlit's Python dependencies during installation. To 
install Xcode command line tools, run:
```sh
xcode-select --install
```


### Create a new environment with Streamlit
1. Navigate to your project folder:
```sh
cd ChatGPT_Hackathon
```

2. Create a new Pipenv environment in that folder and activate that environment:
```sh
pipenv shell
```
When you run the command above, a file called Pipfile will `appear` in `ChatGPT_Hackathon/`. This file is where your Pipenv environment and its dependencies are declared.

3. Install Streamlit in your environment:
```sh
pip install streamlit
```
Or if you want to create an easily-reproducible environment, replace `pip` with `pipenv` every time you install something:
```sh
pipenv install streamlit
```

4. Test that the installation worked:
```sh
streamlit hello
```
Streamlit's Hello app should appear in a new tab in your web browser!

5. Install other required libraries in the new environment
```sh
pip install snowflake-connector-python
```
```sh
pip instal openai
```
```sh
pip instal pandas
```



### Use your new environment
1. Any time you want to use the new environment, you first need to go to your project folder (where the `Pipenv` file lives) and run:
```sh
pipenv shell
```

2. Now you can use Python and Streamlit as usual:
```sh
streamlit run myfile.py
```
To stop the Streamlit server, press `ctrl-C`.

3. When you're done using this environment, just type `exit` or press `ctrl-D` to return to your normal shell.