import datetime
import dataclasses
import numpy as np
from typing import Tuple

import cryptoprice_serialization.business_logic.instrument_definition


@dataclasses.dataclass
class Price:
    bid: float = np.nan
    ask: float = np.nan
    _instrument_id: int = 0
    instrument: cryptoprice_serialization.business_logic.instrument_definition.InstrumentDefinition = None

    def __post_init__(self):
        if self._instrument_id == 0 and self.instrument is None:
            raise Exception("need to define one of _instrument_id or instrument")

    @property
    def instrument_id(self):
        if self._instrument_id == 0:
            return self.instrument.id
        return self._instrument_id


@dataclasses.dataclass
class Prices:
    date: datetime.datetime
    prices: Tuple[Price]


@dataclasses.dataclass(frozen=True)
class TimeSeries:
    instruments: cryptoprice_serialization.business_logic.instrument_definition.InstrumentDefinitions
    # instruments is a Dict mapping Price.instrument_id to InstrumentDefinition
    # if not present (due to size efficiency)

    dates: Tuple[Prices]
