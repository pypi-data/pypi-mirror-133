import datetime
from typing import Any, Dict, Iterable, List, Optional, Union

from benchling_api_client.extensions import UnknownType
from benchling_api_client.types import Response
from benchling_api_client.v2.alpha.api.workflow_tasks import (
    archive_workflow_tasks,
    bulk_copy_workflow_tasks,
    bulk_create_workflow_tasks,
    bulk_update_workflow_tasks,
    copy_workflow_task,
    create_workflow_task,
    get_workflow_task,
    list_workflow_tasks,
    unarchive_workflow_tasks,
    update_workflow_task,
)
from benchling_api_client.v2.alpha.models.list_workflow_tasks_scheduled_on import ListWorkflowTasksScheduledOn
from benchling_api_client.v2.alpha.models.workflow_task import WorkflowTask
from benchling_api_client.v2.alpha.models.workflow_task_archive_reason import WorkflowTaskArchiveReason
from benchling_api_client.v2.alpha.models.workflow_task_bulk_create import WorkflowTaskBulkCreate
from benchling_api_client.v2.alpha.models.workflow_task_bulk_update import WorkflowTaskBulkUpdate
from benchling_api_client.v2.alpha.models.workflow_task_create import WorkflowTaskCreate
from benchling_api_client.v2.alpha.models.workflow_task_update import WorkflowTaskUpdate
from benchling_api_client.v2.alpha.models.workflow_tasks_archival_change import WorkflowTasksArchivalChange
from benchling_api_client.v2.alpha.models.workflow_tasks_archive import WorkflowTasksArchive
from benchling_api_client.v2.alpha.models.workflow_tasks_bulk_copy_request import WorkflowTasksBulkCopyRequest
from benchling_api_client.v2.alpha.models.workflow_tasks_bulk_create_request import (
    WorkflowTasksBulkCreateRequest,
)
from benchling_api_client.v2.alpha.models.workflow_tasks_bulk_update_request import (
    WorkflowTasksBulkUpdateRequest,
)
from benchling_api_client.v2.alpha.models.workflow_tasks_paginated_list import WorkflowTasksPaginatedList
from benchling_api_client.v2.alpha.models.workflow_tasks_unarchive import WorkflowTasksUnarchive

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import (
    none_as_unset,
    optional_array_query_param,
    schema_fields_query_param,
)
from benchling_sdk.models import AsyncTaskLink
from benchling_sdk.services.base_service import BaseService


