from modul_graph.models.module_area import ModuleArea
from ._modules import *
from ._modules import softwareprojekt as softwareprojekt_module

"""
Module areas which are not assigned to a specific module 
"""
wpf_inf = ModuleArea()
wpf_inf.name = "WPF Informatik"
wpf_inf.save()

wpf_inf.filled_by_module.connect(computer_aided_geometric_design)
wpf_inf.filled_by_module.connect(computergraphik_i)
wpf_inf.filled_by_module.connect(computernetze)
wpf_inf.filled_by_module.connect(computernetze_2)
wpf_inf.filled_by_module.connect(einführung_in_digitale_spiele)
wpf_inf.filled_by_module.connect(grundlagen_der_bildverarbeitung)
wpf_inf.filled_by_module.connect(grundlagen_der_cpp_programmierung)
wpf_inf.filled_by_module.connect(grundzüge_der_algorithmischen_geometrie)
wpf_inf.filled_by_module.connect(idea_engineering)
wpf_inf.filled_by_module.connect(interaktive_systeme)
wpf_inf.filled_by_module.connect(introduction_to_deep_learning)
wpf_inf.filled_by_module.connect(introduction_to_robotics)
wpf_inf.filled_by_module.connect(introduction_to_simulation)
wpf_inf.filled_by_module.connect(maschinelles_lernen)
wpf_inf.filled_by_module.connect(mesh_processing)
wpf_inf.filled_by_module.connect(neuronale_netze)
wpf_inf.filled_by_module.connect(parallele_programmierung)
wpf_inf.filled_by_module.connect(usability_und_ästhetik)
wpf_inf.filled_by_module.connect(visualisierung)

wpf_inf_mat = ModuleArea()
wpf_inf_mat.name = "WPF Informatik oder Mathematik"
wpf_inf_mat.save()

wpf_inf_mat.filled_by_module.connect(computer_aided_geometric_design)
wpf_inf_mat.filled_by_module.connect(computergraphik_i)
wpf_inf_mat.filled_by_module.connect(computernetze)
wpf_inf_mat.filled_by_module.connect(computernetze_2)
wpf_inf_mat.filled_by_module.connect(einführung_in_digitale_spiele)
wpf_inf_mat.filled_by_module.connect(grundlagen_der_bildverarbeitung)
wpf_inf_mat.filled_by_module.connect(grundlagen_der_cpp_programmierung)
wpf_inf_mat.filled_by_module.connect(grundzüge_der_algorithmischen_geometrie)
wpf_inf_mat.filled_by_module.connect(idea_engineering)
wpf_inf_mat.filled_by_module.connect(interaktive_systeme)
wpf_inf_mat.filled_by_module.connect(introduction_to_deep_learning)
wpf_inf_mat.filled_by_module.connect(parallele_programmierung)
wpf_inf_mat.filled_by_module.connect(introduction_to_simulation)
wpf_inf_mat.filled_by_module.connect(maschinelles_lernen)
wpf_inf_mat.filled_by_module.connect(mesh_processing)
wpf_inf_mat.filled_by_module.connect(neuronale_netze)
wpf_inf_mat.filled_by_module.connect(parallele_programmierung)
wpf_inf_mat.filled_by_module.connect(usability_und_ästhetik)
wpf_inf_mat.filled_by_module.connect(visualisierung)

wpf_ti = ModuleArea()
wpf_ti.name = "WPF Technische Informatik"
wpf_ti.save()

wpf_ti.filled_by_module.connect(computernetze)
wpf_ti.filled_by_module.connect(computernetze_2)
wpf_ti.filled_by_module.connect(parallele_programmierung)
wpf_ti.filled_by_module.connect(parallele_programmierung)

nebenfach = ModuleArea()
nebenfach.name = "Nebenfach"
nebenfach.save()
nebenfach.filled_by_module.connect(dummy)

trainingsmodul_smk = ModuleArea()
trainingsmodul_smk.name = "Trainingsmodul SMK"
trainingsmodul_smk.save()

trainingsmodul_smk.filled_by_module.connect(trainingsmodul_schlüssel_und_methodenkompetenz_)

