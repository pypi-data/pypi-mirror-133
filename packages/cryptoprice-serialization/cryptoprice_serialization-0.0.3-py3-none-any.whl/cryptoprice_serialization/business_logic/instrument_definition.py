import decimal
from enum import Enum
import dataclasses
from typing import Dict


class PriceSource(Enum):
    link = 0
    tradable = 1
    pricing = 2


@dataclasses.dataclass(unsafe_hash=True, order=True)
class InstrumentDefinition:
    exchange: str
    ticker: str
    instrument_type: str
    currency: str
    _price_source: dataclasses.InitVar[str]
    is_active: bool = True

    price_source: PriceSource = None
    expiry: str = ""
    multiplier: decimal.Decimal = dataclasses.field(
        compare=False, default=decimal.Decimal("nan")
    )

    id: int = dataclasses.field(compare=False, default=0)
    tradable_id: int = dataclasses.field(compare=False, default=0)
    # id is not comparable, because for 2 instruments where all fields match except id, we want equal = true
    # reason is that 1 instrument was queried from DB, another not, and this avoids redundant DB queries

    def __post_init__(self, _price_source):
        assert (
            _price_source in PriceSource.__members__.keys()
        ), f"_price_source has to be one of {', '.join(PriceSource.__members__.keys())}"
        object.__setattr__(self, "price_source", PriceSource[_price_source])

        assert (self.is_active is None and _price_source == PriceSource.link.name) or (
            self.is_active is not None and _price_source != PriceSource.link.name
        )


@dataclasses.dataclass
class InstrumentDefinitions:
    instruments: Dict[int, InstrumentDefinition]

    def __len__(self) -> int:
        return len(self.instruments)
