from modul_graph.models.module import Module
from modul_graph.static.spo_2017_inf_wise._competences import *
from modul_graph.static.spo_2017_inf_wise._competences import algorithmen_und_datenstrukturen as algorithmen_und_datenstrukturen_


algorithmen_und_datenstrukturen = Module()
algorithmen_und_datenstrukturen.name = "Algorithmen und Datenstrukturen"
algorithmen_und_datenstrukturen.cp_plus_description = {'DEFAULT':6.0}
algorithmen_und_datenstrukturen.module_description = "- Listen - Bäume, Balancierte Suchbäume - Hashverfahren - Graphen - Dynamische Programmierung - Entwurf von Algorithmen - Suche in Texten"
algorithmen_und_datenstrukturen.is_in_summer = True
algorithmen_und_datenstrukturen.is_in_winter = True
algorithmen_und_datenstrukturen.save()

algorithmen_und_datenstrukturen.needs_competence.connect(algorithmen_und_datenstrukturen_)
algorithmen_und_datenstrukturen.needs_competence.connect(betriebssysteme)
algorithmen_und_datenstrukturen.needs_competence.connect(analysis)
algorithmen_und_datenstrukturen.needs_competence.connect(datenbanken_und_informationssysteme)
algorithmen_und_datenstrukturen.needs_competence.connect(numerik)
algorithmen_und_datenstrukturen.provides_competence.connect(analysis)
algorithmen_und_datenstrukturen.provides_competence.connect(algorithmen_und_datenstrukturen_)

bachelorarbeit = Module()
bachelorarbeit.name = "Bachelorarbeit"
bachelorarbeit.cp_plus_description = {'DEFAULT':12.0}
bachelorarbeit.module_description = "Das Thema der Bachelorarbeit kann aus aktuellen Forschungsvorhaben der Institute oder aus betrieblichen Problemstellungen mit wissenschaftlichem Charakter abgeleitet werden. Ausgegeben wird die Aufgabenstellung immer von einem Hochschullehrer, der am Studiengang beteiligten Fakultäten. Im Kolloquium haben die Studierenden nachzuweisen, dass sie in der Lage sind, die Arbeitsergebnisse aus der wissenschaftlichen Bearbeitung eines Fachgebietes in einem Fachgespräch zu verteidigen. In dem Kolloquium sollen das Thema der Bachelorarbeit und die damit verbundenen Probleme und Erkenntnisse in einem Vortrag dargestellt und diesbezügliche Fragen beantwortet werden."
bachelorarbeit.is_in_summer = True
bachelorarbeit.is_in_winter = True
bachelorarbeit.save()

bachelorarbeit.needs_competence.connect(analysis)
bachelorarbeit.needs_competence.connect(algorithmen_und_datenstrukturen_)
bachelorarbeit.provides_competence.connect(analysis)
bachelorarbeit.provides_competence.connect(algorithmen_und_datenstrukturen_)
bachelorarbeit.provides_competence.connect(betriebssysteme)
bachelorarbeit.provides_competence.connect(numerik)

computer_aided_geometric_design = Module()
computer_aided_geometric_design.name = "Computer Aided Geometric Design"
computer_aided_geometric_design.cp_plus_description = {'DEFAULT':5.0}
computer_aided_geometric_design.module_description = "Differentialgeometrie von Kurven und FlächenBezier-Kurven Bezier-Spline Kurven B-Spline-Kurven Rationale Kurven Polarformen Tensorprodukt Bezier- und B-Spline Flächen Bezierflächen über Dreiecken Surface interrogation and fairing Subdivision curves and surfaces"
computer_aided_geometric_design.is_in_summer = True
computer_aided_geometric_design.is_in_winter = True
computer_aided_geometric_design.save()

computer_aided_geometric_design.needs_competence.connect(analysis)
computer_aided_geometric_design.needs_competence.connect(algorithmen_und_datenstrukturen_)
computer_aided_geometric_design.needs_competence.connect(numerik)
computer_aided_geometric_design.provides_competence.connect(algorithmen_und_datenstrukturen_)
computer_aided_geometric_design.provides_competence.connect(betriebssysteme)
computer_aided_geometric_design.provides_competence.connect(analysis)
computer_aided_geometric_design.provides_competence.connect(datenbanken_und_informationssysteme)
computer_aided_geometric_design.provides_competence.connect(numerik)

computergraphik_i = Module()
computergraphik_i.name = "Computergraphik I"
computergraphik_i.cp_plus_description = {'DEFAULT':5.0}
computergraphik_i.module_description = "Einführung, Geschichte, Anwendungsgebiete der ComputergraphikModellierung und Akquisition graphischer Daten Graphische Anwendungsprogrammierung Transformationen Clipping Rasterisierung und Antialiasing Beleuchtung Radiosity Texturierung Sichtbarkeit Raytracing Moderne Konzepte der Computergraphik im Überblick"
computergraphik_i.is_in_summer = True
computergraphik_i.is_in_winter = True
computergraphik_i.save()

computergraphik_i.needs_competence.connect(analysis)
computergraphik_i.needs_competence.connect(algorithmen_und_datenstrukturen_)
computergraphik_i.needs_competence.connect(betriebssysteme)
computergraphik_i.needs_competence.connect(numerik)
computergraphik_i.provides_competence.connect(analysis)
computergraphik_i.provides_competence.connect(algorithmen_und_datenstrukturen_)
computergraphik_i.provides_competence.connect(numerik)

computernetze = Module()
computernetze.name = "Computernetze"
computernetze.cp_plus_description = {'DEFAULT':5.0}
computernetze.module_description = "Inhalte Grundlegende Protokolle und Ansätze von der Bitübertragungsschicht bis zur Anwendungsschicht ISO/OSI-Architektur vs TCP/IP-Architektur Datenübertragung Medienzugriffskontrolle Fehlerbehandlung Zuverlässige Nachrichtenübertragung Kommunikationssicherheit Basisdienste auf Anwendungsebene"
computernetze.is_in_summer = True
computernetze.is_in_winter = True
computernetze.save()

computernetze.needs_competence.connect(algorithmen_und_datenstrukturen_)
computernetze.provides_competence.connect(analysis)
computernetze.provides_competence.connect(algorithmen_und_datenstrukturen_)

computernetze_2 = Module()
computernetze_2.name = "Computernetze 2"
computernetze_2.cp_plus_description = {'DEFAULT':5.0}
computernetze_2.module_description = "Inhalte Grundlegende Protokolle und Ansätze bis zur AnwendungsschichtISO/OSI-Architektur vs TCP/IP-ArchitekturInternet-ProtokolleProtokolle der Transportschicht TCP, UDPProtokolle der AnwendungsschichtKommunikationssicherheitProtokolle und Dienste der Anwendungsschicht Protokolle für das Internet der Dinge"
computernetze_2.is_in_summer = True
computernetze_2.is_in_winter = True
computernetze_2.save()

