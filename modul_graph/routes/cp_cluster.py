from uuid import uuid4

from fastapi import APIRouter, HTTPException

from modul_graph.DTOs import RichCPCluster, UpdateCPClusterDTO, CreateCPClusterDTO
from modul_graph.models.cp_cluster import CpCluster
from modul_graph.models.module_cell import ModuleCell
from modul_graph.utils.cp_cluster import util_update_cp_cluster
from modul_graph.utils.sc_DAO import get_rich_cp_cluster

router = APIRouter(prefix="/cp_cluster")


@router.get("/{cp_cluster_id}")
def get_cp_cluster(cp_cluster_id: str) -> RichCPCluster:
    cp_cluster: CpCluster | None = CpCluster.nodes.first_or_none(identifier=cp_cluster_id)

    if cp_cluster is None:
        raise HTTPException(404, f"CpCluster with id {cp_cluster_id} not found")

    return get_rich_cp_cluster(cp_cluster)


@router.put("/")
def update_cp_cluster(data: UpdateCPClusterDTO) -> None:
    cp_cluster: CpCluster | None = CpCluster.nodes.first_or_none(identifier=data.clusterId)

    if cp_cluster is None:
        raise HTTPException(404, f"CpCluster with id {data.clusterId} not found")

    util_update_cp_cluster(cp_cluster, data)

    cp_cluster.save()


@router.delete("/{cp_cluster_id}")
def delete_cp_cluster(cp_cluster_id: str) -> None:
    cp_cluster: CpCluster | None = CpCluster.nodes.first_or_none(identifier=cp_cluster_id)

    if cp_cluster is None:
        raise HTTPException(404, f"CpCluster with id {cp_cluster_id} not found")

    cells: list[ModuleCell] = cp_cluster.consists_of_module_cell.all()

    for cell in cells:
        cell.delete()

    cp_cluster.delete()


@router.post("/")
def create_cp_cluster(data: CreateCPClusterDTO) -> None:
    cp_cluster = CpCluster()
    cp_cluster.identifier = str(uuid4())
    cp_cluster.cp_number = data.cp_note
    cp_cluster.save()
    util_update_cp_cluster(cp_cluster, data)
