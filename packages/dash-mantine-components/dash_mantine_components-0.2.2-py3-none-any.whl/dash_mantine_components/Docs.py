# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Docs(Component):
    """A Docs component.
Layout component for internal use (documentation of Dash Mantine Components).

Keyword arguments:

- children (string; optional):
    Primary content.

- data (list of dicts; optional):
    Data for sidebar and select in navbar.

    `data` is a list of dicts with keys:

    - label (string; required):
        The option's label.

    - value (string; required):
        Option's value."""
    @_explicitize_args
    def __init__(self, children=None, data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'data']
        self._type = 'Docs'
        self._namespace = 'dash_mantine_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Docs, self).__init__(children=children, **args)
