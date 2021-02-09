
from orthogonal import orthogonal_arrays
import pandas as pd
def get_oa(
    input_file, sheet_name, blocks=None, block_check=None, verbose=False,
    *args, **kwargs
):
    
    # without blocks
    frame = pd.read_excel(input_file, sheet_name=sheet_name)
    factors = {
        name: list(frame[name].dropna())
        for name in frame.columns

    }
    if blocks is not None:
        factors.update({'block': range(1, blocks+1)})
        
    oa = orthogonal_arrays.orthogonal_array(factors, verbose=verbose)
    if blocks is not None:
        oa = oa.sort_values('block').reset_index(drop=True)
    oa['index'] = range(1, len(oa)+1)
    if blocks is not None and block_check is not None:
        oa = pd.merge(oa, block_check, on='block', how='left')
    return oa

def write_oa(output_file, sheet_name, *args, **kwargs):
    oa = get_oa(sheet_name, *args, **kwargs)

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        writer.book = book
        oa.to_excel(writer, sheet_name='oa_' + sheet_name, index=False)
        writer.save()