computernetze_2.needs_competence.connect(algorithmen_und_datenstrukturen_)
computernetze_2.provides_competence.connect(analysis)
computernetze_2.provides_competence.connect(algorithmen_und_datenstrukturen_)
computernetze_2.provides_competence.connect(numerik)

datenbanken_module = Module()
datenbanken_module.name = "Datenbanken"
datenbanken_module.cp_plus_description = {'DEFAULT':5.0}
datenbanken_module.module_description = "Eigenschaften von DatenbanksystemenArchitekturen Konzeptueller Entwurf einer relationalen Datenbank Relationales Datenbankmodell Abbildung ER-Schema auf Relationen Datenbanksprachen (Relationenalgebra, SQL) Formale Entwurfskriterien und Normalisierungstheorie Anwendungsprogrammierung Weitere Datenbankkonzepte wie Sichten, Trigger, Rechtevergabe"
datenbanken_module.is_in_summer = True
datenbanken_module.is_in_winter = True
datenbanken_module.save()

datenbanken_module.needs_competence.connect(analysis)
datenbanken_module.needs_competence.connect(algorithmen_und_datenstrukturen_)
datenbanken_module.needs_competence.connect(numerik)

einführung_in_die_informatik = Module()
einführung_in_die_informatik.name = "Einführung in die Informatik"
einführung_in_die_informatik.cp_plus_description = {'DEFAULT':8.0}
einführung_in_die_informatik.module_description = "Grundkonzepte in JavaFunktionen Objektorientierte Programmierung Programmierparadigmen Ausgewählte Algorithmen: Suchen und Sortieren Analyse von Algorithmen: Korrektheit und Komplexität Grundlegende Datenstrukturen und abstrakte Datentypen Berechenbarkeit und Entscheidbarkeit"
einführung_in_die_informatik.is_in_summer = True
einführung_in_die_informatik.is_in_winter = True
einführung_in_die_informatik.save()

einführung_in_die_informatik.needs_competence.connect(analysis)
einführung_in_die_informatik.needs_competence.connect(algorithmen_und_datenstrukturen_)
einführung_in_die_informatik.needs_competence.connect(betriebssysteme)
einführung_in_die_informatik.needs_competence.connect(numerik)

einführung_in_digitale_spiele = Module()
einführung_in_digitale_spiele.name = "Einführung in Digitale Spiele"
einführung_in_digitale_spiele.cp_plus_description = {'DEFAULT':5.0}
einführung_in_digitale_spiele.module_description = "Game DesignGame Development Software Patterns2D-3D Math Game ConceptsCameras, Rendering, AnimationsLights, Shadows, ShaderPhysic Engines, CollisionsAudio EnginePathfinding, Steering, NavigationProcedural Content GenerationGame AIPrototyping, Playtesting, Publishing"
einführung_in_digitale_spiele.is_in_summer = True
einführung_in_digitale_spiele.is_in_winter = True
einführung_in_digitale_spiele.save()

einführung_in_digitale_spiele.needs_competence.connect(analysis)
einführung_in_digitale_spiele.needs_competence.connect(algorithmen_und_datenstrukturen_)
einführung_in_digitale_spiele.needs_competence.connect(numerik)
einführung_in_digitale_spiele.provides_competence.connect(analysis)
einführung_in_digitale_spiele.provides_competence.connect(algorithmen_und_datenstrukturen_)
einführung_in_digitale_spiele.provides_competence.connect(numerik)

ethische_herausforderungen_im_digitalen_zeitalter = Module()
ethische_herausforderungen_im_digitalen_zeitalter.name = "Ethische Herausforderungen im Digitalen Zeitalter"
ethische_herausforderungen_im_digitalen_zeitalter.cp_plus_description = {'DEFAULT':3.0}
ethische_herausforderungen_im_digitalen_zeitalter.module_description = "Definition von Ethik Deskriptive Ethik Begründung von Ethik Teleologische Ethik Deontologische Ethik Chancen der Digitalisierung Schranken der kommerziellen Verwertbarkeit von Daten Ethische Herausforderung im Umgang mit persönlichen Daten / Metadaten Erweiterung des Realitätsbegriffes Künstliche Intelligenz und Technologische Singularität Anwendungsgebiete der Digitalisierung VertriebMobilität (Autonomes Fahren; Smart Cars)Autonome Entscheidungen von MaschinenIntelligente, Vernetzte Produktion, Industrie 4.0Autonome Kriegsführung"
ethische_herausforderungen_im_digitalen_zeitalter.is_in_summer = True
ethische_herausforderungen_im_digitalen_zeitalter.is_in_winter = True
ethische_herausforderungen_im_digitalen_zeitalter.save()

ethische_herausforderungen_im_digitalen_zeitalter.needs_competence.connect(analysis)
ethische_herausforderungen_im_digitalen_zeitalter.needs_competence.connect(algorithmen_und_datenstrukturen_)
ethische_herausforderungen_im_digitalen_zeitalter.needs_competence.connect(betriebssysteme)
ethische_herausforderungen_im_digitalen_zeitalter.needs_competence.connect(numerik)
ethische_herausforderungen_im_digitalen_zeitalter.provides_competence.connect(analysis)
ethische_herausforderungen_im_digitalen_zeitalter.provides_competence.connect(algorithmen_und_datenstrukturen_)

grundlagen_der_bildverarbeitung = Module()
grundlagen_der_bildverarbeitung.name = "Grundlagen der Bildverarbeitung"
grundlagen_der_bildverarbeitung.cp_plus_description = {'DEFAULT':5.0}
grundlagen_der_bildverarbeitung.module_description = "Digitale Bildverarbeitung als algorithmisches ProblemVerarbeitung mehrdimensionaler, digitaler Signale Methoden der Bildverbesserung Grundlegende Segmentierungsverfahren"
grundlagen_der_bildverarbeitung.is_in_summer = True
grundlagen_der_bildverarbeitung.is_in_winter = True
grundlagen_der_bildverarbeitung.save()

grundlagen_der_bildverarbeitung.needs_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_bildverarbeitung.needs_competence.connect(betriebssysteme)
grundlagen_der_bildverarbeitung.needs_competence.connect(digitaltechnik_und_rechnerorganisation)
grundlagen_der_bildverarbeitung.needs_competence.connect(analysis)
grundlagen_der_bildverarbeitung.needs_competence.connect(datenbanken_und_informationssysteme)
grundlagen_der_bildverarbeitung.needs_competence.connect(numerik)
grundlagen_der_bildverarbeitung.provides_competence.connect(analysis)
grundlagen_der_bildverarbeitung.provides_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_bildverarbeitung.provides_competence.connect(betriebssysteme)
grundlagen_der_bildverarbeitung.provides_competence.connect(numerik)

