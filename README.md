# Reinforced Concrete Ontology Construction
- Comparative Evaluation of RDF-Based Ontology Representation Methods for Semantic Structuring of Progress Payment Documents in Reinforced Concrete Work

## Install

```bash
conda create -n RC_Ontology python=3.13.14
conda activate RC_Ontology
conda install -y pip
pip install --upgrade pip
pip install -r requirements.txt
```

## Identifier Convention

Ontology resources use IRIs.

```turtle
@prefix ppdoc: <https://example.org/rc-progress-payment#> .
```

For example, `ppdoc:inspection-record-13` expands to:

```text
https://example.org/rc-progress-payment#inspection-record-13
```

## Ontology Artifacts

```text
Ontology_Development_101_Rebuild.md
Ontology_Tables.md
ontology/ontology.ttl
ontology/sample_data.ttl
visualization/ontology_graph.html
```

## Validate

```bash
conda activate RC_Ontology
python - <<'PY'
from rdflib import Graph
for path in ("ontology/ontology.ttl", "ontology/sample_data.ttl"):
    g = Graph()
    g.parse(path, format="turtle")
    print(path, len(g))
PY
```

## Visualization
http://127.0.0.1:3000/visualization/ontology_graph.html?vscode-livepreview=true
