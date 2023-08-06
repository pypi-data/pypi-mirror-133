import struct
import io
import decimal
import datetime

import cryptoprice_serialization.business_logic.instrument_definition
import cryptoprice_serialization.business_logic.prices
import cryptoprice_serialization.serializer.serialization.message_pb2 as message_pb

def _deserialize_exception(data):
    return Exception(data.reason)


def _deserialize_prices(data):
    prices = [
        cryptoprice_serialization.business_logic.prices.Price(
            _instrument_id=i.instrument_id, bid=i.bid, ask=i.ask
        )
        for i in data.prices
    ]
    date = data.date.ToDatetime().replace(tzinfo=datetime.timezone.utc)
    return cryptoprice_serialization.business_logic.prices.Prices(date=date, prices=tuple(prices))


def _deserialize_instruments(data):
    instruments = {
        i.id: cryptoprice_serialization.business_logic.instrument_definition.InstrumentDefinition(
            exchange=i.exchange,
            ticker=i.ticker,
            instrument_type=i.instrument_type,
            currency=i.currency,
            _price_source=i.price_source,
            expiry=i.expiry,
            multiplier=decimal.Decimal(i.multiplier),
            id=i.id,
            tradable_id=i.tradable_id,
            trading_exchange=i.trading_exchange
            if i.HasField("trading_exchange")
            else None,
            is_active=i.is_active if i.HasField("is_active") else None,
        )
        for i in data.instruments
    }
    return cryptoprice_serialization.business_logic.instrument_definition.InstrumentDefinitions(instruments)


def _deserialize_datetime(data):
    return data.datetime.ToDatetime().replace(tzinfo=datetime.timezone.utc)


def deserialize_message(obj: message_pb.Message):
    with io.BytesIO(initial_bytes=obj) as reader:
        for item in deserialize_with_length(reader, message_pb.Message):
            if not item:
                return

            msg_type = item.WhichOneof("message")
            data = getattr(item, msg_type)
            if msg_type == "instruments":
                yield _deserialize_instruments(data)
            elif msg_type == "prices":
                yield _deserialize_prices(data)
            elif msg_type == "exception":
                yield _deserialize_exception(data)
            elif msg_type == "datetime":
                yield _deserialize_datetime(data)
            else:
                raise Exception("undefined message type for deserialization")


def serialize_message(obj):
    m = message_pb.Message()
    if isinstance(obj, cryptoprice_serialization.business_logic.instrument_definition.InstrumentDefinitions):
        m.instruments.CopyFrom(_serialize_instrument_def(obj))
    elif isinstance(obj, cryptoprice_serialization.business_logic.prices.Prices):
        m.prices.CopyFrom(_serialize_prices(obj))
    elif isinstance(obj, Exception):
        m.exception.CopyFrom(_serialize_exception(obj))
    elif isinstance(obj, datetime.datetime):
        m.datetime.CopyFrom(_serialize_datetime(obj))
    elif isinstance(obj, message_pb.Prices):
        m.prices.CopyFrom(obj)
    else:
        raise Exception("undefined message type for serialization")

    return serialize_with_length(m.SerializeToString())


def _serialize_datetime(obj):
    serializer = message_pb.Datetime()
    serializer.datetime.FromDatetime(obj)
    return serializer


def _serialize_prices(obj):
    serializer = message_pb.Prices()
    serializer.date.FromDatetime(obj.date)
    for p in obj.prices:
        price = serializer.prices.add()
        price.instrument_id = p.instrument_id
        price.bid = p.bid
        price.ask = p.ask
    return serializer


def _serialize_instrument_def(obj):
    serializer = message_pb.InstrumentDefinitions()
    for i in obj.instruments.values():
        instrument = serializer.instruments.add()
        instrument.id = i.id
        instrument.tradable_id = i.tradable_id
        instrument.ticker = i.ticker
        instrument.exchange = i.exchange

        if i.trading_exchange is not None:
            instrument.trading_exchange = i.trading_exchange

        if i.is_active is not None:
            instrument.is_active = i.is_active

        instrument.instrument_type = i.instrument_type
        instrument.currency = i.currency
        instrument.price_source = i.price_source.name
        instrument.expiry = i.expiry
        instrument.multiplier = i.multiplier
    return serializer


def _serialize_exception(obj):
    message = getattr(obj, "message", str(obj))
    serializer = message_pb.Exception()
    serializer.reason = message
    return serializer


def deserialize_with_length(reader: io.BytesIO, pb_type):
    while True:
        msg_len_bytes = reader.read(4)

        # EOF
        if len(msg_len_bytes) == 0:
            return

        msg_len = struct.unpack(">L", msg_len_bytes)[0]

        pb_string = reader.read(msg_len)

        if len(pb_string) == 0:
            return

        pb = pb_type()
        pb.ParseFromString(pb_string)
        yield pb


def serialize_with_length(data: str):
    with io.BytesIO() as writer:
        _serialize_with_length(writer, data)
        return writer.getvalue()


def _serialize_with_length(writer: io.BytesIO, data):
    len_bytes = struct.pack(">L", len(data))
    writer.write(len_bytes + data)
