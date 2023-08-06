import datetime
from typing import TYPE_CHECKING, List, Optional, Union, cast

import pandas as pd

from infima_client.core.types import Unset

from .utils import (
    ResponseMapping,
    frame_chunker,
    handle_factor_date_range,
    response_mapping_to_frame,
)

if TYPE_CHECKING:
    from infima_client.client import InfimaClient


@frame_chunker("cusips")
def get_pool_actuals(
    *,
    client: "InfimaClient",
    cusips: List[str],
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    col: Optional[str] = "cpr",
    wide: bool = True,
) -> Optional[pd.DataFrame]:
    resp = client.api.pool_v1.get_actual_prepayments(
        cusips=cusips, factor_date_range=handle_factor_date_range(start, end)
    )
    mapping = cast(Union[ResponseMapping, Unset], resp.prepayments)
    if isinstance(mapping, Unset):
        return None
    else:
        record_path = ["values"]
        meta = ["symbol"]
        index_cols = ["symbol", "factor_date"]
        wide_on = "factor_date" if wide else None

        return response_mapping_to_frame(
            mapping, record_path, meta, index_cols, col=col, wide_on=wide_on
        )


@frame_chunker("cohorts")
def get_cohort_actuals(
    *,
    client: "InfimaClient",
    cohorts: List[str],
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    col: Optional[str] = "cpr",
    wide: bool = True,
) -> Optional[pd.DataFrame]:
    resp = client.api.cohort_v1.get_actual_prepayments(
        cohorts=cohorts, factor_date_range=handle_factor_date_range(start, end)
    )
    mapping = cast(Union[ResponseMapping, Unset], resp.prepayments)
    if isinstance(mapping, Unset):
        return None
    else:

        record_path = ["values"]
        meta = ["symbol"]
        index_cols = ["symbol", "factor_date"]
        wide_on = "factor_date" if wide else None

        return response_mapping_to_frame(
            mapping, record_path, meta, index_cols, col=col, wide_on=wide_on
        )
