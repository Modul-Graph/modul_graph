from .data_access import da_get_winter_for_module, da_get_module_areas_of_optional_modules_unwound_no_duplicates, da_get_semester_for_obl_module_via_module_area, da_get_module_areas_of_obligatory_modules, da_get_semester_of_module_cell, da_get_summer_for_module, da_get_module_area_for_module_cell, da_get_module_cells_connected_to_module_areas_without_duplicates, da_get_obl_module_via_module_area, da_get_module_areas_for_module, da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates, da_get_provided_comps_per_module, da_get_possible_modules_via_existing_comps, da_get_obl_module_via_module_area, da_get_winter_for_standard_curriculum, da_get_needed_comps_for_module, da_get_previous_modules_for_single_module, da_get_highest_semester_of_std_curr, da_get_modules_indirectly_connected_to_comp
from .std_curr import std_curr, instantiate_std_curr_obj
from collections import Counter
from random import shuffle
from .graph_exception import GraphException

# service provides controller with processed data and gets its data from data_access (NOT from repository)


# ----------------------------------------------------------------------------------------------------------------------
# public functions (accessed by controller)

def get_path_to_competence(comp: str, standard_curriculum: str) -> list[list[str | list[int]] | list[list[int]]]:
    instantiate_std_curr_obj(standard_curriculum)
    start_comps_plus_sem_and_obl_mods: tuple[dict[str, int], dict[str, list[int]]] = tuple(
        get_start_competences_plus_sems_and_obl_mods_plus_sems())
    subgraph: list[list[str | list[int]] | list[list[int]]] = []

    for i in range(0, 100):
        subgraph = __get_subgraph_for_feasibility_analysis(comp, start_comps_plus_sem_and_obl_mods)
        passed: bool = False
        if not subgraph:
            continue

        for module in subgraph:
            if comp in da_get_provided_comps_per_module(module[0]):
                passed = True
        if passed:
            return subgraph

    raise GraphException('No suitable standard curriculum has been found, reason not identifiable.')


def get_start_competences_plus_sems_and_obl_mods_plus_sems() -> tuple[dict[str, int], dict[str, list[int]]]:
    # get names of module areas connected to obligatory modules (each will be single module area, not list)
    module_areas: list[str] = da_get_module_areas_of_obligatory_modules()

    # declaration of variables
    obligatory_modules: list[str] = []
    # nested list because module 'Nebenfach' has several semesters
    semesters: list[list[int]] = []
    ignored_modules: list[str] = []     # in case it needs to be accessed at some point
    competences_plus_semester: dict[str, int] = dict()

    # get obligatory modules and their corresponding semesters
    for module_area in module_areas:
        semester: list[int] = da_get_semester_for_obl_module_via_module_area(module_area)
        # bachelor thesis and minor module don't have one single semester specified
        if len(semester) < 1:
            semester = [-1]
        semesters.append(semester)
        obl_module: str = da_get_obl_module_via_module_area(module_area)
        obligatory_modules.append(obl_module)
    obl_modules_plus_semester = dict(zip(obligatory_modules, semesters))

    # get competences provided by obligatory modules and their earliest possible time of provision
    for module in obligatory_modules:
        comps: list[str] = da_get_provided_comps_per_module(module)
        # if comps is empty, foreach would throw error
        if len(comps) < 1:
            continue
        for comp in comps:
            semester_of_comp_provision: int = min(obl_modules_plus_semester[module]) + 1
            # module 'Bachelorarbeit' has semester -1 (like all modules which don't have a semester specified in the database)
            # that means, the comparison "competences_plus_semester[comp] > semester_of_comp_provision" (see below) would always favor a semester of 0
            if semester_of_comp_provision == 0:
                semester_of_comp_provision = 100
            # if competence is not yet included in dict or if the semester of competence provision can be lowered: update dict
            if comp not in competences_plus_semester.keys() or competences_plus_semester[comp] > semester_of_comp_provision:
                competences_plus_semester.update({comp: semester_of_comp_provision})

    return competences_plus_semester, obl_modules_plus_semester