grundlagen_der_cpp_programmierung = Module()
grundlagen_der_cpp_programmierung.name = "Grundlagen der C++ Programmierung"
grundlagen_der_cpp_programmierung.cp_plus_description = {'DEFAULT':5.0}
grundlagen_der_cpp_programmierung.module_description = "Bedienung des Compilers und Zusammenspiel mit LinkerPrimitive Datentypen, Operatoren und Kontrollfluss (und Unterschiede zu Java) Variablen, Felder, Zeiger und Zeigerarithmetik Funktionen Klassen Speicherverwaltung, Referenzen, Ausnahmebehandlung Überladen von Operatoren Generische Programmierung mit templates Überblick über die Standardbibliothek inklusive STL Werkzeuge (debugger, make, valgrind, doxygen) Allgemeine Problematiken (z.B. Programmierstil, Quellcode-Verwaltung, Optimierung, Zeichensätze/UTF-8)"
grundlagen_der_cpp_programmierung.is_in_summer = True
grundlagen_der_cpp_programmierung.is_in_winter = True
grundlagen_der_cpp_programmierung.save()

grundlagen_der_cpp_programmierung.needs_competence.connect(analysis)
grundlagen_der_cpp_programmierung.needs_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_cpp_programmierung.provides_competence.connect(analysis)
grundlagen_der_cpp_programmierung.provides_competence.connect(algorithmen_und_datenstrukturen_)

grundlagen_der_theoretischen_informatik = Module()
grundlagen_der_theoretischen_informatik.name = "Grundlagen der Theoretischen Informatik"
grundlagen_der_theoretischen_informatik.cp_plus_description = {'DEFAULT':5.0}
grundlagen_der_theoretischen_informatik.module_description = "Einführung in Formale Sprachen (reguläre Sprachen und Grammatiken), elementare Automatentheorie (endliche Automaten, Kellerautomaten), Berechnungsmodelle und Churchsche These, Entscheidbarkeit und Semi-Entscheidbarkeit, Komplexitätsklassen P und NP, NP-Vollständigkeit"
grundlagen_der_theoretischen_informatik.is_in_summer = True
grundlagen_der_theoretischen_informatik.is_in_winter = True
grundlagen_der_theoretischen_informatik.save()

grundlagen_der_theoretischen_informatik.needs_competence.connect(analysis)
grundlagen_der_theoretischen_informatik.needs_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_theoretischen_informatik.needs_competence.connect(numerik)
grundlagen_der_theoretischen_informatik.provides_competence.connect(analysis)
grundlagen_der_theoretischen_informatik.provides_competence.connect(algorithmen_und_datenstrukturen_)

grundlagen_der_theoretischen_informatik_ii = Module()
grundlagen_der_theoretischen_informatik_ii.name = "Grundlagen der Theoretischen Informatik II"
grundlagen_der_theoretischen_informatik_ii.cp_plus_description = {'DEFAULT':5.0}
grundlagen_der_theoretischen_informatik_ii.module_description = " Weiterführendes zu Formalen Sprachen (Kleene Algebra, Homomorphismen, Normalformen von Grammatiken) und Automaten (Varianten, Zustandsminimierung), Äquivalenz verschiedener Berechnungsmodelle (beispielsweise Turingmaschinen,  Regsitermaschinen, primitiv rekursive und mu-rekursive Funktionen, Grammatiken), weitere unentscheidbare und NP-vollständige Probleme."
grundlagen_der_theoretischen_informatik_ii.is_in_summer = True
grundlagen_der_theoretischen_informatik_ii.is_in_winter = True
grundlagen_der_theoretischen_informatik_ii.save()

grundlagen_der_theoretischen_informatik_ii.needs_competence.connect(analysis)
grundlagen_der_theoretischen_informatik_ii.needs_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_theoretischen_informatik_ii.needs_competence.connect(numerik)
grundlagen_der_theoretischen_informatik_ii.provides_competence.connect(analysis)
grundlagen_der_theoretischen_informatik_ii.provides_competence.connect(algorithmen_und_datenstrukturen_)
grundlagen_der_theoretischen_informatik_ii.provides_competence.connect(numerik)

grundzüge_der_algorithmischen_geometrie = Module()
grundzüge_der_algorithmischen_geometrie.name = "Grundzüge der Algorithmischen Geometrie"
grundzüge_der_algorithmischen_geometrie.cp_plus_description = {'DEFAULT':5.0}
grundzüge_der_algorithmischen_geometrie.module_description = "Plane-Sweep und Teile-und-Herrsche als Entwurfsprinzipien für geometrische Algorithmen, Konvexe Hülle, Triangulierung von Punktmengen und Polygonen, Datenstrukturen für Punktlokalisierung und Bereichsanfragen. Einfache geometrische Fragestellungen mit Anwendungen in der Computervisualistik"
grundzüge_der_algorithmischen_geometrie.is_in_summer = True
grundzüge_der_algorithmischen_geometrie.is_in_winter = True
grundzüge_der_algorithmischen_geometrie.save()

grundzüge_der_algorithmischen_geometrie.needs_competence.connect(analysis)
grundzüge_der_algorithmischen_geometrie.needs_competence.connect(algorithmen_und_datenstrukturen_)
grundzüge_der_algorithmischen_geometrie.needs_competence.connect(numerik)
grundzüge_der_algorithmischen_geometrie.provides_competence.connect(algorithmen_und_datenstrukturen_)

idea_engineering = Module()
idea_engineering.name = "Idea Engineering"
idea_engineering.cp_plus_description = {'DEFAULT':5.0}
idea_engineering.module_description = "InnovationsprozessGrundlagen von Ideenfindungstechniken Perspektivwechsel Bewertung von Ideen Selektion und Ausbau von Ideen Klassische Kreativitätstechniken Werbeideenproduktion"
idea_engineering.is_in_summer = True
idea_engineering.is_in_winter = True
idea_engineering.save()

idea_engineering.needs_competence.connect(algorithmen_und_datenstrukturen_)
idea_engineering.provides_competence.connect(algorithmen_und_datenstrukturen_)

