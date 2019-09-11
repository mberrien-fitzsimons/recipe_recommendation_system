import pandas as pd

def combine_instacart_kaggle_datasets(aisles, departments, order, order_products__prior, products):
    '''
    Combines all documents used from the kaggle dataset.
    '''
    prod_ailes = products.merge(aisles,
                  how='outer',
                  on='aisle_id',
                  suffixes=('_x', '_y'))

    product_dataset = prod_ailes.merge(departments,
                    how='outer',
                    on='department_id')

    orders_full = order_products__prior.merge(order,
                             how='left',
                             on='order_id')

    ret = orders_full.merge(product_dataset,
                           how='left',
                           on='product_id')

    return ret