def does_feasible_subgraph_exist(standard_curriculum: str) -> bool:
    instantiate_std_curr_obj(standard_curriculum)
    start_comps_plus_sem_and_obl_mods_plus_sems: tuple[dict[str, int], dict[str, list[int]]] = tuple(get_start_competences_plus_sems_and_obl_mods_plus_sems())
    subgraph: list[list[str | list[int]] | list[list[int]]] = __get_subgraph_for_feasibility_analysis('invalid', start_comps_plus_sem_and_obl_mods_plus_sems)
    if not subgraph:
        raise GraphException('No suitable standard curriculum has been found, reason not identifiable.')
    return True


# ----------------------------------------------------------------------------------------------------------------------
# private functions

def __get_subgraph_for_feasibility_analysis(wanted_comp: str, start_comps_plus_sem_and_obl_mods_plus_sems: tuple[dict[str, int], dict[str, list[int]]]) -> list[list[str | list[int]]]:
    length: int = len(start_comps_plus_sem_and_obl_mods_plus_sems[1])
    obl_mods: list[str] = list(start_comps_plus_sem_and_obl_mods_plus_sems[1].keys())
    obl_mods_sems: list[list[int]] = list(start_comps_plus_sem_and_obl_mods_plus_sems[1].values())
    links_for_obl_mods = __compute_links_for_obl_mods(obl_mods, obl_mods_sems)

    # subgraph initialised to obligatory modules
    # list content per row: name, slot type, semester, previous_modules
    subgraph: list[list[str] | list[int] | list[list[int]]] = [obl_mods, ["Pflichtmodul"] * length, list(start_comps_plus_sem_and_obl_mods_plus_sems[1].values()), links_for_obl_mods]
    types_of_free_slots, sems_of_free_slots, winter_of_free_slots = __get_free_slots_by_type_plus_semester_plus_season()
    if len(types_of_free_slots) == 0:
        raise GraphException('There are no elective slots to be filled.')
    competence_pool: list[str] = list(start_comps_plus_sem_and_obl_mods_plus_sems[0].keys())
    provided_in_sem: list[int] = list(start_comps_plus_sem_and_obl_mods_plus_sems[0].values())
    lowest_sem_of_free_slot: int = min(sems_of_free_slots)
    highest_sem_of_free_slot: int = max(sems_of_free_slots)

    for curr_sem in range(lowest_sem_of_free_slot, highest_sem_of_free_slot + 1):

        # get provided competences up until current semester
        limited_comps: list[str] = [competence_pool[i] for i in range(len(competence_pool)) if provided_in_sem[i] <= curr_sem]

        possible_modules: list[str] = __get_next_level_modules(limited_comps.copy(), subgraph[0])
        # remove duplicates
        possible_modules = [item for item in possible_modules if item not in subgraph]
        # check if all competences a possible module needs are provided (in current semester)
        possible_modules = [item for item in possible_modules if set(da_get_needed_comps_for_module(item)) <= set(limited_comps)]

        # when algorithm is at this point, free slots have not been filled -> possible modules have to exist to continue
        if len(possible_modules) == 0:
            raise GraphException('There are not enough modules to fill all elective slots according to their type.')

        found_modules: list[str] = []
        found_modules_slot_types: list[str] = []
        found_modules_sems: list[int] = []

        # try 10 times to find fitting subgraph
        for i in range(0, 10):
            found_modules, found_modules_slot_types, found_modules_sems, types_of_free_slots, winter_of_free_slots, sems_of_free_slots = __fit_possible_modules_to_free_slots(wanted_comp, possible_modules, list(types_of_free_slots), list(winter_of_free_slots), list(sems_of_free_slots), curr_sem)
            # if up until current semester all free slots can be filled, move on
            if not [sem for sem in sems_of_free_slots if sem <= curr_sem]:
                break

        # if free slots left (which also have an entry in sems_of_free_slots) and their semester is the current one or lower -> standard curriculum impossible to fill
        if [sem for sem in sems_of_free_slots if sem <= curr_sem]:
            raise GraphException('There are not enough modules to fill all elective slots according to their type.')

        subgraph[0] += found_modules
        subgraph[1] += found_modules_slot_types
        subgraph[2] += found_modules_sems
        # module 'Bachelorarbeit' has semester -1 (like all modules which don't have a semester specified in the database), that's why "min(subgraph[2][i]) != -1" is necessary
        existing_mods: list[str] = [x for i, x in enumerate(subgraph[0]) if min(subgraph[2][i]) < curr_sem and min(subgraph[2][i]) != -1]
        subgraph[3] += __compute_links(found_modules, existing_mods)

        # when list of free slots empty: standard curriculum filled -> return
        if not types_of_free_slots:
            return list(zip(subgraph[0], subgraph[1], subgraph[2], subgraph[3]))
        comps_of_found_modules, sems_of_comp_provision = da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates(found_modules)
        competence_pool += comps_of_found_modules
        provided_in_sem += sems_of_comp_provision

        # delete duplicates from competence_pool and provided_in_sem
        # explanation: key is unique value from competence_pool which has duplicates in competence_pool
        indices_containing_duplicates: list[int] = [i for key in (key for key, count in Counter(competence_pool).items() if count > 1) for i, x in enumerate(competence_pool) if x == key]
        first_index_per_duplicate: list[int] = [competence_pool.index(key) for key, count in Counter(competence_pool).items()]
        indices_to_delete: list[int] = list(set(indices_containing_duplicates) - set(first_index_per_duplicate))
        provided_in_sem = [sem for i, sem in enumerate(provided_in_sem) if i not in indices_to_delete]
        competence_pool = [comp for i, comp in enumerate(competence_pool) if i not in indices_to_delete]

    if len(types_of_free_slots) != 0:
        raise GraphException('There are not enough modules to fill all elective slots according to their type.')

    return list(zip(subgraph[0], subgraph[1], subgraph[2], subgraph[3]))


