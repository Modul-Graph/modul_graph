import math
from typing import TypeVar

from neomodel import config  # type: ignore
from pygad import GA  # type: ignore

from modul_graph.models.competence import Competence
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.module_cell import ModuleCell
from modul_graph.models.semester import Semester
from modul_graph.models.standard_curriculum import StandardCurriculum

__T = TypeVar('__T')

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default


class Suggestion:
    __wanted_competences: set[Competence]
    """
    Competences the user wants to achieve
    """

    __idx_semeseter_module_area_mapping: list[tuple[Semester, ModuleArea]]
    """
    Mapping of index of suggestion to semester. This mapping is sorted from lowest to highest semester
    """

    __module_mapping: list[Module]
    """
    Mapping of suggestion value to module
    """

    __baseline_competences_per_semester: dict[int, set[Competence]]
    """
    Mapping the number of a semester to the baseline competences
    """

    __sc: StandardCurriculum
    """
    Standard curriculum to get the suggestion for
    """

    __sem_to_pflichtmodules: set[tuple[Semester, Module]]
    """
    Mapping of semester to pflichtmodules
    """

    __modules_to_provided_competences: dict[Module, set[Competence]]
    """
    For each module map all competences provided by that module
    """

    __modules_to_required_competences: dict[Module, set[Competence]]
    """
    For each module map all competences required by that module
    """

    __module_area_to_module: dict[ModuleArea, set[Module]]
    """
    Maps a module area to all modules that fulfill that module area
    """

    def __init__(self, sc: StandardCurriculum, wanted_competences: set[Competence]):
        self.__wanted_competences = wanted_competences
        self.__baseline_competences_per_semester = {}
        self.__sc = sc
        self.__modules_to_provided_competences = {}
        self.__modules_to_required_competences = {}
        self.__module_area_to_module = {}

        self.__idx_semeseter_module_area_mapping = self.__gen_idx_sem_module_area_map()
        self.__sem_to_pflichtmodules = self.__get_all_semester_pflichtmodule()

        all_modules: set[Module] = set(sc.has_module.all())
        pflichtmodules: set[Module] = set([module for sem, module in self.__sem_to_pflichtmodules])
        self.__module_mapping = list(all_modules - pflichtmodules)

        for module in all_modules:
            self.__modules_to_provided_competences[module] = set(module.provides_competence.all())
            self.__modules_to_required_competences[module] = set(module.needs_competence.all())

            module_areas: set[ModuleArea] = set(module.fills_module_area.all())

            for module_area in module_areas:
                _modules = self.__module_area_to_module.get(module_area, set())
                self.__module_area_to_module[module_area] = _modules.union({module})

        semesters: list[Semester] = sc.specifies_semester.all()

        for semester in semesters:
            self.__baseline_competences_per_semester[semester.number] = self.__get_baseline_competences(semester)

    def __get_baseline_competences(self, semester: Semester) -> set[Competence]:
        """
        For each semester get all competences achieved by pflichtmodule up to that semester (not including the semester specified).

        :param sc: standard curricumum to get that information for
        :param semester: semester up to which to get the baseline competences for
        :return: a set of compteences acciebed by pflichtmodule up to that semester
        """

        competences: set[Competence] = set()

        # Get all pflichtmoduls up to the semester specified
        sem_modules: list[tuple[Semester, Module]] = list(
            filter(lambda x: x[0].number < semester.number, self.__sem_to_pflichtmodules))

        for semester, module in sem_modules:
            module_competences: list[Module] = module.provides_competence.all()

            competences = competences.union(set(module_competences))

        return competences

    def __get_all_semester_pflichtmodule(self) -> set[tuple[Semester, Module]]:
        """
        Get all pflcihtmodule for a standard curriculum mapped to their semesters that they're in
        :param sc: standard curiculum to get that information for
        :return: list of mapping from semester to module
        """

        sem_module: set[tuple[Semester, Module]] = set()

        semersters: list[Semester] = self.__sc.specifies_semester.all()

        for semester in semersters:
            module_cells: list[ModuleCell] = semester.contains_module_cell.all()

            for module_cell in module_cells:
                module_areas: list[ModuleArea] = module_cell.filled_by_module_area.all()
                for module_area in module_areas:
                    if len(module_area.filled_by_module.all()) == 1:
                        sem_module.add((semester, module_area.filled_by_module.single()))

        return sem_module

    def __get_all_semester_wpf(self) -> list[tuple[Semester, ModuleArea]]:
        """
        Get all wpf module areas for a standard curriculum mapped to their semesters that they're in
        :return: set of mapping from semester to module area
        """
        sem_module_area: list[tuple[Semester, ModuleArea]] = []

        semersters: list[Semester] = self.__sc.specifies_semester.all()
        for semester in semersters:
            module_cells: list[ModuleCell] = semester.contains_module_cell.all()
            for module_cell in module_cells:
                module_areas: list[ModuleArea] = module_cell.filled_by_module_area.all()
                for module_area in module_areas:
                    if len(module_area.filled_by_module.all()) > 1:
                        sem_module_area.append((semester, module_area))

        return sem_module_area

    def __gen_idx_sem_module_area_map(self) -> list[tuple[Semester, ModuleArea]]:
        """
        Get mapping for gene list
        :return: list of length of genes_list with semester numbers as values
        """

        sem_wpf_entries: list[tuple[Semester, ModuleArea]] = sorted(self.__get_all_semester_wpf(),
                                                                    key=lambda x: x[0].number)

        return sem_wpf_entries

    def __get_competences(self, semester: Semester, additional_modules: set[Module]) -> set[Competence]:
        """
        Similar to get_all_semester_pflichtmodule but also adds competences provided by additional modules
        :param semester: semester to get the baseline competences for.
            Baseline competences are competences that get provided by the modules up until the semester, excluding the semester.
            (If you set semester to 2, you get all competences provided by modules in semester 1)
        :param additional_modules: moduels which whos competences should be added to the baseline competences
        :return: baseline-competeces + competences from additional modules
        """

        competences: set[Competence] = self.__baseline_competences_per_semester[semester.number]

        for module in additional_modules:
            competences.union(self.__modules_to_provided_competences[module])

        return competences

    def __get_unmet_prerequisites_of_module(self, module: Module, semester: Semester,
                                            additional_modules: set[Module]) -> set[Competence]:
        """
        Get all required competences of a module that haven't been met yet at that semester including additional modules.
        :param module: Module to check if all competences are met
        :param semester: semester the module to check is in
        :param additional_modules: additional modules already taken
        :return: set of unmet competences
        """

        competences = self.__get_competences(semester, additional_modules)

        module_required_competences = self.__modules_to_required_competences[module]

        unmet_requirements = module_required_competences - competences

        return unmet_requirements

    def __module_fitness(self, module: Module, semester: Semester, additional_modules: set[Module]) -> float:
        """
        Fitness function for a module
        :param semester: semester the module is in
        :param additional_modules: additional modules already taken
        :param module: module to evaluate
        :return: fitness value
        """

        unmet_prerequisites = self.__get_unmet_prerequisites_of_module(module, semester, additional_modules)
        provided_competences: set[Competence] = self.__modules_to_provided_competences[module]

        if len(self.__wanted_competences) == 0:
            provided_wanted_competences_rating = 1.0
        else:
            # calculate fitness based on
            provided_wanted_competences_amount = len(provided_competences.intersection(self.__wanted_competences))
            provided_wanted_competences_rating = provided_wanted_competences_amount / len(self.__wanted_competences)

        # Check if suggested module requires competences that haven't been acquired yet
        unmet_prerequisites_rating = math.inf if len(unmet_prerequisites) > 0 else 0

        return provided_wanted_competences_rating - unmet_prerequisites_rating

    def __suggestion_to_semester_modules(self, suggestion: list[int]) -> list[tuple[ModuleArea, Semester, Module]]:
        """
        Convert a suggestion to a list of modules
        :param suggestion: suggestion generated by the genetic algorithm
        :return: list of modules from the suggestion mapped using the mapping. List is sorted from lowest to highest semester
        """

        modules: list[Module] = []
        module_sem: list[tuple[ModuleArea, Semester, Module]] = []

        for idx in suggestion:
            modules.append(self.__module_mapping[idx])

        for idx, module in enumerate(modules):
            module_sem.append((self.__idx_semeseter_module_area_mapping[idx][1],
                               self.__idx_semeseter_module_area_mapping[idx][0], module))

        return module_sem

    def __is_sem_summer(self, semester: Semester) -> bool:
        """
        Check if a semester is a summer semester
        :param semester: semester to check
        :return: True if summer semester, False otherwise
        """
        start_winter = self.__sc.start_winter

        if start_winter:
            return semester.number % 2 == 0
        else:
            return semester.number % 2 != 0

    def _fitness(self, ga_instance: GA, suggestion: list[int], suggestion_idx: int) -> float:
        """
        Fitness function for the genetic algorithm
        :param suggestion_idx: suggestion index
        :param ga_instance: GA instance
        :param suggestion: suggestion to evaluate
        :return: fitness value
        """

        start_winter = self.__sc.start_winter

        suggested_modules_to_sem: list[tuple[ModuleArea, Semester, Module]] = self.__suggestion_to_semester_modules(
            suggestion)
        suggested_unique_modules: set[Module] = set([module for _, sem, module in suggested_modules_to_sem])
        pflichtmodule: set[Module] = set([module for sem, module in self.__sem_to_pflichtmodules])

        # If module is more than once in the suggestion return -inf (invalid)
        if len(suggested_unique_modules) < len(suggested_modules_to_sem):
            return -math.inf

        # If one of the suggested modules is a pflichtmodule return -inf (invalid)
        if suggested_unique_modules.intersection(pflichtmodule):
            return -math.inf

        # Check if modules provided match their module areas
        for idx, (_, module_area) in enumerate(self.__idx_semeseter_module_area_mapping):
            suggested_module: Module = suggested_modules_to_sem[idx][2]
            allowed_modules_in_module_area: set[Module] = self.__module_area_to_module[module_area]
            if not suggested_module in allowed_modules_in_module_area:
                return -math.inf

        fitness_scores: list[float] = []

        for _, semester, module in suggested_modules_to_sem:
            # Get all additional visited modules up to (excluding) the current semester
            visited_modules = set(
                [module for _, sem, module in suggested_modules_to_sem if sem.number < semester.number])

            fitness_scores.append(self.__module_fitness(module, semester, visited_modules))

        return sum(fitness_scores) / len(fitness_scores)

    def __gen_suggested_wpf(self) -> tuple[list[tuple[ModuleArea, Semester, Module]], float]:
        """
        Get suggestion of WPF-Modules
        :return: list of (modulearea module fills, semester module should be taken, module), fitness score of suggestion (higher is better)
        """
        fitness_function = self._fitness

        num_generations = 50000
        num_parents_mating = 1

        sol_per_pop = 100
        num_genes = len(self.__idx_semeseter_module_area_mapping)

        # init_range_low = 0
        # init_range_high = len(self.__module_mapping) - 1

        parent_selection_type = "sss"
        keep_parents = 1

        crossover_type = "single_point"

        mutation_type = "random"
        mutation_percent_genes = 3 / len(self.__module_mapping) * 100
        ga_instance = GA(num_generations=num_generations,
                         num_parents_mating=num_parents_mating,
                         fitness_func=fitness_function,
                         sol_per_pop=sol_per_pop,
                         num_genes=num_genes,
                         gene_space={"low": 0, "high": len(self.__module_mapping) - 1},
                         gene_type=int,
                         parent_selection_type=parent_selection_type,
                         keep_parents=keep_parents,
                         crossover_type=crossover_type,
                         crossover_probability=0.0,
                         mutation_type=mutation_type,
                         mutation_percent_genes=mutation_percent_genes,
                         stop_criteria="saturate_1000",
                         allow_duplicate_genes=False)

        ga_instance.run()

        ga_instance.plot_fitness().savefig("fitness_plot.png")

        solution, score, _ = ga_instance.best_solution()

        modules: list[tuple[ModuleArea, Semester, Module]] = self.__suggestion_to_semester_modules(solution)
        print(score)

        return modules, score

    def gen_suggestion(self) -> tuple[list[tuple[ModuleArea | None, Semester, Module]], float]:
        """
        Genrate a full time table suggestion
        :return: list of (module area [is None if module is pflichtmodule], semester, module), fitness score of suggestion
        """
        res: list[tuple[ModuleArea | None, Semester, Module]] = []

        # Add pflichtmodules
        res += [(None, semester, module) for semester, module in self.__sem_to_pflichtmodules]

        suggestions, score = self.__gen_suggested_wpf()

        # Add suggested wpf modules
        res += suggestions

        return res, score
