# glibs-ndb

[![CI](https://github.com/projetoeureka/glibs-ndb/actions/workflows/ci.yml/badge.svg)](https://github.com/projetoeureka/glibs-ndb/actions/workflows/ci.yml)

Very small library for parsing AppEngine keys as urlsafes when outside the
AppEngine env.

_Note:_ The code here belongs to Google and was modified to suit our needs.

## Usage

### `ndb.Key()`

There are two main usages of `ndb.Key()`: to get the ID from an urlsafe string, or to get the urlsafe string from an ID.

- `ndb.Key(urlsafe=urlsafe, app=app)`

  ```python
  from glibs import ndb

  key = ndb.Key(urlsafe="<urlsafe string>", app="<app name>")
  key.id()
  ```

- `ndb.Key(kind, id, app=app)`

  ```python
  from glibs import ndb

  key = ndb.Key("Kind", 123, app="<app name>")
  key.urlsafe()
  ```

### `ndb.ConverterHelper`

It's a convenience class to ensure you're working with an ID or an urlsafe string, in cases you might get both.

- `ensure_key(urlsafe_or_id, kind=None)` -> returns an urlsafe

  If `urlsafe_or_id` is an urlsafe string, it will only check if the kind matches (if passed).

  if `urlsafe_or_id` is an ID, then `kind` can't be `None` and it will build the Key and return its corresponding urlsafe.

  ```python
  from glibs import ndb

  helper = ndb.ConverterHelper("<app name>")

  urlsafe = helper.ensure_key(urlsafe_or_id, kind="Kind")
  ```

- `ensure_id(urlsafe_or_id)` -> returns a numerical ID (as string)

  If `urlsafe_or_id` is an urlsafe string, it will build the Key and return its id.

  if `urlsafe_or_id` is an ID, it will just cast to string (if necessary).

  ```python
  from glibs import ndb

  helper = ndb.ConverterHelper("<app name>")

  urlsafe = helper.ensure_key(urlsafe_or_id, kind="Kind")
  ```

## Contributing

Run tests with `nox`. This should run tests in multiple Python versions.
