import pandas as pd
import tidyms as ms
from pathlib import Path

def data_container_from_csv(path):
    path = Path(path)        
    sm = pd.read_csv(path.joinpath("sample-metadata.csv"), index_col=0)
    dm = pd.read_csv(path.joinpath("data-matrix.csv"), index_col=0)
    fm = pd.read_csv(path.joinpath("feature-metadata.csv"), index_col=0)
    return ms.DataContainer(dm, fm, sm)


def data_container_to_csv(dc, path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    dm_path = path.joinpath("data-matrix.csv")
    sm_path = path.joinpath("sample-metadata.csv")
    fm_path = path.joinpath("feature-metadata.csv")
    dc.data_matrix.to_csv(dm_path)
    dc.sample_metadata.to_csv(sm_path)
    dc.feature_metadata.to_csv(fm_path)
    