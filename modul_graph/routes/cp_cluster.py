from fastapi import APIRouter, HTTPException

from modul_graph.DTOs import RichCPCluster
from modul_graph.models.cp_cluster import CpCluster
from modul_graph.utils.sc_DAO import get_rich_cp_cluster

router = APIRouter(prefix="/cp_cluster")


@router.get("/{cp_cluster_id}")
def get_cp_cluster(cp_cluster_id: str) -> RichCPCluster:
    cp_cluster: CpCluster | None = CpCluster.nodes.first_or_none(identifier=cp_cluster_id)

    if cp_cluster is None:
        raise HTTPException(404, f"CpCluster with id {cp_cluster_id} not found")

    return get_rich_cp_cluster(cp_cluster)
