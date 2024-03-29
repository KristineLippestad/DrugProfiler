CREATE TABLE "Disease" (
	"DiseaseID"	TEXT NOT NULL UNIQUE,
	"DiseaseName"	INTEGER NOT NULL,
	PRIMARY KEY("DiseaseID")
);

CREATE TABLE "Drug" (
	"DrugID"	TEXT NOT NULL UNIQUE,
	"DrugName"	TEXT NOT NULL,
	"Type"	TEXT,
	"Smiles"	TEXT,
	"InChi Key"	TEXT,
	PRIMARY KEY("DrugID")
);

CREATE TABLE "Gene" (
	"HGNC"	TEXT NOT NULL UNIQUE,
	"UniProtID"	TEXT UNIQUE,
	"Name"	TEXT,
	"Organism"	TEXT,
	PRIMARY KEY("HGNC")
);

CREATE TABLE "BindingAffinity" (
	"BindingReactionID"	TEXT NOT NULL UNIQUE,
	"Kd_min"	NUMERIC,
	"Kd_max"	NUMERIC,
	"Ki_min"	NUMERIC,
	"Ki_max"	NUMERIC,
	"IC50_min"	NUMERIC,
	"IC50_max"	NUMERIC,
	"pH"	NUMERIC,
	"Temperature"	NUMERIC,
	"Organism"	TEXT,
	"Source"	TEXT,
	PRIMARY KEY("BindingReactionID")
);

CREATE TABLE "CellLine" (
	"CLO"	TEXT NOT NULL UNIQUE,
	"Name"	TEXT NOT NULL,
	"TissueType"	TEXT,
	"TissueSubType"	TEXT,
	"DiseaseID"	TEXT,
	CONSTRAINT "CellLine_FK1" FOREIGN KEY("DiseaseID") REFERENCES "Disease"("DiseaseID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "CellLine_PK" PRIMARY KEY("CLO")
);

CREATE TABLE "GeneAssociation" (
	"HGNC"	TEXT NOT NULL,
	"DiseaseID"	TEXT NOT NULL,
	CONSTRAINT "Interaction_FK1" FOREIGN KEY("HGNC") REFERENCES "Gene"("HGNC") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "Interaction_FK2" FOREIGN KEY("DiseaseID") REFERENCES "Disease"("DiseaseID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "Interaction_PK" PRIMARY KEY("HGNC","DiseaseID")
);

CREATE TABLE "IndicatedFor" (
	"DiseaseID"	TEXT NOT NULL,
	"DrugID"	TEXT NOT NULL,
	"Phase"	INTEGER,  
	CONSTRAINT "IndicatedFor_FK2" FOREIGN KEY("DrugID") REFERENCES "Drug"("DrugID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "IndicatedFor_FK1" FOREIGN KEY("DiseaseID") REFERENCES "Disease"("DiseaseID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "IndicatedFor_PK" PRIMARY KEY("DiseaseID","DrugID")
);

CREATE TABLE "Interaction" (
	"HGNC"	TEXT NOT NULL,
	"DrugID"	TEXT NOT NULL,
	"MOA"	TEXT,
	"ActionType"	TEXT,
	"Source"	TEXT,
	CONSTRAINT "Interaction_PK" PRIMARY KEY("HGNC","DrugID"),
	CONSTRAINT "Interaction_FK2" FOREIGN KEY("DrugID") REFERENCES "Drug"("DrugID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "Interaction_FK1" FOREIGN KEY("HGNC") REFERENCES "Gene"("HGNC") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Sensitivity" (
	"CLO"	TEXT NOT NULL,
	"DrugID"	TEXT NOT NULL,
	"IC50"	NUMERIC,
	"AUC"	NUMERIC,
	"Source"	TEXT,
	CONSTRAINT "Sensitivity_PK" PRIMARY KEY("CLO","DrugID"),
	CONSTRAINT "Sensitivity_FK1" FOREIGN KEY("CLO") REFERENCES "CellLine"("CLO") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "Sensitivity_FK2" FOREIGN KEY("DrugID") REFERENCES "Drug"("DrugID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "MeasuredFor" (
	"HGNC"	TEXT NOT NULL,
	"DrugID"	TEXT NOT NULL,
	"BindingReactionID"	TEXT NOT NULL,
	CONSTRAINT "MeasuredFor_PK" PRIMARY KEY("HGNC","DrugID", "BindingReactionID"),
	CONSTRAINT "MeasuredFor_FK1" FOREIGN KEY("HGNC") REFERENCES "Gene"("HGNC") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "MeasuredFor_FK2" FOREIGN KEY("DrugID") REFERENCES "Drug"("DrugID") ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT "MeasuredFor_FK3" FOREIGN KEY("BindingReactionID") REFERENCES "BindingAffinity"("BindingReactionID") ON UPDATE CASCADE ON DELETE CASCADE
);