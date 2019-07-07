
import os
import json
import pandas as pd
from get_config import get_config
from sklearn.model_selection import train_test_split

from tweetvalidator.models import ClusteredCosSimModel

INPUT_DIR_KEY = 'processed_data_path'

# Make sure we can characterize and that we get a sim-score for each embedding
# in our test set.
def test_model():
    input_directory = get_config()[INPUT_DIR_KEY]

    infiles = [x for x in os.listdir(input_directory) if x[0]=='@']

    test_file_path = os.path.join(input_directory, infiles[0])

    with open(test_file_path, 'r') as file:
        in_data =  json.loads(file.read())

    df = pd.DataFrame(in_data, columns = ['tweet','date','embedding'])

    train, test =  train_test_split(df['embedding'],
                                    test_size = 0.4, random_state = 1)

    model = ClusteredCosSimModel()

    model.characterize(train, None)

    sim_scores = model.similarity_score(test)

    assert(len(test)==len(sim_scores))
