import sys
from rdflib import Namespace, Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, XSD

twoc = Namespace("http://example.com/twoc#")
vodan = Namespace("http://purl.org/vodan/whocovid19crfsemdatamodel/")
vodan_inst = Namespace("http://purl.org/vodan/whocovid19crfsemdatamodel/instances/")
obo = Namespace("http://purl.obolibrary.org/obo#")

has_part = obo.BFO_0000051

def generate_crf(n, s, m, p):
    crf = Graph()
    crf.bind("vodan", vodan)
    crf.bind("vodan_inst", vodan_inst)
    crf.bind("obo", obo)

    entry = twoc[n]

    crf.add((entry, RDF.type, vodan["who-covid-19-rapid-crf"]))
    crf.add((entry, vodan.participant_id, Literal(n)))

    # admission module
    module1 = BNode()
    crf.add((entry, has_part, module1))
    crf.add((module1, RDF.type, vodan.Module_1))
    # TODO

    # followup module
    module2 = BNode()
    crf.add((entry, has_part, module2))
    crf.add((module2, RDF.type, vodan.Module_2))

    # Supportive care section
    supportive_care = BNode()
    crf.add((module2, has_part, supportive_care))
    crf.add((supportive_care, RDF.type, vodan.Supportive_care))
    icu_admission = BNode()
    crf.add((supportive_care, has_part, icu_admission))
    crf.add((supportive_care, has_part, icu_admission))
    crf.add((icu_admission, RDF.type, vodan.ICU_admission))
    crf.add((icu_admission, vodan.has_value, vodan_inst.C49488 if s == "1" else vodan_inst.C49487))


    # Lab result section
    lab_results = BNode()
    crf.add((module2, has_part, lab_results))
    crf.add((lab_results, RDF.type, vodan.Laboratory_results))
    pge2 = BNode()
    crf.add((lab_results, has_part, pge2))
    crf.add((pge2, RDF.type, vodan.PGE2))
    crf.add((pge2, vodan.has_literal_value, Literal(p, datatype=XSD.float)))

    # Medication section
    medication = BNode()
    crf.add((module2, has_part, medication))
    crf.add((medication, RDF.type, vodan.Medication))
    corticosteroid = BNode()
    crf.add((medication, has_part, corticosteroid))
    crf.add((corticosteroid, RDF.type, vodan.Corticosteroid))
    if m == "1":
        crf.add((corticosteroid, vodan.has_value, vodan_inst.C49488))
        #agent = BNode()
        #crf.add((corticosteroid, has_part, agent))
        #crf.add((agent, RDF.type, vodan.Maximum_daily_corticosteroid_dose))
        #crf.add((agent, vodan.has_literal_value, Literal("3 mg"))) # replace with csv value?
    else:
        crf.add((corticosteroid, vodan.has_value, vodan_inst.C49487))

    return crf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing CSV input parameter. Example usage:")
        print(f"\t python {sys.argv[0]} data.csv")
        exit(1)

    with open(sys.argv[1]) as file:
        for line in file:
            (n, s, m, p) = line.rstrip().split(",")
            crf = generate_crf(n, s, m, p)
            print(crf.serialize(format="turtle").decode("UTF-8"))
            print(n,s,m,p)