def __compute_links_for_obl_mods(obl_mods: list[str], obl_mods_sems: list[list[int]]) -> list[list[str]]:
    base_mods: list[str] = [x for i, x in enumerate(obl_mods) if obl_mods_sems[i] == [1]]
    links_for_obl_mods: list[list[str]] = [['']] * len(base_mods)

    counter: int = 2
    while len(base_mods) != len(obl_mods):
        if counter > da_get_highest_semester_of_std_curr():
            # for those modules which don't have a semester specified in the database and have thus been assigned semester -1
            counter = -1
        modules_in_curr_sem: list[str] = [x for i, x in enumerate(obl_mods) if min(obl_mods_sems[i]) == counter]
        links_for_obl_mods += __compute_links(modules_in_curr_sem, base_mods)
        base_mods += modules_in_curr_sem
        if counter == -1:
            break
        counter += 1

    # only occurs if backend programmer made a mistake; helps to identify bug
    if len(base_mods) != len(links_for_obl_mods):
        raise GraphException('Please tell your backend programmer to fix the backend; error id: ge_clfom')
    return links_for_obl_mods


def __compute_links(found_mods: list[str], existing_mods: list[str]) -> list[list[str]]:
    ret_list: list[list[str]] = []
    for fmod in found_mods:
        ret_list.append(da_get_previous_modules_for_single_module(fmod, existing_mods))

    # only occurs if backend programmer made a mistake; helps to identify bug
    if len(found_mods) != len(ret_list):
        raise GraphException('Please tell your backend programmer to fix the backend; error id: ge_cl')

    return ret_list


def __get_free_slots_by_type_plus_semester_plus_season() -> tuple[list[list[str]], list[int], list[bool]]:
    free_slots_ids: list[str] = __get_free_slots_and_types()[0]
    free_slots_types: list[list[str]] = __get_free_slots_and_types()[1]
    semesters: list[int] = []
    winter: list[bool] = []

    for cell in free_slots_ids:
        semester = da_get_semester_of_module_cell(cell)
        if semester == -1:
            continue
        # if standard curriculum starts in winter, semesters with odd numbers are in winter
        res_modulo: int = 1 if da_get_winter_for_standard_curriculum(std_curr.name) else 0
        winter.append(semester % 2 == res_modulo)
        semesters.append(semester)

    # sort by semester
    if len(free_slots_ids) != 0:
        sorted_by_sem: list[any] = zip(*sorted(zip(free_slots_ids, free_slots_types, semesters, winter), key=lambda x: x[2]))
        free_slots_ids, free_slots_types, semesters, winter = sorted_by_sem

    # todo: sort by type rarity (optional, implement if performance gets bad again)

    return free_slots_types, semesters, winter


