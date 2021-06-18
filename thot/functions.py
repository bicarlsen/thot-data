#!/usr/bin/env python
# coding: utf-8

# Functions

import builtins
import typing
from functools import partial


def property_filter( prop, value, obj ):
    """
    Check if object matched property filter.

    :param prop: Name of the property to check.
    :param value: Value to match.
    :param obj: LocalObject.
    :returns: True if matches, False otherwise.
    """
    # parse prop
    prop_path = prop.split( '.' )
    for part in prop_path:
        try:
            obj = obj[ part ]

        except KeyError as err:
            # property not contained in object
            return False

    if isinstance( value, list ):
        # value is list, check for inclusion
        if isinstance( obj, list ):
            # object is list, verfiy all values are in object
            for item in value:
                if isinstance( item, typing.Pattern ):
                    # value is regex
                    match = item.search( value )
                    return ( match is None )

                if item not in obj:
                    # search item not obj
                    return False

            # all items present
            return True


        else:
            # object is not list, can not match
            return False

    elif isinstance( value, dict ):
        # value is dictionary, search for operators
        for op, val in value.items():
            if op == '$in':
                # inclusion operator
                if not isinstance( val, list ):
                    raise TypeError( f'Invalid search criteria {op}: {val}. Value must be list.' )

                if not isinstance( obj, list ):
                    raise TypeError( 'Invalid search object. Must be list.' )

                # test all values are included in object
                return all( [ ( v in obj ) for v in val ] )

            else:
                # not an operator
                raise TypeError( f'Invalid search operator {op}' )

        # passed all operator checks
        return True

    else:
        # value is not list, check for direct match
        if isinstance( value, typing.Pattern ):
            # value is regex
            match = value.search( obj )
            return ( match is not None )

        # simple value
        return ( obj == value )


def filter( filter, resources ):
    """
    Filters an iterable of Assets and/or Containers.

    :param filter: Dictionary of search criteria.
    :param resources: Iterable of resources to filter.
    :returns: List of filtered resources.
    """
    matching = resources.copy()
    for prop, value in filter.items():
        obj_fltr = partial( property_filter, prop, value )
        matching = builtins.filter( obj_fltr, matching )  # builtins required because filter overwritten by parameter.

    return list( matching )
