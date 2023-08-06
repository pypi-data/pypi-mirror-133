# glibs-datetime-helpers

Utilties to handle `datetime` in our Python projects.

## Install

```
pip install glibs-datetime-helpers
```

## Usage

- `glibs.datetime_helpers.to_isoformat(datetime: datetime.datetime) -> str`

  Returns a datetime formatted as ISO-8601 with the Z flag automatically.

- `glibs.datetime_helpers.from_isoformat(datetime_str: str) -> datetime.datetime`

  Parse a ISO-8601 string and returns a `datetime.datetime`.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).
