# Did I write this?!  *AI to Detect Fraudulent Tweets*
Fraudulent posts on social media are embarrassing to individuals and expensive to brands.  Language embedding models offer a means to characterize typical activity for a user and can be applied in a simple binary discriminator to screen incoming content.

This repository provides a demonstration of the use of language embedding (via [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/2)) to classify new Twitter posts as in or out-of-character for a particular user.  In a production system (implemented on the platform side), a user could be presented with secondary authentication to validate activity for the occasional false positive.

https://bit.ly/didIWriteThis

## Setup

Clone this repo with `git clone https://github.com/JoshuaGRubin/AI-Tweet-Validator.git <project_path>` on your command line.

*Optional*: while data from 13 Twitter users in included in the `data/raw` directory, if you'd like to be able to retrieve your own (e.g. more/other users, more recent tweets), you'll need to set up a Twitter developer account and app.  To do so, please visit https://developer.twitter.com, create an app, and have it approved. Once this is complete, you'll have access to API credentials. 

### Setup with Docker – *portable and stable*
**The recommended way to run this project is by installing Docker and building and running an image**.  This process manages libraries, the python runtime environment, and dependences; it also manages environment variables nicely.  This maximizes stability and portability.

- First, visit https://www.docker.com to install the Docker platform (e.g. Docker Desktop) on your machine.

- If you've created a Twitter developer account and you'd like to download new content, uncomment the appropriate four rows in `build\Dockerfile` and paste in your credentials.

- To build and run your container, run the following in your command shell.

```bash
cd <project_path>
./build_docker
./run_docker
```

- At this point, you should be able to `cd src/scripts` and `python <script_name>` to run any of the example scripts.  You also have the library, 'tweetvalidator' (from src/tweetvalidator) available in you `PYTHONPATH`, so you can include it in any of your own scripts.

### Setup with Anaconda – *lightweight*

While this setup has a few more steps and possibly plateform-dependent pitfalls, there's less to download and store on disk.

- Install a Python 3.x Anaconda environment from https://www.anaconda.com/distribution.
- Run the following to install dependencies.

```
conda create --name <environment_name>
conda activate <environment_name>
cd <project_path>/build
pip install -r requirements.txt
cd <project_path>/src
pip install -e <environment_name>/src/tweetvalidator/
```
- If you're going to be using the Twitter API, edit build/insightTwitterCreds.bat and add your credentials.
Run:
```
source insightTwitterCreds.bat
```

- **Close your terminal, open a new shell, and** `conda activate <environment_name>`

- Please keep in mind that you'll have to `conda activate <environment_name>` every time a shell launches.  If you plan on spending a lot of time working with this package, consider adding the following lines the end of your `~/.bash_profile`:

```
conda activate <environment_name>
source <project_path>/insightTwitterCreds.bat
```


## Configs
- Coming soon!

## Test
- Coming soon!

## Analysis
- Include some form of EDA (exploratory data analysis)
