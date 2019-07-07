# *Did I write this?!*  AI to Detect Fraudulent Tweets
Fraudulent posts on social media are embarrassing to individuals and expensive to brands.  Language embedding models offer a means to characterize typical activity for a user and can be applied in a simple binary discriminator to screen incoming content.

This repository provides a demonstration of the use of language embedding (via [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/2)) to classify new Twitter posts as in or out-of-character for a particular user.  In a production system (implemented on the platform side), a user could be presented with secondary authentication to validate activity for the occasional false positive.

Slides desribing this project can be found here:  https://bit.ly/didIWriteThis

## Setup

Clone this repo with `git clone https://github.com/JoshuaGRubin/AI-Tweet-Validator.git <project_path>` on your command line.

*Optional*: while data from 13 Twitter users in included in the `data/raw` directory, if you'd like to be able to retrieve your own (e.g. more/other users, more recent tweets), you'll need to set up a Twitter developer account and app.  To do so, please visit https://developer.twitter.com, create an app, and have it approved. Once this is complete, you'll have access to API credentials. 

### Setup with Docker – *portable and stable*
**The recommended way to run this project is by installing Docker and building and running an image**.  This process manages libraries, the python runtime environment, and dependences; it also manages environment variables nicely.  This maximizes stability and portability.

- First, visit https://www.docker.com to install the Docker platform (e.g. Docker Desktop) on your machine.

- If you've created a Twitter developer account and you'd like to download new content, uncomment the appropriate four rows in `build\Dockerfile` and paste in your credentials.

- To build and run your container, run the following in your command shell.

```bash
> cd <project_path>
> ./build_docker
> ./run_docker
```

- At this point, you should be able to `cd src/scripts` and `python <script_name>` to run any of the example scripts.  You also have the library, 'tweetvalidator' (from src/tweetvalidator) available in you `PYTHONPATH`, so you can include it in any of your own scripts.

### Setup with Anaconda – *lightweight*

While this setup has a few more steps and possibly plateform-dependent pitfalls, there's less to download and store on disk.

- Install a Python 3.x Anaconda environment from https://www.anaconda.com/distribution.
- Run the following to create a new conda/Python environment:

```bash
> conda create --name <environment_name>
> conda activate <environment_name>
> conda install pip

# Install project dependencies - includes `tweetvalidator`, the core module provided by this project.
> cd <project_path>/build
> pip install -r requirements.txt
```


- If you're going to be using the Twitter API, edit build/insightTwitterCreds.bat and add your credentials.
Run:
```
> source twitter_creds.bat.bat
```

- Please keep in mind that you'll have to `conda activate <environment_name>` every time a shell launches.  If you plan on spending a lot of time working with this package, consider adding the following lines the end of your `~/.bash_profile`:

```
> conda activate <environment_name>
> source <project_path>/twitter_creds.bat.bat
```

## Troubleshooting

- There's a occationally a problem with TensorFlow Hub that casuses the following error:

>Encoder tf-hub error:
RuntimeError: Missing implementation that supports: loader(*('/var/folders/0w/pn889r517f9220q1vl66k7_h0000gn/T/tfhub_modules/1fb57c3ffe1a38479233ee9853ddd7a8ac8a8c47',), **{})

This seeme to have something to do with the way Universal Sentence Encoder is cached.  Sometimes it's deleted, but TF Hub still thinks it's present.  If you encounter this, simply delete the directory mentioned in the error and rerun.

## Configs
`configs\config.json` allows you to cusomize a number of features of the project pipeline.  These include:

- User-list to retrieve from twitter
- Maximum-number of tweets per user
- Minumum tweet length
- Regular expressions to use in tweet filtering
- Paths to data directories


## Test
To run a set of nontrivial unit-tests on the core tweetvalidator package, navigate to the directory and run pytest:

    > cd <project_directory>/tests
    > pytest


## Analysis
- Include some form of EDA (exploratory data analysis)
