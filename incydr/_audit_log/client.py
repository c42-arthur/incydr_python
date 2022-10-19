from datetime import datetime
from pathlib import Path
from typing import List
from typing import Union

from incydr._audit_log.models import AuditEventsPage
from incydr._audit_log.models import DateRange
from incydr._audit_log.models import QueryAuditLogRequest
from incydr._audit_log.models import QueryExportRequest
from incydr._audit_log.models import UserTypes
from incydr._core.util import get_filename_from_content_disposition


class AuditLogClient:
    def __init__(self, parent):
        self._parent = parent
        self._v1 = None

    @property
    def v1(self):
        if self._v1 is None:
            self._v1 = AuditLogV1(self._parent)
        return self._v1


class AuditLogV1:
    """
    Client for `/v1/audit` endpoints.

    Usage example:

        >>> import incydr
        >>> client = incydr.Client(**kwargs)
        >>> client.audit_log.v1.get_page()
    """

    def __init__(self, parent):
        self._parent = parent

    def get_page(
        self,
        page_num: int = 0,
        page_size: int = None,
        actor_ids: Union[List[str], str] = None,
        actor_ip_addresses: Union[List[str], str] = None,
        actor_names: Union[List[str], str] = None,
        start_time: datetime = None,
        end_time: datetime = None,
        event_types: Union[List[str], str] = None,
        resource_ids: Union[List[str], str] = None,
        user_types: Union[List[UserTypes], UserTypes] = None,
    ) -> AuditEventsPage:
        """
        Search audit log entries.

        **Parameters:**

        * **page_num**: `int` - page_num number for results, starting at 1.
        * **page_size**: `int` - Max number of results to return per page. Defaults to client's `page_size` setting.
            Maximum page size is 10,000.
        * **actor_ids**: `List[str]`, `str` - Finds events whose actor_id is one of the given ids.
        * **actor_ip_addresses**: `List[str]`, `str` - Finds events whose actor_ip_address is one of the given IP addresses.
        * **actor_names**: `List[str]`, `str` - Finds events whose actor_name is one of the given names.
        * **start_time**: `datetime` - Search for events within a date range.  Start time for this date range.
        * **end_time**: `datetime` - Search for events within a date range.  End time for this date range.
        * **event_types**: `List[str]`, `str` - Finds events whose type is one of the given types.
        * **resource_ids**: `List[str]`, `str` - Filters searchable events that match resource_id.
        * **user_types**: `List[UserTypes]` - Filters searchable events that match actor type.

        **Returns**: A [`AuditEventsPage`][auditeventspage-model] object representing the search response.
        """

        page_size = page_size or self._parent.settings.page_size

        request = _build_query_request(
            page_num=page_num,
            page_size=page_size,
            actor_ids=actor_ids,
            actor_ip_addresses=actor_ip_addresses,
            actor_names=actor_names,
            start_time=start_time,
            end_time=end_time,
            event_types=event_types,
            resource_ids=resource_ids,
            user_types=user_types,
        )

        response = self._parent.session.post(
            "/v1/audit/search-audit-log", json=request.dict()
        )

        return AuditEventsPage.parse_response(response)

    def search_events(
        self,
        actor_ids: Union[List[str], str] = None,
        actor_ip_addresses: Union[List[str], str] = None,
        actor_names: Union[List[str], str] = None,
        start_time: datetime = None,
        end_time: datetime = None,
        event_types: Union[List[str], str] = None,
        resource_ids: Union[List[str], str] = None,
        user_types: Union[List[UserTypes], UserTypes] = None,
    ) -> AuditEventsPage:
        """
        Search audit log entries, specifically for large return sets without paging.

        Returns up to 100,000 events that match the search criteria provided.

        Default: returns most recent 100,000 events.

        **Parameters:**

        * **actor_ids**: `List[str]`, `str` - Finds events whose actor_id is one of the given ids.
        * **actor_ip_addresses**: `List[str]`, `str` - Finds events whose actor_ip_address is one of the given IP addresses.
        * **actor_names**: `List[str]`, `str` - Finds events whose actor_name is one of the given names.
        * **start_time**: `datetime` - Search for events within a date range.  Start time for this date range.
        * **end_time**: `datetime` - Search for events within a date range.  End time for this date range.
        * **event_types**: `List[str]`, `str` - Finds events whose type is one of the given types.
        * **resource_ids**: `List[str]`, `str` - Filters searchable events that match resource_id.
        * **user_types**: `List[UserTypes]` - Filters searchable events that match actor type.

        **Returns**: A [`AuditEventsPage`][auditeventspage-model] object representing the search response.
        """

        request = _build_query_request(
            page_num=0,
            page_size=0,
            actor_ids=actor_ids,
            actor_ip_addresses=actor_ip_addresses,
            actor_names=actor_names,
            start_time=start_time,
            end_time=end_time,
            event_types=event_types,
            resource_ids=resource_ids,
            user_types=user_types,
        )

        response = self._parent.session.post(
            "/v1/audit/search-results-export", json=request.dict()
        )

        return AuditEventsPage.parse_response(response)

    def get_event_count(
        self,
        page_num: int = 0,
        page_size: int = None,
        actor_ids: Union[List[str], str] = None,
        actor_ip_addresses: Union[List[str], str] = None,
        actor_names: Union[List[str], str] = None,
        start_time: datetime = None,
        end_time: datetime = None,
        event_types: Union[List[str], str] = None,
        resource_ids: Union[List[str], str] = None,
        user_types: Union[List[UserTypes], UserTypes] = None,
    ) -> int:
        """
        Get the total result count of a search.

        **Parameters:**

        * **page_num**: `int` - Page number for results, starting at 1.
        * **page_size**: `int` - Max number of results to return per page.
        * **actor_ids**: `List[str]`, `str` - Finds events whose actor_id is one of the given ids.
        * **actor_ip_addresses**: `List[str]`, `str` - Finds events whose actor_ip_address is one of the given IP addresses.
        * **actor_names**: `List[str]`, `str` - Finds events whose actor_name is one of the given names.
        * **start_time**: `datetime` - Search for events within a date range.  Start time for this date range.
        * **end_time**: `datetime` - Search for events within a date range.  End time for this date range.
        * **event_types**: `List[str]`, `str` - Finds events whose type is one of the given types.
        * **resource_ids**: `List[str]`, `str` - Filters searchable events that match resource_id.
        * **user_types**: `List[UserTypes]` - Filters searchable events that match actor type.

        **Returns**: An `int` indicating the number of resulting audit log events from search.
        """

        page_size = page_size or self._parent.settings.page_size

        request = _build_query_request(
            page_num=page_num,
            page_size=page_size,
            actor_ids=actor_ids,
            actor_ip_addresses=actor_ip_addresses,
            actor_names=actor_names,
            start_time=start_time,
            end_time=end_time,
            event_types=event_types,
            resource_ids=resource_ids,
            user_types=user_types,
        )

        response = self._parent.session.post(
            "/v1/audit/search-results-count", json=request.dict()
        )

        return response.json()["totalResultCount"]

    def download_events(
        self,
        target_folder: Path,
        actor_ids: Union[List[str], str] = None,
        actor_ip_addresses: Union[List[str], str] = None,
        actor_names: Union[List[str], str] = None,
        start_time: datetime = None,
        end_time: datetime = None,
        event_types: Union[List[str], str] = None,
        resource_ids: Union[List[str], str] = None,
        user_types: Union[List[UserTypes], UserTypes] = None,
    ) -> Path:
        """
        Export search results.

        **Parameters:**

        * **target_folder**: `Path, str` - A string or `pathlib.Path` object that represents the folder
        which the file will be saved to.
        * **actor_ids**: `List[str]`, `str` - Finds events whose actor_id is one of the given ids.
        * **actor_ip_addresses**: `List[str]`, `str` - Finds events whose actor_ip_address is one of the given IP addresses.
        * **actor_names**: `List[str]`, `str` - Finds events whose actor_name is one of the given names.
        * **start_time**: `datetime` - Search for events within a date range.  Start time for this date range.
        * **end_time**: `datetime` - Search for events within a date range.  End time for this date range.
        * **event_types**: `List[str]`, `str` - Finds events whose type is one of the given types.
        * **resource_ids**: `List[str]`, `str` - Filters searchable events that match resource_id.
        * **user_types**: `List[UserTypes]` - Filters searchable events that match actor type.

        **Returns**: A `pathlib.Path` object representing location of the downloaded csv file.
        """

        date_range = DateRange()
        if start_time:
            date_range.startTime = start_time.timestamp()
        if end_time:
            date_range.endTime = end_time.timestamp()

        data = QueryExportRequest(
            actorIds=[actor_ids] if isinstance(actor_ids, str) else actor_ids,
            actorIpAddresses=[actor_ip_addresses]
            if isinstance(actor_ip_addresses, str)
            else actor_ip_addresses,
            actorNames=[actor_names] if isinstance(actor_names, str) else actor_names,
            dateRange=date_range,
            eventTypes=[event_types] if isinstance(event_types, str) else event_types,
            resourceIds=[resource_ids]
            if isinstance(resource_ids, str)
            else resource_ids,
            userTypes=[user_types] if isinstance(user_types, str) else user_types,
        )

        folder = Path(target_folder)  # ensure a Path object if we get passed a string
        if not folder.is_dir():
            raise ValueError(
                f"`target_folder` argument must resolve to a folder: {target_folder}"
            )

        export_response = self._parent.session.post(
            "/v1/audit/export", json=data.dict()
        )

        download_response = self._parent.session.get(
            f"/v1/audit/redeemDownloadToken?downloadToken={export_response.json()['downloadToken']}"
        )

        filename = get_filename_from_content_disposition(
            download_response, fallback="AuditLog_SearchResults.csv"
        )
        target = folder / filename
        target.write_bytes(download_response.content)

        return target