softwareproject = ModuleArea()
softwareproject.name = "Softwareprojekt"
softwareproject.save()

softwareproject.filled_by_module.connect(softwareprojekt_module)

wiss_seminar = ModuleArea()
wiss_seminar.name = "Wiss. Seminar"
wiss_seminar.save()

wiss_seminar.filled_by_module.connect(wissenschaftliches_seminar)

wpf_fin_smk = ModuleArea()
wpf_fin_smk.name = "WPF FIN-SMK"
wpf_fin_smk.save()
wpf_fin_smk.filled_by_module.connect(dummy)

ba_praktikum = ModuleArea()
ba_praktikum.name = "Betriebspraktikum/Bachelorprojekt und Bachelorarbeit"
ba_praktikum.save()
ba_praktikum.filled_by_module.connect(bachelorarbeit)

"""
Module areas with a specific module assigned to them
"""

einf_inf = ModuleArea()
einf_inf.name = "Einführung in die Informatik"
einf_inf.save()

einf_inf.filled_by_module.connect(einführung_in_die_informatik)

datenbanken = ModuleArea()
datenbanken.name = "Datenbanken"
datenbanken.save()

datenbanken.filled_by_module.connect(datenbanken_module)

ti_1 = ModuleArea()
ti_1.name = "Technische Informatik 1"
ti_1.save()

ti_1.filled_by_module.connect(technische_informatik_i)

mathe_1 = ModuleArea()
mathe_1.name = "Mathematiname"
mathe_1.save()

mathe_1.filled_by_module.connect(mathematik_i)

schlüko_1 = ModuleArea()
schlüko_1.name = "Schlüsselkompetenzen 1"
schlüko_1.save()

schlüko_1.filled_by_module.connect(schlüsselkompetenzen_i)

schlüko_2 = ModuleArea()
schlüko_2.name = "Schlüsselkompetenzen 2"
schlüko_2.save()

schlüko_2.filled_by_module.connect(schlüsselkompetenzen_ii)

aud = ModuleArea()
aud.name = "Algorithmen und Datenstrukturen"
aud.save()

aud.filled_by_module.connect(algorithmen_und_datenstrukturen)

modellierung = ModuleArea()
modellierung.name = "Modellierung"
modellierung.save()

modellierung.filled_by_module.connect(modellierung_module)

ti_2 = ModuleArea()
ti_2.name = "Technische Informatik 2"
ti_2.save()

ti_2.filled_by_module.connect(technische_informatik_ii)

mathe_2 = ModuleArea()
mathe_2.name = "Mathematik 2"
mathe_2.save()

mathe_2.filled_by_module.connect(mathematik_ii)

logik = ModuleArea()
logik.name = "Logik"
logik.save()

logik.filled_by_module.connect(logik_module)

i_s = ModuleArea()
i_s.name = "Intelligente Systeme"
i_s.save()

i_s.filled_by_module.connect(intelligente_systeme)

itpm = ModuleArea()
itpm.name = "IT-Projektmanagement"
itpm.save()

itpm.filled_by_module.connect(it_projektmanagement)

mathe_3 = ModuleArea()
mathe_3.name = "Mathematik"
mathe_3.save()

mathe_3.filled_by_module.connect(mathematik_iii)

theo_inf_1 = ModuleArea()
theo_inf_1.name = "Grundlagen der Theo. Informatiname"
theo_inf_1.save()

theo_inf_1.filled_by_module.connect(grundlagen_der_theoretischen_informatik)

sisi = ModuleArea()
sisi.name = "Sichere Systeme"
sisi.save()

sisi.filled_by_module.connect(sichere_systeme)

pgp = ModuleArea()
pgp.name = "Programmierparadigmen"
pgp.save()

pgp.filled_by_module.connect(programmierparadigmen)

se = ModuleArea()
se.name = "Software Engineering"
se.save()

se.filled_by_module.connect(software_engineering_)

theo_inf_2 = ModuleArea()
theo_inf_2.name = "Grundlagen der Theo. Informatik 2"
theo_inf_2.save()

theo_inf_2.filled_by_module.connect(grundlagen_der_theoretischen_informatik_ii)
