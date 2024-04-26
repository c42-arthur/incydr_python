import itertools
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from _incydr_sdk.enums import SortDirection
from _incydr_sdk.enums.sessions import ContentInspectionStatuses
from _incydr_sdk.enums.sessions import SessionStates
from _incydr_sdk.enums.sessions import SortKeys
from _incydr_sdk.queries.utils import parse_ts_to_posix_ts
from _incydr_sdk.sessions.models.models import SessionsChangeStateRequest
from _incydr_sdk.sessions.models.models import SessionsCriteriaRequest
from _incydr_sdk.sessions.models.models import SessionsQueryRequest
from _incydr_sdk.sessions.models.response import Session
from _incydr_sdk.sessions.models.response import SessionEvents
from _incydr_sdk.sessions.models.response import SessionsPage


class SessionsV1:
    """
    Client for `/v1/sessions` endpoints.

    Usage example:

        >>> import incydr
        >>> from incydr.enums.items import SessionStates
        >>> client = incydr.Client(**kwargs)
        >>> client.items.v1.change_state("<session_id>", SessionStates.CLOSED)
    """

    def __init__(self, parent):
        self._parent = parent

    def get_page(
        self,
        actor_id: str = None,
        start_time: Union[str, datetime, int] = None,
        end_time: Union[str, datetime, int] = None,
        has_alerts: bool = True,
        sort_key: Optional[SortKeys] = None,
        risk_indicators: List[str] = None,
        sort_dir: Optional[SortDirection] = None,
        states: List[SessionStates] = None,
        severities: Union[List[int], int] = None,
        rule_ids: Union[List[str], str] = None,
        watchlist_ids: Union[List[str], str] = None,
        page_num: int = 0,
        page_size: int = 50,
        content_inspection_status: Optional[ContentInspectionStatuses] = None,
    ):
        """
        Get a page of items.

        Filter results by passing the appropriate parameters.

        **Parameters**:

        * **actor_id**: `str | None` - Only include items generated by this actor.
        * **start_time**: `datetime | str | int | None` - Only include items beginning on or after this date and time.  Can be a date-formatted string, a `datetime` instance, or a POSIX `int` timestamp.
        * **end_time**: `datetime | str | int | None` - Only include items beginning before this date and time.  Can be a date-formatted string, a `datetime` instance, or a POSIX `int` timestamp.
        * **has_alerts**: `bool` - Only include items that have a matching alert status. Defaults to `True`.
        * **sort_key**: [`SortKeys`][items-sort-keys] - `end_time` or `score`. Value on which the results will be sorted. Defaults to `end time`.
        * **risk_indicators**: `List[str] | None` - List of risk indicator IDs that must be present on the items before they are returned.
        * **sort_dir**: `SortDirection` - `asc` for ascending or `desc` for descending. The direction in which to sort the response based on the corresponding key. Defaults to `desc`.
        * **states**: List[[`SessionStates`][items-session-states]] - Optional list of one or more session states to filter upon. Only include items that include these matching states.
        * **severities**: `List[int] | None` - Only include items that have the matching severity value(s). 0 = no risk, 1 = low, 2 = moderate, 3 = high, 4 = critical
        * **rule_ids**: `List[str] | None` - Optional list of one or more rule ids to filter upon.
        * **watchlist_ids**: `List[str] | None` - Optional list of one or more watchlist ids to filter upon.
        * **page_num**: `int` - Page number for results, starting at 0.
        * **page_size**: `int` - Max number of results to return per page, between 1 and 50 inclusive. Defaults to 50.
        * **content_inspection_status**: `List[[ContentInspectionStatuses][items-content-inspection-statuses]] | None` - The content inspection status(es) to limit the search to.

        **Returns**: A [`SessionsPage`][sessionspage-model] object.
        """

        # Parse timestamps
        if start_time and not isinstance(start_time, (int, float)):
            start_time = parse_ts_to_posix_ts(start_time)
        if end_time and not isinstance(end_time, (int, float)):
            end_time = parse_ts_to_posix_ts(end_time)

        if states and not isinstance(states, List):
            states = [states]
        if rule_ids and not isinstance(rule_ids, List):
            rule_ids = [rule_ids]
        if watchlist_ids and not isinstance(watchlist_ids, List):
            watchlist_ids = [watchlist_ids]
        if severities and not isinstance(severities, List):
            severities = [severities]

        data = SessionsQueryRequest(
            actor_id=actor_id,
            on_or_after=start_time,
            before=end_time,
            has_alerts=str(has_alerts).lower() if has_alerts is not None else None,
            order_by=sort_key,
            risk_indicators=risk_indicators,
            sort_direction=sort_dir,
            state=states,
            severity=severities,
            rule_id=rule_ids,
            watchlist_id=watchlist_ids,
            page_number=page_num,
            page_size=page_size,
            content_inspection_status=content_inspection_status,
        )
        response = self._parent.session.get("/v1/sessions", params=data.dict())
        return SessionsPage.parse_response(response)

    def iter_all(
        self,
        actor_id: str = None,
        start_time: Union[str, datetime, int] = None,
        end_time: Union[str, datetime, int] = None,
        has_alerts: bool = True,
        sort_key: Optional[SortKeys] = None,
        risk_indicators: List[str] = None,
        sort_dir: Optional[SortDirection] = None,
        states: List[SessionStates] = None,
        severities: List[int] = None,
        rule_ids: List[str] = None,
        watchlist_ids: List[str] = None,
        page_size: int = 50,
        content_inspection_status: Optional[ContentInspectionStatuses] = None,
    ):
        """
        Iterate over all items.

        Accepts the same parameters as `.get_page()` excepting `page_num`.

        **Returns**: A generator yielding individual [`Session`][session-model] objects.
        """
        print(watchlist_ids)
        for page_num in itertools.count(0):
            page = self.get_page(
                actor_id=actor_id,
                start_time=start_time,
                end_time=end_time,
                has_alerts=has_alerts,
                sort_key=sort_key,
                risk_indicators=risk_indicators,
                sort_dir=sort_dir,
                states=states,
                severities=severities,
                rule_ids=rule_ids,
                watchlist_ids=watchlist_ids,
                page_num=page_num,
                page_size=page_size,
                content_inspection_status=content_inspection_status,
            )
            yield from page.items
            if len(page.items) < page_size:
                break

    def get_session_details(self, session_id: str):
        """
        Get details of a session.

        **Parameters**:

        * **session_id**: `str` (required) - The session ID.

        **Returns**: A [`Session`][session-model] object representing the session.
        """
        response = self._parent.session.get(f"/v1/sessions/{session_id}")
        return Session.parse_response(response)

    def get_session_events(self, session_id: str):
        """
        Gets details for the events associated with alerted-on session activity.

        Returns the same response object as the file event client search method.

        **Parameters**:

        * **session_id**: `str` (required) - The session ID.

        **Returns**: A [`FileEventsPage`][fileeventspage-model] object.
        """
        response = self._parent.session.get(f"/v1/sessions/{session_id}/events")
        return SessionEvents.parse_response(response).query_result

    def update_state_by_id(
        self, session_ids: Union[str, List[str]], new_state: SessionStates
    ):
        """
        Change the state of a one or more items specified by ID.

        Processes up to 100 session IDs at a time and continues to make subsequent API calls until all indicated items are updated.

        **Parameters**:

        * **session_id**: `str | List[str]` (required) - One or more session IDs.
        * **state**: [`SessionStates`][items-session-states] - The new state for the desired items.

        **Returns**: An array of all `requests.Response` objects received during processing.
        """
        if isinstance(session_ids, str):
            session_ids = [session_ids]
        results = []
        ids = iter(session_ids)
        while True:
            chunk = list(itertools.islice(ids, 100))
            if not chunk:
                break
            else:
                data = SessionsChangeStateRequest(ids=session_ids, newState=new_state)
                response = self._parent.session.post(
                    "/v1/sessions/change-state", json=data.dict()
                )
                results.append(response)
        return results

    def update_state_by_criteria(
        self,
        new_state: SessionStates,
        actor_id: str = None,
        start_time: Union[str, datetime, int] = None,
        end_time: Union[str, datetime, int] = None,
        has_alerts: bool = True,
        risk_indicators: List[str] = None,
        states: List[SessionStates] = None,
        severities: Union[List[int], int] = None,
        rule_ids: Union[List[str], str] = None,
        watchlist_ids: Union[List[str], str] = None,
        content_inspection_status: Optional[ContentInspectionStatuses] = None,
    ):
        """
        Change the state of all items matching the filter criteria.

        Makes an initial API call to update the desired items to the `state`.
        Processes up to 500 session IDs at a time and continues to make subsequent API calls until all items matching the criteria are updated.

        **Parameters**:

        * **actor_id**: `str | None` - The ID of the actor to limit the search to.
        * **start_time**: `datetime | str | int | None` - Only include items beginning on or after this date and time.  Can be a date-formatted string, a `datetime` instance, or a POSIX `int` timestamp.
        * **end_time**: `datetime | str | int | None` - Only include items beginning before this date and time.  Can be a date-formatted string, a `datetime` instance, or a POSIX `int` timestamp.
        * **has_alerts**: `bool` - Only include items that have a matching alert status. Defaults to `True`.
        * **sort_key**: [`SortKeys`][items-sort-keys] - `end_time` or `score`. Value on which the results will be sorted. Defaults to `end time`.
        * **risk_indicators**: `List[str] | None` - List of risk indicator IDs that must be present on the items before they are returned.
        * **sort_dir**: `SortDirection` - `asc` for ascending or `desc` for descending. The direction in which to sort the response based on the corresponding key. Defaults to `desc`.
        * **states**: List[[`SessionStates`][items-session-states]] - Only include items that have a matching state.
        * **severities**: `List[int | None` - Only include items that have a matching severity value. 0 = no risk, 1 = low, 2 = moderate, 3 = high, 4 = critical
        * **rule_ids**: `List[str] | None` - Optional list of rule ids to filter upon.
        * **watchlist_ids**: `List[str] | None` - Optional list of watchlist ids to filter upon.
        * **page_num**: `int` - Page number for results, starting at 1.
        * **page_size**: `int` - Max number of results to return per page, between 1 and 50 inclusive. Defaults to 50.
        * **content_inspection_status**: `List[[ContentInspectionStatuses][items-content-inspection-statuses]] | None` - The content inspection status(es) to limit the search to.

        **Returns**: An array of all `requests.Response` objects received during processing.
        """

        # Parse timestamps
        if start_time and not isinstance(start_time, (int, float)):
            start_time = parse_ts_to_posix_ts(start_time)
        if end_time and not isinstance(end_time, (int, float)):
            end_time = parse_ts_to_posix_ts(end_time)

        if states and not isinstance(states, List):
            states = [states]
        if rule_ids and not isinstance(rule_ids, List):
            rule_ids = [rule_ids]
        if watchlist_ids and not isinstance(watchlist_ids, List):
            watchlist_ids = [watchlist_ids]
        if severities and not isinstance(severities, List):
            severities = [severities]

        data = SessionsCriteriaRequest(
            actor_id=actor_id,
            on_or_after=start_time,
            before=end_time,
            has_alerts=str(has_alerts).lower() if has_alerts is not None else None,
            risk_indicators=risk_indicators,
            state=states,
            severity=severities,
            rule_id=rule_ids,
            watchlist_id=watchlist_ids,
            content_inspection_status=content_inspection_status,
        )
        continuation_token = None
        initial_request_made = False
        results = []

        # make initial request & continue processing continuation tokens
        while continuation_token is not None or not initial_request_made:
            response = self._parent.session.post(
                "/v1/sessions/change-states",
                params=data.dict(),
                json={"continuationToken": continuation_token, "newState": new_state},
            )
            results.append(response)
            initial_request_made = True
            try:
                continuation_token = response.json()["continuationToken"]
            except IndexError:
                continuation_token = None
        return results

    def add_note(self, session_id: str, note_content: str):
        """
        Add a note to a session, specified by ID.

        **Parameters**:

        * **session_id**: `str` (required) - The session ID.
        * **note_content**: `str` (required) -  The note content to add. Max 2000 characters.

        **Returns**: A `requests.Response` object indicating success.
        """
        if len(note_content) > 2000:
            raise ValueError("note_content has a 2000 character max limit.")

        return self._parent.session.post(
            f"/v1/sessions/{session_id}/add-note", json={"noteContent": note_content}
        )


class SessionsClient:
    def __init__(self, parent):
        self._parent = parent
        self._v1 = None

    @property
    def v1(self):
        if self._v1 is None:
            self._v1 = SessionsV1(self._parent)
        return self._v1
