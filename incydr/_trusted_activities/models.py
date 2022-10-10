from __future__ import annotations

from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from incydr._core.models import ResponseModel
from incydr.enums.trusted_activities import ActivityType
from incydr.enums.trusted_activities import Name
from incydr.enums.trusted_activities import PrincipalType


class ProviderObject(BaseModel):
    name: Optional[Name] = Field(
        None,
        description="The name of a provider for a specified activity action.\n  ### Supported providers for trusted "
        "activity type and actions\n\n  - `DOMAIN`\n    - `CLOUD_SHARE`\n      - `BOX`\n      - "
        "`GOOGLE_DRIVE` \n      - `ONE_DRIVE`\n    - `CLOUD_SYNC`\n      - `BOX`\n      - `GOOGLE_DRIVE` "
        "\n      - `ICLOUD` \n      - `ONE_DRIVE` \n    - `EMAIL` \n      - `GMAIL`\n      - "
        "`OFFICE_365`\n  - `ACCOUNT_NAME`\n    - `CLOUD_SYNC`\n      - `DROPBOX`\n      - `ONE_DRIVE`\n",
    )

    class Config:
        use_enum_values = True


class ActivityAction(BaseModel):
    type: Optional[ActivityType] = Field(
        None,
        description="The type of an activity action.\n### Supported trusted activity types for each activity action "
        "type\n\n- `CLOUD_SHARE` \n  - `DOMAIN`\n- `CLOUD_SYNC` \n  - `DOMAIN`\n  - `ACCOUNT_NAME`\n- "
        "`EMAIL` \n  - `DOMAIN`\n- `FILE_UPLOAD`\n  - `DOMAIN`\n\nNote: `SLACK` and `URL_PATH` do not "
        "need any activity actions specified.\n",
    )
    providers: Optional[List[ProviderObject]] = Field(
        None,
        description="A list of enabled providers for the specified activity action.",
    )

    class Config:
        use_enum_values = True


class ActivityActionGroup(BaseModel):
    name: Optional[Name] = Field(
        "DEFAULT",
        description="The name of the activity action group. Currently, only `DEFAULT` activity action group is "
        "supported.",
    )
    activityActions: Optional[List[ActivityAction]] = Field(
        None, description="The list of activity actions for an activity action group."
    )

    class Config:
        use_enum_values = True


class TrustedActivity(ResponseModel):
    """A model representing an TrustedActivity.

    **Fields**:

    * **activity_action_groups**: `List[ActivityActionGroup]` The list of activity actions associated with the activity.
    * **activity_id**: `str` The unique identifier of the trusted activity.
    * **description**: `str` A description of the trusted activity.
    * **principal_type**: `PrincipalType | None`
    * **activity_type**: `ActivityType | None` The type of the trusted activity.
    * **update_time**: `datetime | None` The time at which the trust activity was last created or modified.
    * **updated_by_principal_id**: `str | None` The unique identifier of the user who last updated the trust activity.
    * **updated_by_principal_name**: `str | None` The username of the user who last updated the trusted activity.
    * **value**: `str` The value of the trusted activity.
    """

    activity_action_groups: Optional[List[ActivityActionGroup]] = Field(
        None,
        description="The list of activity actions associated with the activity.",
        alias="activityActionGroups",
    )
    activity_id: Optional[str] = Field(
        None,
        description="The unique identifier of the trusted activity.",
        alias="activityId",
        allow_mutation=False,
    )
    description: Optional[str] = Field(
        None, description="A description of the trusted activity."
    )
    principal_type: Optional[PrincipalType] = Field(
        None, alias="principalType", allow_mutation=False
    )
    activity_type: Optional[ActivityType] = Field(
        None, description="The type of the trusted activity.", alias="activityType"
    )
    update_time: Optional[datetime] = Field(
        None,
        description="The time at which the trust activity was last created or modified.",
        alias="updateTime",
        allow_mutation=False,
    )
    updated_by_principal_id: Optional[str] = Field(
        None,
        description="The unique identifier of the user who last updated the trust activity.",
        alias="updatedByPrincipalId",
        allow_mutation=False,
    )
    updated_by_principal_name: Optional[str] = Field(
        None,
        description="The username of the user who last updated the trusted activity.",
        alias="updatedByPrincipalName",
        allow_mutation=False,
    )
    value: Optional[str] = Field(None, description="The value of the trusted activity.")

    class Config:
        validate_assignment = True


class UpdateTrustedActivity(BaseModel):
    activity_action_groups: Optional[List[ActivityActionGroup]] = Field(
        None,
        description="The list of activity action groups for the trusted activity. \n- `DOMAIN` - If array is empty, "
        "existing activity action groups are maintained. \n- `ACCOUNT_NAME` - Atleast 1 activity action "
        "group is required.\n- `SLACK` - No activity action groups are allowed - array must be empty.\n- "
        "`URL_PATH` - No activity action groups are allowed - array must be empty.\n",
        alias="activityActionGroups",
    )
    description: Optional[str] = Field(
        None, description="The description of the trusted activity."
    )
    activity_type: Optional[ActivityType] = Field(
        None,
        description="The type of the trusted activity.\n\nNote: The `ACCOUNT_NAME` trusted activity type requires "
        "agent version 1.5.0 or later for Incydr \nProfessional, Enterprise, Gov F2, and Horizon product "
        "plans, and Code42 app version 9.0.0 or later for \nIncydr Basic, Advanced, and Gov F1 product "
        "plans.\n",
        alias="activityType",
    )
    value: Optional[str] = Field(None, description="The value of the trusted activity.")

    class Config:
        extra = "ignore"


class TrustedActivitiesPage(ResponseModel):
    """
    A model representing a page of `TrustedActivity` objects.

    **Fields**:

    * **total_count**: `int` Total count of trusted activities found by the query.
    * **trusted_activities**: `List[TrustedActivity]` The list of trusted activities retrieved from the query.
    """

    total_count: Optional[float] = Field(None, alias="totalCount")
    trusted_activities: Optional[List[TrustedActivity]] = Field(
        None,
        description="A list of TrustedActivityResponses",
        alias="trustedActivities",
    )


class QueryTrustedActivitiesRequest(BaseModel):
    page_num: Optional[int]
    page_size: Optional[int]
    activity_type: Optional[str]
    sort_key: Optional[str]
    sort_direction: Optional[str]


class CreateTrustedActivityRequest(BaseModel):
    type: Optional[str]
    value: Optional[str]
    description: Optional[str]
    activityActionGroups: Optional[List[ActivityActionGroup]]

    class Config:
        use_enum_values = True