intelligente_systeme = Module()
intelligente_systeme.name = "Intelligente Systeme"
intelligente_systeme.cp_plus_description = {'DEFAULT':5.0}
intelligente_systeme.module_description = "Eigenschaften intelligenter Systeme Modellierungstechniken für wissensintensive Anwendungen Subsymbolische Lösungsverfahren Heuristische Suchverfahren Lernende Systeme Modellansätze für kognitive Systeme Wissensrevision und Ontologien Entscheidungsunterstützende Systeme Weitere aktuelle Methoden für die Entwicklung Intelligenter Systeme wie Kausale Netze, Unscharfes Schließen"
intelligente_systeme.is_in_summer = True
intelligente_systeme.is_in_winter = True
intelligente_systeme.save()

intelligente_systeme.needs_competence.connect(algorithmen_und_datenstrukturen_)
intelligente_systeme.needs_competence.connect(betriebssysteme)
intelligente_systeme.needs_competence.connect(digitaltechnik_und_rechnerorganisation)
intelligente_systeme.needs_competence.connect(analysis)
intelligente_systeme.needs_competence.connect(datenbanken_und_informationssysteme)
intelligente_systeme.needs_competence.connect(diskrete_strukturen)
intelligente_systeme.needs_competence.connect(logik)
intelligente_systeme.needs_competence.connect(algebra)
intelligente_systeme.needs_competence.connect(numerik)
intelligente_systeme.provides_competence.connect(algorithmen_und_datenstrukturen_)
intelligente_systeme.provides_competence.connect(betriebssysteme)
intelligente_systeme.provides_competence.connect(analysis)
intelligente_systeme.provides_competence.connect(datenbanken_und_informationssysteme)
intelligente_systeme.provides_competence.connect(numerik)

interaktive_systeme = Module()
interaktive_systeme.name = "Interaktive Systeme"
interaktive_systeme.cp_plus_description = {'DEFAULT':5.0}
interaktive_systeme.module_description = "Technische Grundlagen der Mensch-Computer-Interaktion (Fenster-, Menü- und Dialogsysteme) Interaktionstechniken und Interaktionsaufgaben Kognitive Grundlagen der Mensch-Computer-Interaktion Analyse von Aufgaben und Benutzern Prototypentwicklung und EvaluierungSpezifikation von Benutzungsschnittstellen"
interaktive_systeme.is_in_summer = True
interaktive_systeme.is_in_winter = True
interaktive_systeme.save()

interaktive_systeme.needs_competence.connect(algorithmen_und_datenstrukturen_)
interaktive_systeme.needs_competence.connect(betriebssysteme)
interaktive_systeme.needs_competence.connect(analysis)
interaktive_systeme.needs_competence.connect(datenbanken_und_informationssysteme)
interaktive_systeme.needs_competence.connect(numerik)
interaktive_systeme.provides_competence.connect(algorithmen_und_datenstrukturen_)

introduction_to_deep_learning = Module()
introduction_to_deep_learning.name = "Introduction to Deep Learning"
introduction_to_deep_learning.cp_plus_description = {'DEFAULT':10.0}
introduction_to_deep_learning.module_description = "- artificial neural network fundamentals (gradient descent & backpropagation, activation functions) - network architectures (Convolutional Neural Networks, Recurrent/Recursive Neural Networks, Auto-Encoders) - regularization techniques - introspection & analysis techniques - optimization techniques - advanced training strategies (e.g. teacher-student)"
introduction_to_deep_learning.is_in_summer = True
introduction_to_deep_learning.is_in_winter = True
introduction_to_deep_learning.save()

introduction_to_deep_learning.needs_competence.connect(analysis)
introduction_to_deep_learning.needs_competence.connect(algorithmen_und_datenstrukturen_)
introduction_to_deep_learning.provides_competence.connect(analysis)
introduction_to_deep_learning.provides_competence.connect(algorithmen_und_datenstrukturen_)
introduction_to_deep_learning.provides_competence.connect(numerik)

introduction_to_robotics = Module()
introduction_to_robotics.name = "Introduction to Robotics"
introduction_to_robotics.cp_plus_description = {'DEFAULT':5.0}
introduction_to_robotics.module_description = "The lecture Introduction to Robotics will teach students the fundamental concepts of robotics from a top-down perspective, focused on mobile robots. The lecture starts with some exemplary robotic systems to show the variety of system in action today. Afterwards, multiple views on robotics systems are shown, which highlight different aspects like communication, behavior, movement, and system setup. The lecture continues with a description of multiple communication paradigms typically used in the robotic context and their relation to physical communication mechanisms. The next topic highlights some components typically found for perception and actuation like cameras, LiDARs, Distance Sensors, linear and revolute motors and piezo actuators. Afterwards, mechanisms to combine perception and actuation using low-level control mechanisms are shown. The shown mechanisms are reactive behaviors based on rule-sets and state-machines and feed-back-based control. Additionally, some kinematic models for movement of robots are highlighted like differential drive, Ackerman steering and holonomic movement. The next part of the lecture focus on localization of mobile robots using external mechanisms like Triangulation and Trilateration and internal mechanisms like SLAM and landmark tracking. The last two parts of the lecture discuss algorithms for path- and trajectory planning, and the extension to multi-robot systems. The exercises to the lecture will highlight the concepts of the lecture with practical examples based on robotic simulations in ROS with the Gazebo simulator."
introduction_to_robotics.is_in_summer = True
introduction_to_robotics.is_in_winter = True
introduction_to_robotics.save()

introduction_to_robotics.needs_competence.connect(analysis)
introduction_to_robotics.needs_competence.connect(algorithmen_und_datenstrukturen_)
introduction_to_robotics.needs_competence.connect(numerik)
introduction_to_robotics.provides_competence.connect(analysis)
introduction_to_robotics.provides_competence.connect(algorithmen_und_datenstrukturen_)

introduction_to_simulation = Module()
introduction_to_simulation.name = "Introduction to Simulation"
introduction_to_simulation.cp_plus_description = {'DEFAULT':5.0}
introduction_to_simulation.module_description = "ereignisorientierte Simulation Zufallsvariablen Zufallszahlenerzeugung statistische Datenanalyse gewöhnliche Differentialgleichungen numerische Integration stochastische Petri-Netze AnyLogic Simulationssystem zeitdiskrete Markov Ketten agentenbasierte Simulation"
introduction_to_simulation.is_in_summer = True
introduction_to_simulation.is_in_winter = True
introduction_to_simulation.save()

