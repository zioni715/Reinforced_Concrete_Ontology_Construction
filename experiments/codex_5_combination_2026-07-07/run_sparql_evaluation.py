from __future__ import annotations

import csv
import json
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = Path(__file__).resolve().parent
SPARQL_DIR = EXPERIMENT_DIR / "sparql"

DATA_FILES = [
    ROOT / "ontology" / "ontology.ttl",
    ROOT / "ontology" / "sample_data.ttl",
]

EXPECTED_ROWS = {
    "cq01_document_hierarchy.rq": 1,
    "cq02_statement_subdocuments.rq": 4,
    "cq03_worktype_sections.rq": 9,
    "cq04_cost_items.rq": 7,
    "cq05_boq_traceability.rq": 6,
    "cq06_shared_specification_basis.rq": 6,
    "cq07_summary_amounts.rq": 4,
    "cq08_specification_attributes.rq": 4,
    "cq09_statement_metadata.rq": 1,
    "cq10_boq_table_format_fields.rq": 10,
    "cq11_boq_required_field_completeness.rq": 6,
    "cq12_boq_amount_arithmetic.rq": 6,
    "cq13_boq_cost_component_reconciliation.rq": 6,
    "cq14_quantity_basis_unit_conversion.rq": 6,
    "cq15_summary_rollup_reconciliation_gap.rq": 1,
    "cq16_boq_partial_summary_coverage.rq": 3,
    "cq17_direct_cost_matches_rc_summary.rq": 1,
    "cq18_cost_basis_transitive_dependency.rq": 4,
    "cq19_concrete_spec_reuse_trace.rq": 2,
    "cq20_rebar_spec_reuse_trace.rq": 2,
    "cq21_formwork_shoring_spec_split.rq": 2,
    "cq22_boq_source_traceability.rq": 6,
    "cq23_required_optional_field_distribution.rq": 2,
    "cq24_missing_required_boq_field_count.rq": 1,
    "cq25_missing_quantity_basis_count.rq": 1,
    "cq26_missing_specification_object_count.rq": 1,
    "cq27_specification_reference_counts.rq": 4,
    "cq28_worktype_cross_document_coverage.rq": 3,
    "cq29_cost_category_coverage.rq": 4,
    "cq30_schema_class_property_profile.rq": 1,
}


def term_to_text(value) -> str:
    return "" if value is None else value.n3()


def main() -> None:
    graph = Graph()
    for path in DATA_FILES:
        graph.parse(path, format="turtle")

    summary_rows = []
    detail_payload = {
        "graph_triples": len(graph),
        "data_files": [str(path.relative_to(ROOT)) for path in DATA_FILES],
        "queries": [],
    }

    for query_path in sorted(SPARQL_DIR.glob("*.rq")):
        query = query_path.read_text(encoding="utf-8")
        result = list(graph.query(query))
        expected = EXPECTED_ROWS[query_path.name]
        passed = len(result) >= expected

        summary_rows.append({
            "query": query_path.name,
            "expected_min_rows": expected,
            "actual_rows": len(result),
            "passed": str(passed).lower(),
        })

        detail_payload["queries"].append({
            "query": query_path.name,
            "expected_min_rows": expected,
            "actual_rows": len(result),
            "passed": passed,
            "variables": [str(var) for var in result[0].labels] if result else [],
            "sample_rows": [
                [term_to_text(value) for value in row]
                for row in result[:5]
            ],
        })

    csv_path = EXPERIMENT_DIR / "sparql_execution_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["query", "expected_min_rows", "actual_rows", "passed"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    json_path = EXPERIMENT_DIR / "sparql_execution_results.json"
    json_path.write_text(
        json.dumps(detail_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    passed_count = sum(1 for row in summary_rows if row["passed"] == "true")
    print(f"graph_triples={len(graph)}")
    print(f"queries={len(summary_rows)}")
    print(f"passed={passed_count}")
    print(f"failed={len(summary_rows) - passed_count}")


if __name__ == "__main__":
    main()