def _build_query_request(
    page_num: int = 0,
    page_size: int = 100,
    actor_ids: Union[List[str], str] = None,
    actor_ip_addresses: Union[List[str], str] = None,
    actor_names: Union[List[str], str] = None,
    start_time: datetime = None,
    end_time: datetime = None,
    event_types: Union[List[str], str] = None,
    resource_ids: Union[List[str], str] = None,
    user_types: Union[List[UserTypes], UserTypes] = None,
):
    date_range = DateRange()
    if start_time:
        date_range.startTime = start_time.timestamp()
    if end_time:
        date_range.endTime = end_time.timestamp()

    request = QueryAuditLogRequest(
        actorIds=[actor_ids] if isinstance(actor_ids, str) else actor_ids,
        actorIpAddresses=[actor_ip_addresses]
        if isinstance(actor_ip_addresses, str)
        else actor_ip_addresses,
        actorNames=[actor_names] if isinstance(actor_names, str) else actor_names,
        dateRange=date_range,
        eventTypes=[event_types] if isinstance(event_types, str) else event_types,
        pageNum=page_num,
        pageSize=page_size,
        resourceIds=[resource_ids] if isinstance(resource_ids, str) else resource_ids,
        userTypes=[user_types] if isinstance(user_types, str) else user_types,
    )

    return request
