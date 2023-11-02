
import dataset

# Connect to data.db
db = dataset.connect('sqlite:///data.db')

runs_table = db['runs']


def save_run(run):
    runs_table.insert(run)