def __get_free_slots_and_types() -> tuple[list[str], list[list[str]]]:
    mod_areas_obl: list[str] = da_get_module_areas_of_obligatory_modules()
    mod_areas_opt: list[str] = da_get_module_areas_of_optional_modules_unwound_no_duplicates(mod_areas_obl)
    free_slots: list[str] = da_get_module_cells_connected_to_module_areas_without_duplicates(mod_areas_opt)
    types: list[list[str]] = []
    for slot in free_slots:
        types.append(da_get_module_area_for_module_cell(slot))
    return list(set(free_slots)), types


def __get_next_level_modules_plus_areas(comps: list[str], existing_mods: list[str]) -> tuple[list[str], list[list[str]]]:
    modules: list[str] = __get_next_level_modules(comps, existing_mods)
    modules = list(set(modules))
    areas: list[list[str]] = []
    for mod in modules:
        areas.append(da_get_module_areas_for_module(mod))
    return modules, areas


def __get_next_level_modules(comps: list[str], existing_mods: list[str]) -> list[str]:
    result: list[str] = da_get_possible_modules_via_existing_comps(comps)
    # don't include duplicates
    modules = list(set(result))
    # don't include already used modules in next level modules
    return [item for item in modules if item not in existing_mods]


# find cell/slot to fill for one module, then delete cell and module from lists
# possible_modules & areas belong together
# free_slots (contains not IDs but types of module cells, p.ex. "WPF Informatik") & semester & winter belong together
def __fit_possible_modules_to_free_slots(wanted_comp: str, possible_modules: list[str], types_of_free_slots: list[list[str]], winter_of_free_slots: list[bool], sems_of_free_slots: list[int], curr_sem) -> tuple[list[str], list[str], list[list[int]], list[list[str]], list[bool], list[int]]:
    possible_mods_season_winter: list[bool] = []
    possible_mods_season_summer: list[bool] = []
    found_modules: list[str] = []
    found_modules_slot_types: list[str] = []
    found_modules_sem: list[list[int]] = []
    indices_to_remove_from_free_slot_lists: list[int] = []

    # permutate possible modules
    shuffle(possible_modules)

    # get modules to the front which (indirectly) provide the wanted competence
    for i in range(len(possible_modules)):
        if possible_modules[i] in da_get_modules_indirectly_connected_to_comp(wanted_comp) or wanted_comp in da_get_provided_comps_per_module(possible_modules[i]):
            possible_modules = [possible_modules[i]] + possible_modules[:i] + possible_modules[i + 1:]

    # compute for each module if it can be visited during winter or summer
    for i, mod in enumerate(possible_modules):
        possible_mods_season_winter.append(da_get_winter_for_module(mod))
        possible_mods_season_summer.append(da_get_summer_for_module(mod))

    # copy because the list itself will be modified in the loop
    for i, slot in enumerate(types_of_free_slots.copy()):
        found_module: str = ''
        for j, single_slot_type in enumerate(slot):
            for k, mod in enumerate(possible_modules):
                matches_summer_winter: bool = (possible_mods_season_summer[k] and not winter_of_free_slots[j]) or (possible_mods_season_winter[k] and winter_of_free_slots[j])
                if matches_summer_winter and single_slot_type in da_get_module_areas_for_module(mod) and sems_of_free_slots[i] == curr_sem:
                    found_module = mod
                    break
            if found_module != '':
                # print(f"Found module '{found_module}' for slot '{single_slot_type}' (semester: {sems_of_free_slots[i]})")
                found_modules.append(found_module)
                found_modules_slot_types.append(single_slot_type)
                found_modules_sem.append([sems_of_free_slots[i]])
                index_to_remove: int = possible_modules.index(found_module)
                possible_modules.pop(index_to_remove)
                possible_mods_season_summer.pop(index_to_remove)
                possible_mods_season_winter.pop(index_to_remove)
                indices_to_remove_from_free_slot_lists.append(i)
                break
        if found_module == '':
            remaining_free_slots, and_their_winter, and_their_sem = __remove_indices(types_of_free_slots, winter_of_free_slots, sems_of_free_slots, indices_to_remove_from_free_slot_lists)
            return found_modules, found_modules_slot_types, found_modules_sem, remaining_free_slots, and_their_winter, and_their_sem

    remaining_free_slots, and_their_winter, and_their_sem = __remove_indices(types_of_free_slots, winter_of_free_slots, sems_of_free_slots, indices_to_remove_from_free_slot_lists)
    return found_modules, found_modules_slot_types, found_modules_sem, remaining_free_slots, and_their_winter, and_their_sem


