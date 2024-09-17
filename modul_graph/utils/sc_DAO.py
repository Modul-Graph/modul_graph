from modul_graph.DTOs import RichCPCluster, RichCPClusterCell
from modul_graph.models.cp_cluster import CpCluster
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.module_cell import ModuleCell
from modul_graph.models.semester import Semester
from modul_graph.models.standard_curriculum import StandardCurriculum


def get_cp_clusters(sc: StandardCurriculum) -> set[CpCluster]:
    """
    Get all CP clusters from a standard curriculum
    :param sc:
    :return:
    """

    res: set[CpCluster] = set()

    semesters: list[Semester] = list(sc.specifies_semester.all())

    for semester in semesters:
        cp_clusters: list[CpCluster] = list(semester.consists_of_cp_cluster.all())
        res.update(cp_clusters)

    return res


def get_semester_range(cp_cluster: CpCluster) -> tuple[int, int]:
    """
    Get min/max semester from a CP cluster
    :param cp_cluster: CP Cluster to be considered
    :return: tuple of form: (min-semester, max-semester)
    """

    semesters: list[Semester] = list(cp_cluster.is_component_of_semester.all())
    semester_nums: list[int] = [semester.number for semester in semesters]

    return min(semester_nums), max(semester_nums)


def get_cell_display_info(cp_cluster: CpCluster) -> list[tuple[str, int, int, str, bool]]:
    """
    Get display information for a cell
    :param cp_cluster: CP Cluster to be considered
    :return: list of cell information. Cell is tuple of form: (pflichtmodule-/wpf-name, cp, semester, cell_id)
    """

    res: list[tuple[str, int, int, str, bool]] = []

    module_cells: list[ModuleCell] = list(cp_cluster.consists_of_module_cell.all())

    for module_cell in module_cells:
        semester: Semester = module_cell.is_in_semester.single()
        module_area: ModuleArea = module_cell.filled_by_module_area.single()
        module_name: str
        cp: int
        cell_id: str = module_cell.identifier

        if module_area.is_wpf:
            module_name = module_area.name
            cp = module_area.cp  # TODO: implement missing CP for module_area
        else:
            module: Module = module_area.filled_by_module.single()
            module_name = module.name
            cp = module.cp_plus_description["DEFAULT"]

        res.append((module_name, cp, semester.number, cell_id, module_area.is_wpf))

    return res


def get_rich_cp_cluster(cp_cluster: CpCluster) -> RichCPCluster:
    """
    Get rich CP cluster of a CP cluster
    :param cp_cluster: the CP cluster
    :return: CP cluster enriched with module information
    """

    cells: list[RichCPClusterCell] = []

    for module_name, cp, semester, cell_id, isWPF in get_cell_display_info(cp_cluster):
        cells.append(RichCPClusterCell(cp=cp, sem=semester, name=module_name, cellId=cell_id, isWPF=isWPF))

    return RichCPCluster(cells=cells, cp_note=cp_cluster.cp_number, cp_cluster_id=cp_cluster.identifier)

def get_rich_cp_clusters(sc: StandardCurriculum) -> list[RichCPCluster]:
    """
    Get rich CP clusters of a standard curriculum
    :param sc: the standard curriculum
    :return: list of all cp clusters in the SC enriched with module information
    """

    rich_cp_clusters: list[RichCPCluster] = []
    cp_clusters: set[CpCluster] = get_cp_clusters(sc)

    for cp_cluster in cp_clusters:
        rich_cp_clusters.append(get_rich_cp_cluster(cp_cluster))

    return rich_cp_clusters