introduction_to_simulation.needs_competence.connect(algorithmen_und_datenstrukturen_)
introduction_to_simulation.needs_competence.connect(betriebssysteme)
introduction_to_simulation.needs_competence.connect(digitaltechnik_und_rechnerorganisation)
introduction_to_simulation.needs_competence.connect(analysis)
introduction_to_simulation.needs_competence.connect(datenbanken_und_informationssysteme)
introduction_to_simulation.needs_competence.connect(numerik)
introduction_to_simulation.provides_competence.connect(algorithmen_und_datenstrukturen_)
introduction_to_simulation.provides_competence.connect(betriebssysteme)
introduction_to_simulation.provides_competence.connect(analysis)
introduction_to_simulation.provides_competence.connect(datenbanken_und_informationssysteme)
introduction_to_simulation.provides_competence.connect(numerik)

it_projektmanagement = Module()
it_projektmanagement.name = "IT-Projektmanagement "
it_projektmanagement.cp_plus_description = {'DEFAULT':3.0}
it_projektmanagement.module_description = "Projektvorbereitung: Projektbeschreibung, Zieldefinition, Aufbau- u. Ablauforganisation, Wirtschaftlichkeitsprognose Projektplanung: Budgetierung, Ablaufplanung, Terminmanagement, Kapazitätsplanung, Analyse kritischer Pfade Projektsteuerung: Fortschrittskontrolle, Budgetüberwachung, Dokumentation und Berichtswesen Projektabschluss: Projektabnahme, Erkenntnissicherung, Projektliquidation Projektunterstützende Maßnahmen: Projektmanagementwerkzeuge, Kreativitäts- und Arbeitstechniken, Konfigurationsmanagement Agiles Projektmanagment, SCRUM"
it_projektmanagement.is_in_summer = True
it_projektmanagement.is_in_winter = True
it_projektmanagement.save()

it_projektmanagement.needs_competence.connect(analysis)
it_projektmanagement.needs_competence.connect(algorithmen_und_datenstrukturen_)

logik_module = Module()
logik_module.name = "Logik"
logik_module.cp_plus_description = {'DEFAULT':5.0}
logik_module.module_description = "Anwendungsfelder für Logik in der Informatik, Logische Syntax (Formelbegriff und Argumentbegriff für Aussagenlogik und Prädikatenlogik), formale Repräsentation von Wissen, Logische Semantik von zwei- und dreiwertiger Aussagenlogik sowie Prädikatenlogik, Domänenspezifische Sprachen und Abstraktion zu allgemeinen logischen Sprachen, Folgerungsbegriff und logische Folgerung, Regelsysteme (u.a. für Formeln und Beweise), grundlegende Algorithmen für logische Probleme (SAT-Solving, Hornformel-Algorithmus, Überführung in Normalformen)"
logik_module.is_in_summer = True
logik_module.is_in_winter = True
logik_module.save()

logik_module.needs_competence.connect(algorithmen_und_datenstrukturen_)

maschinelles_lernen = Module()
maschinelles_lernen.name = "Maschinelles Lernen"
maschinelles_lernen.cp_plus_description = {'DEFAULT':5.0}
maschinelles_lernen.module_description = "Einführung in das Funktionslernen; Einführung in die Konzepträume und Konzeptlernen; Algorithmen des Instanz-basiertes Lernens und Clusteranalyse; Algorithmen zum Aufbau der Entscheidungsbäume; Bayesches Lernen; Neuronale Netze; Assoziationsanalyse; Verstärkungslernen; Hypothesen Evaluierung."
maschinelles_lernen.is_in_summer = True
maschinelles_lernen.is_in_winter = True
maschinelles_lernen.save()

maschinelles_lernen.needs_competence.connect(analysis)
maschinelles_lernen.needs_competence.connect(algorithmen_und_datenstrukturen_)
maschinelles_lernen.needs_competence.connect(numerik)
maschinelles_lernen.provides_competence.connect(analysis)
maschinelles_lernen.provides_competence.connect(algorithmen_und_datenstrukturen_)

mathematik_i = Module()
mathematik_i.name = "Mathematik I (Lineare Algebra und analytische Geometrie)"
mathematik_i.cp_plus_description = {'DEFAULT':8.0}
mathematik_i.module_description = "Algebra: Mengen, Relationen und Abbildungen, Vektorräume, lineare Gleichungssysteme, lineare Abbildungen und Matrizen, Determinanten, Eigenwerte und Eigenvektoren Geometrie: Grundlagen der affinen und projektiven Geometrie, homogene Koordinaten und Transformationen"
mathematik_i.is_in_summer = True
mathematik_i.is_in_winter = True
mathematik_i.save()

mathematik_i.needs_competence.connect(analysis)
mathematik_i.needs_competence.connect(algorithmen_und_datenstrukturen_)
mathematik_i.needs_competence.connect(numerik)

mathematik_ii = Module()
mathematik_ii.name = "Mathematik II (Algebra und Analysis)"
mathematik_ii.cp_plus_description = {'DEFAULT':8.0}
mathematik_ii.module_description = "Algebra: Algebraische Strukturen und ihre Eigenschaften: Gruppen, Ringe und Körper, Faktorstrukturen und Homomorphie Analysis I: Folgen und Reihen, Differential- und Integralrechnung für Funktionen mit einer und mehreren Veränderlichen, Potenzreihen und ihr Konvergenzkreis Analysis II: Differential- und Integralrechnung von Funktionen mit mehreren Veränderlichen"
mathematik_ii.is_in_summer = True
mathematik_ii.is_in_winter = True
mathematik_ii.save()

mathematik_ii.needs_competence.connect(analysis)
mathematik_ii.needs_competence.connect(algorithmen_und_datenstrukturen_)

mathematik_iii = Module()
mathematik_iii.name = "Mathematik III (Stochastik, Statistik, Numerik, Differentialgleichungen)"
mathematik_iii.cp_plus_description = {'DEFAULT':6.0}
mathematik_iii.module_description = "Stochastik: Diskrete und stetige Zufallsgrößen und ihre Verteilungsfunktionen, Grenzwertsätze, Modellierung Statistik: Beschreibende Statistik, Vertrauensintervalle und Testen von Hypothesen, Statistischen Datenanalyse, Regressions-, Korrelations- und Varianzanalyse Numerik: Interpolation durch Polynome, numerische Integration, Numerik linearer Gleichungssysteme, Nullstellen nichtlinearer Gleichungen Differentialgleichungen: Grundlagen gewöhnlicher Differentialgleichungen n’ter Ordnung: elementare explizite Lösungsverfahren und Anfangswertprobleme"
mathematik_iii.is_in_summer = True
mathematik_iii.is_in_winter = True
mathematik_iii.save()

mathematik_iii.needs_competence.connect(analysis)
mathematik_iii.needs_competence.connect(algorithmen_und_datenstrukturen_)
mathematik_iii.needs_competence.connect(numerik)
mathematik_iii.provides_competence.connect(algorithmen_und_datenstrukturen_)

