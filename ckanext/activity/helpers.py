# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Any, Optional, cast

import jinja2
import datetime
from markupsafe import Markup

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.lib.helpers import helper_functions as h

from ckan.types import Context
from . import changes


def dashboard_activity_stream(
    user_id: str,
    filter_type: Optional[str] = None,
    filter_id: Optional[str] = None,
    offset: int = 0,
    limit: int = 0,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
) -> list[dict[str, Any]]:
    """Return the dashboard activity stream of the current user.

    :param user_id: the id of the user
    :type user_id: string

    :param filter_type: the type of thing to filter by
    :type filter_type: string

    :param filter_id: the id of item to filter by
    :type filter_id: string

    :returns: an activity stream as an HTML snippet
    :rtype: string

    """
    context = cast(Context, {"user": tk.g.user})
    if filter_type:
        action_functions = {
            "dataset": "package_activity_list",
            "user": "user_activity_list",
            "group": "group_activity_list",
            "organization": "organization_activity_list",
        }
        action_function = tk.get_action(action_functions[filter_type])
        return action_function(
            context, {
                "id": filter_id,
                "limit": limit,
                "offset": offset,
                "before": before,
                "after": after
                })
    else:
        return tk.get_action("dashboard_activity_list")(
            context, {
                "offset": offset,
                "limit": limit,
                "before": before,
                "after": after
                }
        )


