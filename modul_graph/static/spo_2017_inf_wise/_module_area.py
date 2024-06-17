from modul_graph.models.module_area import ModuleArea


"""
Module areas which are not assigned to a specific module 
"""
wpf_inf = ModuleArea()
wpf_inf.name = "WPF Informatik"
wpf_inf.save()

wpf_inf_mat = ModuleArea()
wpf_inf_mat.name = "WPF Informatik oder Mathematik"
wpf_inf_mat.save()

wpf_ti = ModuleArea()
wpf_ti.name = "WPF Technische Informatik"
wpf_ti.save()

nebenfach = ModuleArea()
nebenfach.name = "Nebenfach"
nebenfach.save()

trainingsmodul_smk = ModuleArea()
trainingsmodul_smk.name = "Trainingsmodul SMK"
trainingsmodul_smk.save()

softwareproject = ModuleArea()
softwareproject.name = "Softwareprojekt"
softwareproject.save()

wiss_seminar = ModuleArea()
wiss_seminar.name = "Wiss. Seminar"
wiss_seminar.save()

wpf_fin_smk = ModuleArea()
wpf_fin_smk.name = "WPF FIN-SMK"
wpf_fin_smk.save()


ba_praktikum = ModuleArea()
ba_praktikum.name = "Betriebspraktikum/Bachelorprojekt und Bachelorarbeit"
ba_praktikum.save()


"""
Module areas with a specific module assigned to them
"""

einf_inf = ModuleArea()
einf_inf.name = "Einführung in die Informatik"
einf_inf.save()

datenbanken = ModuleArea()
datenbanken.name = "Datenbanken"
datenbanken.save()

ti_1 = ModuleArea()
ti_1.name = "Technische Informatik 1"
ti_1.save()

mathe_1 = ModuleArea()
mathe_1.name = "Mathematiname"
mathe_1.save()

schlüko_1 = ModuleArea()
schlüko_1.name = "Schlüsselkompetenzen 1"
schlüko_1.save()

schlüko_2 = ModuleArea()
schlüko_2.name = "Schlüsselkompetenzen 2"
schlüko_2.save()

aud = ModuleArea()
aud.name = "Algorithmen und Datenstrukturen"
aud.save()

modellierung = ModuleArea()
modellierung.name = "Modellierung"
modellierung.save()

ti_2 = ModuleArea()
ti_2.name = "Technische Informatik 2"
ti_2.save()

mathe_2 = ModuleArea()
mathe_2.name = "Mathematik 2"
mathe_2.save()

logik = ModuleArea()
logik.name = "Logik"
logik.save()

i_s = ModuleArea()
i_s.name = "Intelligente Systeme"
i_s.save()

itpm = ModuleArea()
itpm.name = "IT-Projektmanagement"
itpm.save()

mathe_3 = ModuleArea()
mathe_3.name = "Mathematik"
mathe_3.save()

theo_inf_1 = ModuleArea()
theo_inf_1.name = "Grundlagen der Theo. Informatiname"
theo_inf_1.save()

sisi = ModuleArea()
sisi.name = "Sichere Systeme"
sisi.save()

pgp = ModuleArea()
pgp.name = "Programmierparadigmen"
pgp.save()

se = ModuleArea()
se.name = "Software Engineering"
se.save()

theo_inf_2 = ModuleArea()
theo_inf_2.name = "Grundlagen der Theo. Informatik 2"
theo_inf_2.save()




