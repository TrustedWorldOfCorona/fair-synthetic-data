import sys
import os
from rdflib import Namespace, Graph, BNode, Literal
from rdflib.namespace import RDF, XSD

twoc = Namespace("http://example.com/twoc#")
vodan = Namespace("http://purl.org/vodan/whocovid19crfsemdatamodel/")
vodan_inst = Namespace("http://purl.org/vodan/whocovid19crfsemdatamodel/instances/")
obo = Namespace("http://purl.obolibrary.org/obo/")

has_part = obo.BFO_0000051

def generate_crf(n, s, m, p):
    crf = Graph()
    crf.bind("vodan", vodan)
    crf.bind("vodan_inst", vodan_inst)
    crf.bind("obo", obo)

    entry = twoc[n]

    crf.add((entry, RDF.type, vodan["who-covid-19-rapid-crf"]))
    crf.add((entry, vodan.participant_id, Literal(n.zfill(5))))

    # admission module
    module1 = BNode()
    crf.add((entry, has_part, module1))
    crf.add((module1, RDF.type, vodan.Module_1))

    # Supportive care section
    supportive_care = BNode()
    crf.add((module1, has_part, supportive_care))
    crf.add((supportive_care, RDF.type, vodan.Supportive_care))
    icu_admission = BNode()
    crf.add((supportive_care, has_part, icu_admission))
    crf.add((supportive_care, has_part, icu_admission))
    crf.add((icu_admission, RDF.type, vodan.ICU_admission))
    crf.add((icu_admission, vodan.has_value, vodan_inst.C49488 if s == "1" else vodan_inst.C49487))


    # Lab result section
    lab_results = BNode()
    crf.add((module1, has_part, lab_results))
    crf.add((lab_results, RDF.type, vodan.Laboratory_results))
    pge2 = BNode()
    crf.add((lab_results, has_part, pge2))
    crf.add((pge2, RDF.type, vodan.PGE2))
    crf.add((pge2, vodan.has_literal_value, Literal(p, datatype=XSD.float)))

    # Medication section
    medication = BNode()
    crf.add((module1, has_part, medication))
    crf.add((medication, RDF.type, vodan.Medication))
    corticosteroid = BNode()
    crf.add((medication, has_part, corticosteroid))
    crf.add((corticosteroid, RDF.type, vodan.Corticosteroid))
    if m == "1":
        crf.add((corticosteroid, vodan.has_value, vodan_inst.C49488))
    else:
        crf.add((corticosteroid, vodan.has_value, vodan_inst.C49487))

    return crf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing CSV input and output location parameters. Example usage:")
        print(f"\tpython {sys.argv[0]} ../randomizer/out/exp1_random_sdata.csv ./out")
        exit(1)
    if len(sys.argv) < 3:
        print("Missing output location parameter. Example usage:")
        print(f"\tpython {sys.argv[0]} ../randomizer/out/exp1_random_sdata.csv ./out")
        exit(2)

    out_path = sys.argv[2]    

    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    with open(sys.argv[1]) as file:
        # skip header line
        next(file)

        for line in file:
            (n, s, m, p) = line.rstrip().split(",")
            crf = generate_crf(n, s, m, p)
            crf.serialize(f"{out_path}/{n.zfill(5)}.ttl", format="turtle")