mesh_processing = Module()
mesh_processing.name = "Mesh Processing"
mesh_processing.cp_plus_description = {'DEFAULT':6.0}
mesh_processing.module_description = "3D-scannen und TriangulierungDatenstrukturendiskrete Differentialgeometrie Glätten Parametriesierung Dezimierung Remeshing Deformation"
mesh_processing.is_in_summer = True
mesh_processing.is_in_winter = True
mesh_processing.save()

mesh_processing.needs_competence.connect(algorithmen_und_datenstrukturen_)
mesh_processing.needs_competence.connect(betriebssysteme)
mesh_processing.needs_competence.connect(digitaltechnik_und_rechnerorganisation)
mesh_processing.needs_competence.connect(analysis)
mesh_processing.needs_competence.connect(datenbanken_und_informationssysteme)
mesh_processing.needs_competence.connect(numerik)
mesh_processing.provides_competence.connect(algorithmen_und_datenstrukturen_)
mesh_processing.provides_competence.connect(betriebssysteme)
mesh_processing.provides_competence.connect(digitaltechnik_und_rechnerorganisation)
mesh_processing.provides_competence.connect(analysis)
mesh_processing.provides_competence.connect(datenbanken_und_informationssysteme)
mesh_processing.provides_competence.connect(numerik)

modellierung_module = Module()
modellierung_module.name = "Modellierung"
modellierung_module.cp_plus_description = {'DEFAULT':4.0}
modellierung_module.module_description = "Modellierungstheorie: Von der Diskurswelt zu formalisierten Informationsmodellen Prozesse, Workflows und Geschäftsprozesse Meta-Modelle, Referenzmodellierung Grundsätze ordnungsmäßiger Modellierung Fachkonzeptuelle Modellierung mit höheren Petri-Netzen, der Entity Relationship-Methode und der BPMN Objektorientierte Modellierung mit UML Umsetzung konkreter Aufgabenstellungen"
modellierung_module.is_in_summer = True
modellierung_module.is_in_winter = True
modellierung_module.save()

modellierung_module.needs_competence.connect(algorithmen_und_datenstrukturen_)

neuronale_netze = Module()
neuronale_netze.name = "Neuronale Netze"
neuronale_netze.cp_plus_description = {'DEFAULT':5.0}
neuronale_netze.module_description = "Einführung in die Grundlagen der neuronalen Netze aus Sicht der Informatik Behandlung von Lernparadigmen und Lernalgorithmen, Netzmodelle"
neuronale_netze.is_in_summer = True
neuronale_netze.is_in_winter = True
neuronale_netze.save()

neuronale_netze.needs_competence.connect(analysis)
neuronale_netze.needs_competence.connect(algorithmen_und_datenstrukturen_)
neuronale_netze.needs_competence.connect(betriebssysteme)
neuronale_netze.needs_competence.connect(numerik)
neuronale_netze.provides_competence.connect(algorithmen_und_datenstrukturen_)
neuronale_netze.provides_competence.connect(betriebssysteme)
neuronale_netze.provides_competence.connect(digitaltechnik_und_rechnerorganisation)
neuronale_netze.provides_competence.connect(analysis)
neuronale_netze.provides_competence.connect(datenbanken_und_informationssysteme)
neuronale_netze.provides_competence.connect(diskrete_strukturen)
neuronale_netze.provides_competence.connect(numerik)

parallele_programmierung = Module()
parallele_programmierung.name = "Parallele Programmierung"
parallele_programmierung.cp_plus_description = {'DEFAULT':5.0}
parallele_programmierung.module_description = "Die parallele Programmierung gewinnt immer mehr an Bedeutung, da heutzutage bereits Mobiltelefone und Laptops über mehrere Prozessorkerne verfügen. Supercomputer besitzen teilweise sogar mehrere Millionen Kerne und haben sich als ein nützliches und mittlerweile unverzichtbares Werkzeug für viele Wissenschaftsbereiche etabliert. Die dadurch möglichen Analysen und Simulationen haben es erlaubt, den wissenschaftlichen Erkenntnisgewinn in vielen Bereichen deutlich zu steigern. Die optimale Nutzung dieser Komponenten ist allerdings keine einfache Aufgabe, weshalb Wissenschaftlerinnen und Wissenschaftler bei der Entwicklung effizienter Anwendungen vor immer neue Herausforderungen gestellt werden. Für die parallele Programmierung ist daher ein tiefergehendes Verständnis der Hard- und Softwareumgebung sowie möglicher Fehlerursachen unabdingbar. In der Vorlesung werden die Grundlagen der parallelen Programmierung gelehrt; die Übungen dienen der praktischen Anwendung und Umsetzung der erworbenen Kenntnisse in der Programmiersprache C. Im Rahmen der Vorlesung werden einige der wichtigsten Themengebiete betrachtet: Hard- und Softwarekonzepte (Mehrkernprozessoren, Prozesse/Threads, NUMA etc.), unterschiedliche Ansätze zur parallelen Programmierung (OpenMP, POSIX Threads, MPI) sowie Werkzeuge zur Leistungsanalyse und Fehlersuche (Skalierbarkeit, Deadlocks, Race Conditions etc.). Zusätzlich werden Gründe und Lösungsansätze für Leistungsprobleme diskutiert und alternative Ansätze für die parallele Programmierung vorgestellt. Beispiele und Probleme werden anhand realer wissenschaftlicher Anwendungen veranschaulicht."
parallele_programmierung.is_in_summer = True
parallele_programmierung.is_in_winter = True
parallele_programmierung.save()

parallele_programmierung.needs_competence.connect(analysis)
parallele_programmierung.needs_competence.connect(algorithmen_und_datenstrukturen_)
parallele_programmierung.provides_competence.connect(analysis)
parallele_programmierung.provides_competence.connect(algorithmen_und_datenstrukturen_)

praktikum = Module()
praktikum.name = "Praktikum"
praktikum.cp_plus_description = {'DEFAULT':18.0}
praktikum.module_description = "Praktikumsspezifisch in Bezug auf den Studiengang"
praktikum.is_in_summer = True
praktikum.is_in_winter = True
praktikum.save()

praktikum.needs_competence.connect(analysis)
praktikum.needs_competence.connect(algorithmen_und_datenstrukturen_)
praktikum.needs_competence.connect(numerik)
praktikum.provides_competence.connect(algorithmen_und_datenstrukturen_)
praktikum.provides_competence.connect(betriebssysteme)
praktikum.provides_competence.connect(analysis)
praktikum.provides_competence.connect(datenbanken_und_informationssysteme)
praktikum.provides_competence.connect(numerik)

