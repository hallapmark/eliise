# eliise
Eliise juturobot (An Estonian implementation of the Eliza chatbot)

### Installation
1) It is recommended to have [conda](https://www.anaconda.com/products/distribution) for this project. 
2) Once you have conda, clone the project into a folder on your computer.
3) Make sure you are running exactly Python 3.9.x. If you are using conda, then in your terminal/shell you can create a suitable environment with the command `conda create -n py39eliise python=3.9`. Then run `conda activate py39eliise`. 
4) Make sure you have the [estnlk](https://github.com/estnltk/estnltk) natural language processing library installed. If you created the conda environment described in step 3 activated, then you can install it with the command `conda install -c estnltk -c conda-forge estnltk=1.7.0rc0`. Note: this is a large library with its own dependencies. If you run into any trouble with the installation, follow the [instructions](https://github.com/estnltk/estnltk)in the library documents.

### Use
In your terminal, navigate to the folder where you cloned Eliise. If you are using conda, remember to check that you have the environment described above activated. Then run `python eliise_cmdl_interface.py`
