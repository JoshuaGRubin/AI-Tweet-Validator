
import os
import json
import pytest
import pandas as pd
from tweetvalidator.data_processing import embed_tweets_from_directories
from get_config import get_config

INPUT_DIR_KEY = 'preprocessed_data_path'
EXPECTED_OUTPUT_COLUMNS = 3

# Set up a temp output directory and embed
@pytest.fixture(scope='module')
def temp_output_dir(tmpdir_factory):
    config = get_config()
    tmpdir = tmpdir_factory.mktemp('output')
    embed_tweets_from_directories(config[INPUT_DIR_KEY], tmpdir)
    return tmpdir

# Make sure there's an input file for every output file.
def test_makes_all_files(temp_output_dir):
    input_directory = get_config()[INPUT_DIR_KEY]

    infiles = [x for x in os.listdir(input_directory) if x[0]=='@']
    outfiles = os.listdir(temp_output_dir)

    assert(len(infiles)==len(outfiles))

# Make sure that all output files have the right structure.
def test_file_structure(temp_output_dir):
    output_paths = [os.path.join(temp_output_dir, x)
                         for x in os.listdir(temp_output_dir) if x[0]=='@']

    for file_path in output_paths:
        print(file_path)
        with open(file_path, 'r') as file:
          in_data =  json.loads(file.read())
    
        df = pd.DataFrame(in_data) 

        assert(df.shape[1]==EXPECTED_OUTPUT_COLUMNS)