programmierparadigmen = Module()
programmierparadigmen.name = "Programmierparadigmen"
programmierparadigmen.cp_plus_description = {'DEFAULT':5.0}
programmierparadigmen.module_description = "Konzepte der wesentlichen Paradigmenprozedural,objektorientiert,funktional,logisches,sowie ggf weitere ParadigmenTechnische Umsetzung der Paradigmen in ProgrammiersprachenAnwendung der Paradigmen in Programmiersprachen wie z.B.CJavaScalaHaskellPrologEntscheidungskriterien für Paradigmen"
programmierparadigmen.is_in_summer = True
programmierparadigmen.is_in_winter = True
programmierparadigmen.save()

programmierparadigmen.needs_competence.connect(analysis)
programmierparadigmen.needs_competence.connect(algorithmen_und_datenstrukturen_)
programmierparadigmen.needs_competence.connect(numerik)
programmierparadigmen.provides_competence.connect(analysis)
programmierparadigmen.provides_competence.connect(algorithmen_und_datenstrukturen_)

schlüsselkompetenzen_i = Module()
schlüsselkompetenzen_i.name = "Schlüsselkompetenzen I"
schlüsselkompetenzen_i.cp_plus_description = {'DEFAULT': 2.5}
schlüsselkompetenzen_i.module_description = "Studienplanung & erfolgreiches Studieren Ziele & zielorientiertes Handeln Zeitmanagement & Zeitplanung Selbstständig denken und handeln Werte und ethisches Handeln Teams und Teamfähigkeit Entrepreneurgeist & Initiative Diskussionsführung wissenschaftlichen Berichte und Präsentationen Digital Rights"
schlüsselkompetenzen_i.is_in_summer = True
schlüsselkompetenzen_i.is_in_winter = True
schlüsselkompetenzen_i.save()

schlüsselkompetenzen_i.needs_competence.connect(analysis)
schlüsselkompetenzen_i.needs_competence.connect(algorithmen_und_datenstrukturen_)

schlüsselkompetenzen_ii = Module()
schlüsselkompetenzen_ii.name = "Schlüsselkompetenzen II"
schlüsselkompetenzen_ii.cp_plus_description = {'DEFAULT':2.5}
schlüsselkompetenzen_ii.module_description = "Studienplanung & erfolgreiches Studieren Ziele & zielorientiertes Handeln Zeitmanagement & Zeitplanung Selbstständig denken und handeln Werte und ethisches Handeln Teams und Teamfähigkeit Entrepreneurgeist & Initiative Diskussionsführung wissenschaftlichen Berichte und Präsentationen Digital Rights"
schlüsselkompetenzen_ii.is_in_summer = True
schlüsselkompetenzen_ii.is_in_winter = True
schlüsselkompetenzen_ii.save()

schlüsselkompetenzen_ii.needs_competence.connect(analysis)
schlüsselkompetenzen_ii.needs_competence.connect(algorithmen_und_datenstrukturen_)

sichere_systeme = Module()
sichere_systeme.name = "Sichere Systeme"
sichere_systeme.cp_plus_description = {'DEFAULT':5.0}
sichere_systeme.module_description = "IT-Sicherheitsaspekte und IT-Sicherheitsbedrohungen Designprinzipien sicherer IT-Systeme Sicherheitsrichtlinien Ausgewählte Sicherheitsmechanismen"
sichere_systeme.is_in_summer = True
sichere_systeme.is_in_winter = True
sichere_systeme.save()

sichere_systeme.needs_competence.connect(analysis)
sichere_systeme.needs_competence.connect(algorithmen_und_datenstrukturen_)
sichere_systeme.provides_competence.connect(analysis)
sichere_systeme.provides_competence.connect(algorithmen_und_datenstrukturen_)
sichere_systeme.provides_competence.connect(numerik)

software_engineering_it_projektmanagement = Module()
software_engineering_it_projektmanagement.name = "Software Engineering & IT-Projektmanagement"
software_engineering_it_projektmanagement.cp_plus_description = {'DEFAULT':5.0}
software_engineering_it_projektmanagement.module_description = "- Software Engineering - Was ist das und wozu wird es gebraucht? - Prozessmodelle: Wasserfall Modell, Inkrementelles Modell, Integration und Konfiguration - Prozessaktivitäten: Spezifikation, Entwicklung, Validierung, Evolution - Test & Debugging - Agile Softwareentwicklung  - Tools & Werkzeuge - Clean-Coding / Code-Conventions - praktische Beispiele"
software_engineering_it_projektmanagement.is_in_summer = True
software_engineering_it_projektmanagement.is_in_winter = True
software_engineering_it_projektmanagement.save()

software_engineering_it_projektmanagement.needs_competence.connect(algorithmen_und_datenstrukturen_)
software_engineering_it_projektmanagement.needs_competence.connect(betriebssysteme)
software_engineering_it_projektmanagement.needs_competence.connect(analysis)
software_engineering_it_projektmanagement.needs_competence.connect(datenbanken_und_informationssysteme)
software_engineering_it_projektmanagement.needs_competence.connect(numerik)
software_engineering_it_projektmanagement.provides_competence.connect(algorithmen_und_datenstrukturen_)

software_engineering_ = Module()
software_engineering_.name = "Software Engineering "
software_engineering_.cp_plus_description = {'DEFAULT':5.0}
software_engineering_.module_description = "Vermittelt werden sollen hierbei Techniken und Tools, welche die Entwicklung von großen Softwareprojekten zwangsläufig notwendig machen. Dabei wird innerhalb des Semesters der gesamte Entwicklungszyklus vom ersten Requirement über das Softwaredesign bis zur Erstellung der Dokumentation durchgespielt. Die Veranstaltung richtet sich an alle Informatik-Bachelorstudenten."
software_engineering_.is_in_summer = True
software_engineering_.is_in_winter = True
software_engineering_.save()

software_engineering_.needs_competence.connect(analysis)
software_engineering_.needs_competence.connect(algorithmen_und_datenstrukturen_)
software_engineering_.needs_competence.connect(betriebssysteme)
software_engineering_.needs_competence.connect(numerik)
software_engineering_.provides_competence.connect(analysis)
software_engineering_.provides_competence.connect(algorithmen_und_datenstrukturen_)

softwareprojekt = Module()
softwareprojekt.name = "Softwareprojekt"
softwareprojekt.cp_plus_description = {'DEFAULT':6.0}
softwareprojekt.module_description = "Durchführung eines Softwareentwicklungsprojektes im Team Anwendung der Inhalte des Moduls IT- Projektmanagement Dieses Modul wird durch unterschiedliche Lehrveranstaltungen implementiert. Fachliche Inhalte sind angebotsspezifisch."
softwareprojekt.is_in_summer = True
softwareprojekt.is_in_winter = True
softwareprojekt.save()

