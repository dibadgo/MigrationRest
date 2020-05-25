from binds.MigrationBind import MigrationBind
from models.migration import Migration
from models.workload import Workload
from storage.cruid_repository import CruidRepository
from storage.mongo_provider import MotorClientFactory
from storage.workloads_repo import WorkloadsRepo


class MigrationRepo(CruidRepository):
    """The concrete implementation of Migration repo"""

    def __init__(self, mongo_client: MotorClientFactory, workload_repo: WorkloadsRepo):
        self._workload_repo = workload_repo
        super().__init__(mongo_client, collection_name="migration_binds")

    def create_model_from_dict(self, d: dict, obj_id: str):
        d["id"] = obj_id
        return MigrationBind(**d)

    def model_to_dict(self, model: MigrationBind) -> dict:
        return model.dict()

    async def get_async(self, document_id) -> Migration:
        bind = await super().get_async(document_id)

        source_workload, target_workload = await self._get_source_and_target(bind)
        return bind.get_migration(source_workload, target_workload)

    async def create_async(self, document: MigrationBind) -> Migration:
        return await super().create_async(document)

    async def update_async(self, document_id, document: MigrationBind) -> Migration:
        old_bind = await super().get_async(document_id)

        if document.mount_points:
            old_bind.mount_points = document.mount_points

        if document.source_id:
            source_workload = await self._workload_repo.get_async(document.source_id)
            old_bind.source_id = source_workload.id

        if document.migration_target:
            if document.migration_target.target_vm_id:
                target_workload = await self._workload_repo.get_async(document.migration_target.target_vm_id)
                old_bind.migration_target.target_vm_id = target_workload.id

            if document.migration_target.cloud_type:
                old_bind.migration_target.cloud_type = document.migration_target.cloud_type

            if document.migration_target.cloud_credentials:
                old_bind.migration_target.cloud_credentials = document.migration_target.cloud_credentials

        return await super().update_async(document_id, old_bind)

    async def list_async(self):
        binds = await super().list_async()

        migrations = []
        for b in binds:
            source_workload, target_workload = await self._get_source_and_target(b)
            m = b.get_migration(source_workload, target_workload)
            migrations.append(m)

        return migrations

    async def _get_source_and_target(self, bind: MigrationBind) -> (Workload, Workload):
        source_workload = await self._workload_repo.get_async(bind.source_id)
        target_workload = await self._workload_repo.get_async(bind.migration_target.target_vm_id)

        return source_workload, target_workload