class WorkflowTaskService(BaseService):
    """
    Workflow Tasks.

    Workflow tasks encapsulate a single unit of work.

    See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks
    """

    @api_method
    def get_by_id(self, workflow_task_id: str) -> WorkflowTask:
        """
        Get a workflow task.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/getWorkflowTask
        """
        response = get_workflow_task.sync_detailed(client=self.client, workflow_task_id=workflow_task_id)
        return model_from_detailed(response)

    @api_method
    def _workflow_tasks_page(
        self,
        ids: Optional[Iterable[str]] = None,
        workflow_task_group_ids: Optional[Iterable[str]] = None,
        schema_id: Optional[str] = None,
        status_ids: Optional[Iterable[str]] = None,
        assignee_ids: Optional[Iterable[str]] = None,
        watcher_ids: Optional[Iterable[str]] = None,
        responsible_team_ids: Optional[Iterable[str]] = None,
        execution_origin_ids: Optional[Iterable[str]] = None,
        execution_types: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        creator_ids: Optional[Iterable[str]] = None,
        scheduled_on: Union[None, ListWorkflowTasksScheduledOn, datetime.date, UnknownType] = None,
        scheduled_on_lt: Optional[datetime.date] = None,
        scheduled_on_lte: Optional[datetime.date] = None,
        scheduled_on_gte: Optional[datetime.date] = None,
        scheduled_on_gt: Optional[datetime.date] = None,
        modified_at: Optional[datetime.date] = None,
        display_ids: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
        next_token: NextToken = None,
    ) -> Response[WorkflowTasksPaginatedList]:
        return list_workflow_tasks.sync_detailed(  # type: ignore
            client=self.client,
            ids=none_as_unset(optional_array_query_param(ids)),
            workflow_task_group_ids=none_as_unset(optional_array_query_param(workflow_task_group_ids)),
            schema_id=none_as_unset(schema_id),
            status_ids=none_as_unset(optional_array_query_param(status_ids)),
            assignee_ids=none_as_unset(optional_array_query_param(assignee_ids)),
            watcher_ids=none_as_unset(optional_array_query_param(watcher_ids)),
            responsible_team_ids=none_as_unset(optional_array_query_param(responsible_team_ids)),
            execution_origin_ids=none_as_unset(optional_array_query_param(execution_origin_ids)),
            execution_types=none_as_unset(optional_array_query_param(execution_types)),
            # Ignore for non-stable because we expect v2.alpha.models.schema_fields_query_param.SchemaFieldsQueryParam
            schema_fields=none_as_unset(schema_fields_query_param(schema_fields)),  # type: ignore
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            creator_ids=none_as_unset(optional_array_query_param(creator_ids)),
            scheduled_on=none_as_unset(scheduled_on),
            scheduled_onlt=none_as_unset(scheduled_on_lt),
            scheduled_onlte=none_as_unset(scheduled_on_lte),
            scheduled_ongte=none_as_unset(scheduled_on_gte),
            scheduled_ongt=none_as_unset(scheduled_on_gt),
            modified_at=none_as_unset(modified_at),
            display_ids=none_as_unset(optional_array_query_param(display_ids)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
        )

    def list(
        self,
        ids: Optional[Iterable[str]] = None,
        workflow_task_group_ids: Optional[Iterable[str]] = None,
        schema_id: Optional[str] = None,
        status_ids: Optional[Iterable[str]] = None,
        assignee_ids: Optional[Iterable[str]] = None,
        watcher_ids: Optional[Iterable[str]] = None,
        responsible_team_ids: Optional[Iterable[str]] = None,
        execution_origin_ids: Optional[Iterable[str]] = None,
        execution_types: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        creator_ids: Optional[Iterable[str]] = None,
        scheduled_on: Union[None, ListWorkflowTasksScheduledOn, datetime.date, UnknownType] = None,
        scheduled_on_lt: Optional[datetime.date] = None,
        scheduled_on_lte: Optional[datetime.date] = None,
        scheduled_on_gte: Optional[datetime.date] = None,
        scheduled_on_gt: Optional[datetime.date] = None,
        modified_at: Optional[datetime.date] = None,
        display_ids: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[WorkflowTask]:
        """
        List workflow tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/listWorkflowTasks
        """

        def api_call(next_token: NextToken) -> Response[WorkflowTasksPaginatedList]:
            return self._workflow_tasks_page(
                ids=ids,
                workflow_task_group_ids=workflow_task_group_ids,
                schema_id=schema_id,
                status_ids=status_ids,
                assignee_ids=assignee_ids,
                watcher_ids=watcher_ids,
                responsible_team_ids=responsible_team_ids,
                execution_origin_ids=execution_origin_ids,
                execution_types=execution_types,
                schema_fields=schema_fields,
                name=name,
                name_includes=name_includes,
                creator_ids=creator_ids,
                scheduled_on=scheduled_on,
                scheduled_on_lt=scheduled_on_lt,
                scheduled_on_lte=scheduled_on_lte,
                scheduled_on_gte=scheduled_on_gte,
                scheduled_on_gt=scheduled_on_gt,
                modified_at=modified_at,
                display_ids=display_ids,
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: WorkflowTasksPaginatedList) -> Optional[List[WorkflowTask]]:
            return body.workflow_tasks

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, workflow_task: WorkflowTaskCreate) -> WorkflowTask:
        """
        Create a new workflow task.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/createWorkflowTask
        """
        response = create_workflow_task.sync_detailed(client=self.client, json_body=workflow_task)
        return model_from_detailed(response)

    @api_method
    def update(self, workflow_task_id: str, workflow_task: WorkflowTaskUpdate) -> WorkflowTask:
        """
        Update a workflow task.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/updateWorkflowTask
        """
        response = update_workflow_task.sync_detailed(
            client=self.client, workflow_task_id=workflow_task_id, json_body=workflow_task
        )
        return model_from_detailed(response)

    @api_method
    def copy(self, workflow_task_id: str) -> WorkflowTask:
        """
        Copy workflow task.

        Creates a new workflow task with the same fields and assignee as the provided task and creates
        a relationship between the two tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/copyWorkflowTask
        """
        response = copy_workflow_task.sync_detailed(
            client=self.client,
            workflow_task_id=workflow_task_id,
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, workflow_task_ids: Iterable[str], reason: WorkflowTaskArchiveReason
    ) -> WorkflowTasksArchivalChange:
        """
        Archive one or more workflow tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/archiveWorkflowTasks
        """
        archive_request = WorkflowTasksArchive(reason=reason, workflow_task_ids=list(workflow_task_ids))
        response = archive_workflow_tasks.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, workflow_task_ids: Iterable[str]) -> WorkflowTasksArchivalChange:
        """
        Unarchive one or more workflow tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/unarchiveWorkflowTasks
        """
        unarchive_request = WorkflowTasksUnarchive(workflow_task_ids=list(workflow_task_ids))
        response = unarchive_workflow_tasks.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_create(self, workflow_tasks: Iterable[WorkflowTaskBulkCreate]) -> AsyncTaskLink:
        """
        Create one or more workflow tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/bulkCreateWorkflowTasks
        """
        body = WorkflowTasksBulkCreateRequest(list(workflow_tasks))
        response = bulk_create_workflow_tasks.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update(self, workflow_tasks: Iterable[WorkflowTaskBulkUpdate]) -> AsyncTaskLink:
        """
        Update one or more workflow tasks.

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/bulkUpdateWorkflowTasks
        """
        body = WorkflowTasksBulkUpdateRequest(list(workflow_tasks))
        response = bulk_update_workflow_tasks.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_copy(self, workflow_task_ids: Iterable[str]) -> AsyncTaskLink:
        """
        Bulk copy workflow tasks.

        Bulk creates new workflow tasks where each new task has the same fields and assignee as one of
        the provided tasks and creates a relationship between the provided task and its copy

        See https://benchling.com/api/v2-alpha/reference?showLA=true#/Workflow%20Tasks/bulkCopyWorkflowTask
        """
        body = WorkflowTasksBulkCopyRequest(list(workflow_task_ids))
        response = bulk_copy_workflow_tasks.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)