softwareprojekt.needs_competence.connect(analysis)
softwareprojekt.needs_competence.connect(algorithmen_und_datenstrukturen_)
softwareprojekt.provides_competence.connect(analysis)
softwareprojekt.provides_competence.connect(algorithmen_und_datenstrukturen_)

technische_informatik_i = Module()
technische_informatik_i.name = "Technische Informatik I"
technische_informatik_i.cp_plus_description = {'DEFAULT':5.0}
technische_informatik_i.module_description = "Kombinatorische SchaltnetzeSequentielle Schaltwerke Computerarithmetik Aufbau eines Rechners Befehlssatz und Adressierung Fließband- und Parallelverarbeitung"
technische_informatik_i.is_in_summer = True
technische_informatik_i.is_in_winter = True
technische_informatik_i.save()

technische_informatik_i.needs_competence.connect(analysis)
technische_informatik_i.needs_competence.connect(algorithmen_und_datenstrukturen_)
technische_informatik_i.needs_competence.connect(numerik)

technische_informatik_ii = Module()
technische_informatik_ii.name = "Technische Informatik II"
technische_informatik_ii.cp_plus_description = {'DEFAULT':5.0}
technische_informatik_ii.module_description = "Inhalte Entwurfsprinzipien und Abstraktionen Systemressourcen und Aktivitätsstrukturen Kommunikation und Synchronisation Beispiele für Ressourcenverwaltung und Protokolle aus dem Bereich der Betriebs- und Netzwerkarchitekturen"
technische_informatik_ii.is_in_summer = True
technische_informatik_ii.is_in_winter = True
technische_informatik_ii.save()

technische_informatik_ii.needs_competence.connect(analysis)
technische_informatik_ii.needs_competence.connect(algorithmen_und_datenstrukturen_)
technische_informatik_ii.needs_competence.connect(numerik)
technische_informatik_ii.provides_competence.connect(analysis)
technische_informatik_ii.provides_competence.connect(algorithmen_und_datenstrukturen_)
technische_informatik_ii.provides_competence.connect(numerik)

trainingsmodul_schlüssel_und_methodenkompetenz_ = Module()
trainingsmodul_schlüssel_und_methodenkompetenz_.name = "Trainingsmodul Schlüssel- und Methodenkompetenz "
trainingsmodul_schlüssel_und_methodenkompetenz_.cp_plus_description = {'DEFAULT':3.0}
trainingsmodul_schlüssel_und_methodenkompetenz_.module_description = "Dieses Modul wird durch unterschiedliche Lehrveranstaltungen implementiert. Die Inhalte sind daher angebotsspezifisch."
trainingsmodul_schlüssel_und_methodenkompetenz_.is_in_summer = True
trainingsmodul_schlüssel_und_methodenkompetenz_.is_in_winter = True
trainingsmodul_schlüssel_und_methodenkompetenz_.save()

trainingsmodul_schlüssel_und_methodenkompetenz_.needs_competence.connect(algorithmen_und_datenstrukturen_)

usability_und_ästhetik = Module()
usability_und_ästhetik.name = "Usability und Ästhetik"
usability_und_ästhetik.cp_plus_description = {'DEFAULT':5.0}
usability_und_ästhetik.module_description = "Methoden des User Experience Design und Design Thinking für die Ideation Phase im Entwicklungsprozess von Produkten und Dienstleistungen   - Designgeschichte von Informations- und Kommunikationsprodukten - Methoden zur Konzipierung und Realisierung einer Usability und User Experience - 10 Thesen des guten Designs - Gutes Design für Informations- und Kommunikationssysteme bzw. Informations- und Kommunikationstechnik"
usability_und_ästhetik.is_in_summer = True
usability_und_ästhetik.is_in_winter = True
usability_und_ästhetik.save()

usability_und_ästhetik.needs_competence.connect(analysis)
usability_und_ästhetik.needs_competence.connect(algorithmen_und_datenstrukturen_)
usability_und_ästhetik.needs_competence.connect(numerik)

visualisierung = Module()
visualisierung.name = "Visualisierung"
visualisierung.cp_plus_description = {'DEFAULT':5.0}
visualisierung.module_description = "Visualization goals and quality criteriaUnderstanding of fundamentals of visual perceptionOverview about data structures in visualizationBasic algorithms (Isolines, color scales, diagramm techniques),Direct and indirecte visualization of volume dataInformation visualization"
visualisierung.is_in_summer = True
visualisierung.is_in_winter = True
visualisierung.save()

visualisierung.needs_competence.connect(analysis)
visualisierung.needs_competence.connect(algorithmen_und_datenstrukturen_)
visualisierung.needs_competence.connect(numerik)
visualisierung.provides_competence.connect(analysis)
visualisierung.provides_competence.connect(algorithmen_und_datenstrukturen_)
visualisierung.provides_competence.connect(numerik)

wahlpflichtfach_fin_schlüssel_und_methodenkompetenz = Module()
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.name = "Wahlpflichtfach FIN Schlüssel- und Methodenkompetenz"
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.cp_plus_description = {'DEFAULT':5.0}
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.module_description = "Dieses Modul kann durch unterschiedliche Lehrveranstaltungen implementiert werden. Die fachspezifischen Inhalte sind angebotsspezifisch."
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.is_in_summer = True
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.is_in_winter = True
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.save()

wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.needs_competence.connect(algorithmen_und_datenstrukturen_)
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.provides_competence.connect(analysis)
wahlpflichtfach_fin_schlüssel_und_methodenkompetenz.provides_competence.connect(algorithmen_und_datenstrukturen_)

wissenschaftliches_seminar = Module()
wissenschaftliches_seminar.name = "Wissenschaftliches Seminar"
wissenschaftliches_seminar.cp_plus_description = {'DEFAULT':3.0}
wissenschaftliches_seminar.module_description = "Dieses Modul kann durch unterschiedliche Lehrveranstaltungen implementiert werden. Die fachlichen Inhalte sind angebotsspezifisch."
wissenschaftliches_seminar.is_in_summer = True
wissenschaftliches_seminar.is_in_winter = True
wissenschaftliches_seminar.save()

wissenschaftliches_seminar.needs_competence.connect(algorithmen_und_datenstrukturen_)


dummy = Module()
dummy.name = "DUMMY"
dummy.cp_plus_description = {'DEFAULT': 5.0}
dummy.module_description = "DUMMY"
dummy.is_in_summer = True
dummy.is_in_winter = True
dummy.provides_competence.connect(dummy_competence)
dummy.save()