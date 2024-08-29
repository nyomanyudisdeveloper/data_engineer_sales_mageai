import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def convert_sales_date(order_id,df):
        return  df[df['order_id'] == order_id]['sales_date'].iloc[0]


@transformer
def transform(data_csv,data_mongodb,data_api, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = pd.concat([data_csv,data_mongodb])

    df[['order_id','menu_id','promotion_id','id']] = df[['order_id','menu_id','promotion_id','id']].astype('object')
    df[['brand','name']] = df[['brand','name']].astype('string')
    df[['quantity']] = df[['quantity']].astype('int')
    df[['disc_value','max_disc','price','cogs']] = df[['disc_value','max_disc','price','cogs']].astype('float')
    df['sales_date'] = pd.to_datetime(df['sales_date']).dt.date
    df['start_date'] = pd.to_datetime(df['start_date']).dt.date
    df['end_date'] = pd.to_datetime(df['end_date']).dt.date
    df['effective_date'] = pd.to_datetime(df['effective_date']).dt.date
    
    df.loc[df['disc_value'] > 0.8,'disc_value'] = 0.8
    
    df_filter_sales_date_based_order_id =  df.groupby(['order_id']).agg({'sales_date':'min'}).reset_index()
    
    df['sales_date'] =  df.apply(lambda row: convert_sales_date(row.order_id,df_filter_sales_date_based_order_id),axis=1)
    
    column = df.columns.to_list()
    column.remove("quantity")
    df_group_qty = df.groupby(column).agg({'quantity':'sum'}).reset_index()
    
    return df_group_qty


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
