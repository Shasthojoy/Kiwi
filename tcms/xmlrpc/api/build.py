# -*- coding: utf-8 -*-

from modernrpc.core import rpc_method

from tcms.management.models import TestBuild
from tcms.xmlrpc.decorators import permissions_required
from tcms.xmlrpc.utils import pre_check_product, parse_bool_value

__all__ = (
    'create',
    'update',
    'filter',
)


@rpc_method(name='Build.filter')
def filter(query={}):
    """
    .. function:: XML-RPC Build.filter(query)

        Search and return builds matching query.

        :param query: Field lookups for :class:`tcms.management.models.TestBuild`
        :type query: dict
        :return: List of serialized :class:`tcms.management.models.TestBuild` objects
        :rtype: list(dict)
    """
    return TestBuild.to_xmlrpc(query)


@rpc_method(name='Build.create')
@permissions_required('management.add_testbuild')
def create(values):
    """
    .. function:: XML-RPC Build.create(values)

        Create a new build object and store it in the database.

        :param values: Field values for :class:`tcms.management.models.TestBuild`
        :type values: dict
        :return: Serialized :class:`tcms.management.models.TestBuild` object
        :rtype: dict
        :raises: ValueError if product or name not specified
        :raises: PermissionDenied if missing *management.add_testbuild* permission
    """
    if not values.get('product') or not values.get('name'):
        raise ValueError('Product and name are both required.')

    p = pre_check_product(values)

    return TestBuild.objects.create(
        product=p,
        name=values['name'],
        description=values.get('description'),
        is_active=parse_bool_value(values.get('is_active', True))
    ).serialize()


@permissions_required('management.change_testbuild')
@rpc_method(name='Build.update')
def update(build_id, values):
    """
    .. function:: XML-RPC Build.update(build_id, values)

        Updates the fields of the selected build.

        :param build_id: PK of TestBuild to modify
        :type build_id: int
        :param values: Field values for :class:`tcms.management.models.TestBuild`
        :type values: dict
        :return: Serialized :class:`tcms.management.models.TestBuild` object
        :rtype: dict
        :raises: TestBuild.DoesNotExist if build not found
        :raises: PermissionDenied if missing *management.change_testbuild* permission
    """
    tb = TestBuild.objects.get(build_id=build_id)

    def _update_value(obj, name, value):
        setattr(obj, name, value)
        update_fields.append(name)

    update_fields = list()
    if values.get('product'):
        _update_value(tb, 'product', pre_check_product(values))
    if values.get('name'):
        _update_value(tb, 'name', values['name'])
    if values.get('description'):
        _update_value(tb, 'description', values['description'])
    if values.get('is_active') is not None:
        _update_value(tb, 'is_active', parse_bool_value(values.get(
            'is_active', True)))

    tb.save(update_fields=update_fields)

    return tb.serialize()