def recently_changed_packages_activity_stream(
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    if limit:
        data_dict = {"limit": limit}
    else:
        data_dict = {}
    context = cast(
        Context, {"model": model, "session": model.Session, "user": tk.g.user}
    )
    return tk.get_action("recently_changed_packages_activity_list")(
        context, data_dict
    )


def new_activities() -> Optional[int]:
    """Return the number of activities for the current user.

    See :func:`logic.action.get.dashboard_new_activities_count` for more
    details.

    """
    if not tk.g.userobj:
        return None
    action = tk.get_action("dashboard_new_activities_count")
    return action({}, {})


def activity_list_select(
    pkg_activity_list: list[dict[str, Any]], current_activity_id: str
) -> list[Markup]:
    """
    Builds an HTML formatted list of options for the select lists
    on the "Changes" summary page.
    """
    select_list = []
    template = jinja2.Template(
        '<option value="{{activity_id}}" {{selected}}>{{timestamp}}</option>',
        autoescape=True,
    )
    for activity in pkg_activity_list:
        entry = tk.h.render_datetime(
            activity["timestamp"], with_hours=True, with_seconds=True
        )
        select_list.append(
            Markup(
                template.render(
                    activity_id=activity["id"],
                    timestamp=entry,
                    selected="selected"
                    if activity["id"] == current_activity_id
                    else "",
                )
            )
        )

    return select_list


def compare_pkg_dicts(
    old: dict[str, Any], new: dict[str, Any], old_activity_id: str
) -> list[dict[str, Any]]:
    """
    Takes two package dictionaries that represent consecutive versions of
    the same dataset and returns a list of detailed & formatted summaries of
    the changes between the two versions. old and new are the two package
    dictionaries. The function assumes that both dictionaries will have
    all of the default package dictionary keys, and also checks for fields
    added by extensions and extra fields added by the user in the web
    interface.

    Returns a list of dictionaries, each of which corresponds to a change
    to the dataset made in this revision. The dictionaries each contain a
    string indicating the type of change made as well as other data necessary
    to form a detailed summary of the change.
    """

    change_list: list[dict[str, Any]] = []

    changes.check_metadata_changes(change_list, old, new)

    changes.check_resource_changes(change_list, old, new, old_activity_id)

    # if the dataset was updated but none of the fields we check were changed,
    # display a message stating that
    if len(change_list) == 0:
        change_list.append({"type": "no_change"})
    
    change_list = h.update_activity_keys(change_list)
    
    return change_list


def compare_group_dicts(
    old: dict[str, Any], new: dict[str, Any], old_activity_id: str
):
    """
    Takes two package dictionaries that represent consecutive versions of
    the same organization and returns a list of detailed & formatted summaries
    of the changes between the two versions. old and new are the two package
    dictionaries. The function assumes that both dictionaries will have
    all of the default package dictionary keys, and also checks for fields
    added by extensions and extra fields added by the user in the web
    interface.

    Returns a list of dictionaries, each of which corresponds to a change
    to the dataset made in this revision. The dictionaries each contain a
    string indicating the type of change made as well as other data necessary
    to form a detailed summary of the change.
    """
    change_list: list[dict[str, Any]] = []

    changes.check_metadata_org_changes(change_list, old, new)

    # if the organization was updated but none of the fields we check
    # were changed, display a message stating that
    if len(change_list) == 0:
        change_list.append({"type": "no_change"})

    return change_list


def activity_show_email_notifications() -> bool:
    return tk.config.get("ckan.activity_streams_email_notifications")


def convert_activity_stream_for_display_names(activity_stream):
    display_names_dict = {}
    for activity in activity_stream:
        if 'group' in activity.get('data', {}):
            group_dict = activity['data']['group']
            group_id = group_dict.get('id', '')

            if group_id not in display_names_dict:
                group_obj = model.Group.get(group_id)
                display_name = group_obj.title
                if h.lang() == 'ar':
                    title_arabic = group_obj.extras.get('title_arabic', '')
                    display_name = title_arabic or display_name 
                display_names_dict[group_id] = display_name
            
            group_dict['display_name'] = display_names_dict[group_id]


        if 'organization' in activity.get('data', {}):
            group_dict = activity['data']['organization']
            group_id = group_dict.get('id', '')

            if group_id not in display_names_dict:
                group_obj = model.Group.get(group_id)
                display_name = group_obj.title
                if h.lang() == 'ar':
                    title_arabic = group_obj.extras.get('title_arabic', '')
                    display_name = title_arabic or display_name 
                display_names_dict[group_id] = display_name
            
            group_dict['display_name'] = display_names_dict[group_id]

        package_dict = activity.get('data', {}).get('package')
        if isinstance(package_dict, dict):
            organization_dict = package_dict.get('organization') or {}
            org_id = organization_dict.get('id') or package_dict.get('owner_org')

            if org_id and org_id not in display_names_dict:
                group_obj = model.Group.get(org_id)
                if group_obj:
                    display_name = group_obj.title
                    if h.lang() == 'ar':
                        title_arabic = group_obj.extras.get('title_arabic', '')
                        display_name = title_arabic or display_name
                    display_names_dict[org_id] = display_name

            if organization_dict and org_id in display_names_dict:
                organization_dict['display_name'] = display_names_dict[org_id]
            elif org_id in display_names_dict:
                package_dict['organization'] = {
                    'id': org_id,
                    'display_name': display_names_dict[org_id],
                }
    return activity_stream


def _extras_to_dict(extras: Any) -> dict[str, Any]:
    if isinstance(extras, dict):
        return extras
    if isinstance(extras, list):
        result: dict[str, Any] = {}
        for item in extras:
            if isinstance(item, dict):
                key = item.get('key')
                value = item.get('value')
                if key:
                    result[key] = value
        return result
    return {}


def _group_display_name_from_obj(group_obj: Optional[model.Group]) -> Optional[str]:
    if not group_obj:
        return None

    display_name = group_obj.title or group_obj.name
    if h.lang() == 'ar':
        extras_dict = getattr(group_obj, 'extras', {}) or {}
        if isinstance(extras_dict, dict):
            title_arabic = extras_dict.get('title_arabic') or extras_dict.get('title_ar')
        else:
            title_arabic = None
        if title_arabic:
            display_name = title_arabic
    return display_name


def _group_display_name_from_dict(group_dict: dict[str, Any]) -> Optional[str]:
    if not group_dict:
        return None

    display_name = group_dict.get('display_name') or group_dict.get('title') or group_dict.get('name')

    if h.lang() == 'ar':
        for key in ('title_arabic', 'title_ar', 'display_name_ar', 'name_ar'):
            title_arabic = group_dict.get(key)
            if title_arabic:
                display_name = title_arabic
                break
        else:
            extras_dict = _extras_to_dict(group_dict.get('extras'))
            title_arabic = extras_dict.get('title_arabic') or extras_dict.get('title_ar')
            if title_arabic:
                display_name = title_arabic
    return display_name


def _activity_get(activity: Any, key: str, default: Any = None) -> Any:
    if isinstance(activity, dict):
        return activity.get(key, default)
    return getattr(activity, key, default)


def get_activity_actor_display_name(activity: Any) -> str:
    activity_data = _activity_get(activity, 'data') or {}

    package_dict = activity_data.get('package') or {}
    if isinstance(package_dict, dict):
        organization_dict = package_dict.get('organization') or {}
        if organization_dict:
            display_name = _group_display_name_from_dict(organization_dict)
            if display_name:
                url = h.url_for("organization.read", id=organization_dict.get('id'))
                return f'<a href="{url}">{display_name}</a>'

        owner_org_id = package_dict.get('owner_org')
        if owner_org_id:
            display_name = _group_display_name_from_obj(model.Group.get(owner_org_id))
            if display_name:
                return '<a href="/organization/{}">{}</a>'.format(object_id, display_name)

    organization_dict = activity_data.get('organization') or {}
    if organization_dict:
        display_name = _group_display_name_from_dict(organization_dict)
        if display_name:
            return '<a href="/organization/{}">{}</a>'.format(object_id, display_name)

    group_dict = activity_data.get('group') or {}
    if group_dict:
        display_name = _group_display_name_from_dict(group_dict)
        if display_name:
            return '<a href="/group/{}">{}</a>'.format(group_dict.get('id'), display_name)

    object_id = _activity_get(activity, 'object_id')
    if object_id:
        display_name = _group_display_name_from_obj(model.Group.get(object_id))
        if display_name:
            return '<a href="/group/{}">{}</a>'.format(object_id, display_name)

    
    return tk.h.linked_user(activity.get('user_id')) or tk._('Unknown actor')