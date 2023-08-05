[0.1.0a]

- core functionalities, including build and batch methods

[0.2.0a]

- handling of all pydantic constraint

[0.3.0b]

- full features MvP

[0.3.1b]

- fix issues with decimal parsing

[0.3.2b]

- removed support for python 3.6
- added beanie extension

[0.3.3b]

- resolve TypeError being raised from issubclass() for python 3.9+

[0.3.4b]

- add support for forward refs
- add support for ODMantic
- add Ignore and Require fields

[0.3.5b]

- update readme
- update fields

[0.4.0]

- added support for dataclasses

[0.4.1]

- randomly return None values for Optional[] marked fields

[0.4.2]

- updated handling of dataclasses to support randomized optionals

[0.4.3]

- fixed `py.typed` not placed inside the package

[0.4.4]

- make exports explicit

[0.4.5]

- fix generation of enum in complex types

[0.4.6]

- fix generation of nested constrained fields

[0.5.0]

- add ormar extension


[0.6.0]

- added `__allow_none_optionals__` factory class variable
- updated the `ModelFactory.create_factory` method to accept an optional `base` kwarg user defined **kwargs
- added a new method on `ModelFactory` called `should_set_none_value`, which dictates whether a None value should be set for a given `ModelField`
- updated dependencies


[0.6.1]

- fix bug were nested optionals did not factor in `__allow_none_optionals__` settings


[0.6.2]

- fix bug with Literal[] values not being recognized


[0.6.3]

- fix backwards compatible import


[0.7.0]

- added support for `factory_use_construct` kwargs, thanks - @danielkatzan


[0.8.0]

- added random configuration. Thanks to @eviltnan
