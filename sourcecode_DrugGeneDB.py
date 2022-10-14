from aifc import Error
import sqlite3
import pandas as pd
import csv


#Connect to the database
def create_connection(db_file):
    """Create a database connection to the SQLite database given by the db_file
    :param db_file: database db_file
    :return: Connection object or None"""

    global con
    global cursor

    try:
        con = sqlite3.connect(db_file)
        cursor = con.cursor()
        print("Successfully connected to SQLite")
    except Error as e:
        print(e)
        print("ERROR")

    return con

#Write diseases to databse
def insertDiseaseInputsIntoDisease(db_file, OTP_file, diseaseId, diseaseName):
    """Write diseaseId and diseaseName to Disease table from tsv file collected from the Open Target Platform.
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, diseaseId: column name for disease id in OTP_file, diseaseName: column name for disease name in OTP_file
    :return: database with updated Disease table"""

    create_connection(db_file)
    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        for ind in df.index:
            diseaseID = df[diseaseId][ind]
            name = df[diseaseName][ind]
            cursor.execute("INSERT OR REPLACE INTO Disease VALUES (?, ?)", (diseaseID, name))
            con.commit()
    con.close()

#Write drugs to database
def insertDrugInputsIntoDrug(db_file, OTP_file, drugId, drugName, type):
    """Write drugId, drugName, and type to drug table from tsv file collected from the Open Target Platform.
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, drugId: column name for drug id in OTP_file, diseaseId: column name for drug name in OTP_file, type: column name for drug type in OTP_file. 
    :return: database with updated Drug table"""

    create_connection(db_file)
    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        for ind in df.index:
            drugID = df[drugId][ind]
            name = df[drugName][ind]
            moleculeType = df[type][ind]
            cursor.execute("INSERT OR REPLACE INTO Drug VALUES (?, ?, ?)", (drugID, name, moleculeType))
            con.commit()
    con.close()

#Write genes to database
def insertGeneInputsIntoGene(db_file, OTP_file, geneCardSymbol, geneName, gene_file, geneCardsSymbol, entry):
    """Write GeneCardsSymbol, UniProtID and name to Gene table from tsv file collected from the Open Target Platform.
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, geneCardsSymbol: column name for GeneCard symbol in OTP_file, geneName: column name for gene name in OTP_file,
           gene_file: tsv file collected from UniProt ID mapping, geneCardsSymbol: column name for geneCard symbols in gene_file, entry: column name for entry in gene_file. 
    :return: database with updated gene table"""

    create_connection(db_file)
    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        uniProtDict = uniProt_dict(gene_file, geneCardsSymbol, entry)
        for ind in df.index:
            symbol = df[geneCardSymbol][ind]
            uniprotID = uniProtDict.get(symbol, None)
            name = df[geneName][ind]
            cursor.execute("INSERT OR REPLACE INTO Gene VALUES (?, ?, ?)", (symbol, uniprotID, name))
            con.commit()
    con.close()

def uniProt_dict(gene_file, geneCardsSymbol, entry):
    """Make a dictionary with geneCardsSymbols as keys and entries from UniProt as values. 
    :param db_file: gene_file: tsv file collected from UniProt ID mapping, geneCardsSymbol: column name for geneCard symbols in gene_file, entry: column name for entry in gene_file. 
    :return: Dictionary with GeneCards symbols as kesy and entries from UniProt as values. """

    gene_dict = {}

    with open(gene_file, "r") as drug_file:
        df = pd.read_csv(gene_file, delimiter="\t")
        for ind in df.index:
            gcSymbol = df[geneCardsSymbol][ind]
            uniProtID = df[entry][ind]
            gene_dict[gcSymbol] = uniProtID

    return gene_dict

#Write gene associations to database
def insertGeneAssociationInputsIntoGeneAssociation(db_file, OTP_file, geneCardSymbol, diseaseId):
    """Write geneCardsSymbol and diseaseID  to GeneAssociation table from tsv file collected from the Open Target Platform
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, geneCardSymbol: column name for GeneCard symbol in OTP_file, diseaseId: column name for disease ID in OTP_file. 
    :return: database with updated GeneAsssociation table"""

    create_connection(db_file)

    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        for ind in df.index:
            symbol = df[geneCardSymbol][ind]
            diseaseID = df[diseaseId][ind]
            cursor.execute("INSERT OR REPLACE INTO GeneAssociation VALUES (?, ?)", (symbol, diseaseID))
            con.commit()
    con.close()

#Write interactions to database
def insertInteractionInputsIntoInteraction(db_file, OTP_file, geneCardSymbol, drugId, mechanismOfAction, actionType):
    """Write GeneCardsSymbol, drugID, mechanismOfAction, and actionType to Interaction table from tsv file collected from the Open Target Platform.
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, geneCardSymbol: column name for GeneCard symbol in OTP_file, drugId: column name for drug ID in OTP_file, mechanismOfAction: column name for mechanism of action in OTP_file, actionType: column name for action type in OTP_file.
    :return: database with updated Interaction table"""

    create_connection(db_file)
    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        for ind in df.index:
            symbol = df[geneCardSymbol][ind]
            drugID = df[drugId][ind]
            MOA = df[mechanismOfAction][ind]
            actType = df[actionType][ind]
            source = "https://platform.opentargets.org/disease/EFO_0000311"

            cursor.execute("INSERT OR REPLACE INTO Interaction VALUES (?, ?, ?, ?, ?)", (symbol, drugID, MOA, actType, source))
            con.commit()
    con.close()

#Write indicated for to database
def insertIndicatedForInputsIntoIndicatedFor(db_file, OTP_file, diseaseId, drugId, phase):
    """Write diseaseID, drugID, and phase to IndicatedFor table from tsv file collected from the Open Target Platform
    :param db_file: database db_file, OTP_file: tsv file from Open Target Platform, diseaseId: column name for disease ID in OTP_file, drugId: column name for drug ID in OTP_file, phase: column name for phase in OTP_file.
    :return: database with updated IndicatedFor table"""

    create_connection(db_file)
    with open(OTP_file, "r") as OTP_file:
        df = pd.read_csv(OTP_file, delimiter="\t")
        for ind in df.index:
            diseaseID = df[diseaseId][ind]
            drugID = df[drugId][ind]
            Phase = df[phase][ind]

            cursor.execute("INSERT OR REPLACE INTO IndicatedFor VALUES (?, ?, ?)", (diseaseID, drugID, int(Phase)))
            con.commit()
    con.close()


create_connection("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db")
#insertDiseaseInputsIntoDisease("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'diseaseId', 'diseaseName')
#insertDrugInputsIntoDrug("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'drugId', 'drugName', 'type')
#insertGeneInputsIntoGene("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'symbol', 'name', "/Users/kristinelippestad/Dokumenter/Master/uniProtID.tsv", "From", "Entry")
#insertGeneAssociationInputsIntoGeneAssociation("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'symbol', 'diseaseId')
#insertInteractionInputsIntoInteraction("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'symbol', 'drugId', 'mechanismOfAction', 'actionType')
#insertIndicatedForInputsIntoIndicatedFor("/Users/kristinelippestad/Dokumenter/Master/Test_DB.db", "/Users/kristinelippestad/Downloads/EFO_0000311-known-drugs.tsv", 'diseaseId', 'drugId', 'phase')
#con.close()


