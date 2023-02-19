# ChatGPT_Hackathon

## Install Streamlit on Windows
Streamlit's officially-supported environment manager on Windows is [Anaconda Navigator](https://docs.anaconda.com/navigator/).

## Install Anaconda
If you don't have Anaconda install yet, follow the steps provided on the [Anaconda installation page](https://docs.anaconda.com/anaconda/install/windows/).

## Create a new environment with Streamlit
Next you'll need to set up your environment.

1. Follow the steps provided by Anaconda to [set up and manage your environment](https://docs.anaconda.com/navigator/getting-started/#managing-environments) using the Anaconda Navigator.

2. Select the "▶" icon next to your new environment. Then select "Open terminal":

3. In the terminal that appears, type:
```sh
pip install streamlit
```

4. Test that the installation worked:
```sh
streamlit hello
```
Streamlit's Hello app should appear in a new tab in your web browser!

## Use your new environment
1. In Anaconda Navigator, open a terminal in your environment (see step 2 above).

2. In the terminal that appears, use Streamlit as usual:
```sh
streamlit run app.py
```
