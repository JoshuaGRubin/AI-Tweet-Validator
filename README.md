# Did I write this?  
Fraudulent posts on social media are embarrassing to individuals and expensive to brands.  Language embedding models offer a means to characterize typical activity for a user and can be applied in a simple binary discriminator to screen incoming content.

This repository provides a demonstration of the use of language embedding (via [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/2)) to classify new Twitter posts as in or out-of-character for a particular user.  In a production system (implemented on the platform side), a user could be presented with secondary authentication to validate activity for the occasional false positive.

https://bit.ly/didIWriteThis

## Setup

The reccomended way to run this project is by installing Docker and building and running an image.  This process manages libraries, the python runtime environment, and dependences; it also manages environment variables nicely.  This maximizes stability and portibility.

- First, visit https://www.docker.com to install the Docker platform (e.g. Docker Desktop) on your machine.

- *Optional*: while data from 13 Twitter users in included in the `data/raw` directory, if you'd like to be able to retrieve your own (e.g. more/other users, more recent tweets), you'll need to set up a Twitter developer account and app.  To do so, please visit https://developer.twitter.com, create an app, and have it approved.  Once this is complete, you'll have access to API keys.  To enable API access in this package, please uncomment the appropriate four rows in `build\Dockerfile` and paste in your credientials.

- To build and run your container, run the following in your command shell.

```bash
cd <project directory>
./build_docker
./run_docker
```

- At this point, you should be able to `cd src/cripts` and `python <script_name>` to run any of th example scripts.  You also have the library, 'tweetvalidator' (from src/tweetvalidator) availabel in you `PYTHONPATH`, so you can include it in any of your own scripts.

## Configs
- We recommond using either .yaml or .txt for your config files, not .json
- **DO NOT STORE CREDENTIALS IN THE CONFIG DIRECTORY!!**
- If credentials are needed, use environment variables or HashiCorp's [Vault](https://www.vaultproject.io/)


## Test
- Coming soon!

## Analysis
- Include some form of EDA (exploratory data analysis)
