from mage_ai.io.file import FileIO
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    For multiple directories, use the following:
        FileIO().load(file_directories=['dir_1', 'dir_2'])

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    df_menu = pd.read_csv("dataset/menu.csv")
    df_order = pd.read_csv("dataset/order.csv")
    df_promotion = pd.read_csv("dataset/promotion.csv")
    # filepath = 'path/to/your/file.csv'

    return df_order.merge(df_menu,on='menu_id')


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