def __remove_indices(list1: list[list[str]], list2: list[bool], list3: list[int], indices: list[int]) -> tuple[list[list[str]], list[bool], list[int]]:
    ret_list1: list[list[str]] = [item for i, item in enumerate(list1) if i not in indices]
    ret_list2: list[bool] = [item for i, item in enumerate(list2) if i not in indices]
    ret_list3: list[int] = [item for i, item in enumerate(list3) if i not in indices]
    return ret_list1, ret_list2, ret_list3


'''
Ansatz 1:
- im projekt berechnen, welche slot types nur wenig module zugeordnet haben
- wenn in einer iteration für so einen slot typ kein modul gefunden wird: schauen ob im bereits bestehenden subgraph ein modul verbaut ist,
    was u.a. als dieser slot typ gekennzeichnet ist, aber bei einem slot mit häufigem typ untergebracht ist
- dieses modul nur dann aus vorherigem slot klauen, wenn der slot anderweitig besetzt werden kann -> dann graph aktualisieren
    (komplett? welche teile davon? wenn komplett aktualisieren, kann es sein dass er sich ständig nur neu aktualisieren muss und nicht terminiert)
    weil geklautes modul vlt kompetenzen bereitgestellt hat, die jetzt nicht mehr in dem semester bereitgestellt werden können
    
Ansatz 2:
- ebenfalls im projekt berechnen, welche slot types nur wenig module zugeordnet haben
- beim filling algorithmus zuerst für slots mit seltenen typen ein modul suchen
- implementerung: liste von freien slots (mit gepaarten listen) ist bereits nach semester sortiert,
    innerhalb eines semesters wird danach sortiert, welcher slot den typ mit den wenigsten modulverbindungen hat
    - mögliche interpretationen: geringste modulverbindungen zu aktueller 'possible_modules' liste, oder generell im regelstudienplan
    - sind 2 verschiedene metriken, hauptsächlich eine davon bevorzugen, aber falls nicht alle slots des aktuellen semesters gefüllt werden können,
    mit der anderen nochmal __fit_possible_modules_to_free_slots() ausführen
    - zuerst als metrik probieren: geringste verbindungen generell im regelstudienplan
- für slots mit typ der von vielen modulen gefüllt werden kann, modul bevorzugen was keine seltenen slottypen füllen kann
- implementierung: input 'possible_modules' so sortieren, dass module hinten sind welche die selteneren slottypen bedienen,
    dabei sortierung innerhalb einer slottyp-gruppe so, dass module weiter vorn sind, die nur einen slottyp bedienen 

Ansatz 3:
- if after execution of __fit_possible_modules_to_free_slots() there are still free slots in the CURRENT semester (would mean curriculum not possible)
    permutate order of 'possible_modules' input and execute again
- it should be checked wether possible_modules contains enough modules to fill all slots, and if for each type of free slots there are enough modules to fill all slots
- the latter can be done using Counter for a flattened list of module types

Ansatz 2 & 3 sind mit weniger unklarheiten implementierbar, allerdings kann nur Ansatz 1 auf frühere semester zugreifen und dort änderungen vornehmen
Ansatz 2 ist kontrollierter und granularer als Ansatz 3
Fav.: Ansatz 2
'''