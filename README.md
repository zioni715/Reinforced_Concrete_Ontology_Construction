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


## Visualization
http://127.0.0.1:3000/visualization/ontology_graph.html?vscode-livepreview=true
