# New RDF/RDFS Experiment Report

## 1. 실험 개요

본 보고서는 현재 구축한 `공사기성부분 내역서` 중심 RDF/RDFS 온톨로지를 바탕으로 5개 RDF 기반 표현 조합을 비교 평가한 실험 내용을 정리한 문서이다.

실험의 목적은 다음과 같다.

1. 현재 RDF/RDFS 온톨로지가 연구 질문에 SPARQL로 응답 가능한지 확인한다.
2. 현재 RDF/RDFS 모델을 기준으로 4개 확장 조합을 추가 생성한다.
3. 5개 조합 모델을 Codex 평가 대상으로 넘기고, SPARQL 기반 질문지와 정답지를 이용해 어떤 조합이 가장 적합한지 판단한다.

평가 대상 조합은 다음 5개이다.

| 순번 | 조합 | 역할 |
| ---: | --- | --- |
| 1 | RDF/RDFS | 기준 모델 |
| 2 | RDF/RDFS + SKOS | 용어 체계 확장 모델 |
| 3 | RDF/RDFS + OWL 2 RL | 규칙 기반 경량 추론 확장 모델 |
| 4 | RDF/RDFS + OWL 2 DL | 표현력 중심 의미 추론 확장 모델 |
| 5 | RDF/RDFS + SHACL | 데이터 품질 검증 확장 모델 |

## 2. 실험 범위

실험 범위는 철근콘크리트 공종 전체 기성서류가 아니라, `공사기성부분 내역서`를 중심으로 한 문서 구조와 산정 구조이다.

대상 문서 계층은 다음과 같다.

```text
기성서류
└─ 철근콘크리트 공종 기성서류
   └─ 내역서
      └─ 공사기성부분 내역서
         ├─ 원가계산서
         ├─ 공종별집계표
         ├─ 공종별내역서
         └─ 수량산출서
```

공종 분개는 다음 수준에서 멈춘다.

| 문서 | 분개 |
| --- | --- |
| 원가계산서 | 철근콘크리트공사 직접공사비, 간접비 및 법정경비, 일반관리비 및 이윤, 세금 및 총액 |
| 공종별집계표 | 콘크리트공사, 철근공사, 거푸집 및 동바리공사 |
| 공종별내역서 | 콘크리트공사, 철근공사, 거푸집 및 동바리공사 |
| 수량산출서 | 콘크리트공사, 철근공사, 거푸집 및 동바리공사 |

콘크리트 강도, 슬럼프, 철근 강종, 직경, 거푸집 종류 같은 값은 공종 계층 노드로 더 분개하지 않고, `Specification` 계열 규격 객체와 속성으로 표현한다.

## 3. 사용 파일

| 구분 | 파일 |
| --- | --- |
| 기준 온톨로지 | `ontology/ontology.ttl` |
| 샘플 RDF 데이터 | `ontology/sample_data.ttl` |
| RDF/RDFS 구축 설명서 | `RDF&RDFS_New_Report.md` |
| 시각화 파일 | `visualization/ontology_graph.html` |
| 기존 CQ 실행기 | `experiments/codex_5_combination_2026-07-07/run_sparql_evaluation.py` |
| 모델 비교 실행기 | `experiments/codex_5_combination_2026-07-07/run_model_combination_evaluation.py` |
| 5개 조합 manifest | `experiments/codex_5_combination_2026-07-07/models/model_manifest.json` |
| 모델 평가 정답지 | `experiments/codex_5_combination_2026-07-07/evaluation/model_capability_answer_key.json` |
| 모델 평가 SPARQL | `experiments/codex_5_combination_2026-07-07/evaluation/model_capability_sparql/*.rq` |

## 4. 실행 환경

실험은 로컬 저장소 `/home/jiwon/Reinforced_Concrete_Ontology_Construction`에서 실행하였다.

| 항목 | 값 |
| --- | --- |
| 실행일 | 2026-07-07 |
| 평가 주체 | Codex |
| Codex 기반 모델 | GPT-5 기반 Codex coding agent |
| Codex CLI | `codex-cli 0.142.5` |
| Python | `3.13.14` |
| RDF 라이브러리 | `rdflib 7.6.0` |
| pandas | `3.0.3` |
| openpyxl | `3.1.5` |
| SPARQLWrapper | `2.0.0` |
| Java | OpenJDK `21.0.11` |
| 시각화 라이브러리 | D3.js 7.x CDN |

Codex의 정확한 서버 측 모델 빌드 번호는 로컬 실행 환경에서 직접 노출되지 않는다. 따라서 본 보고서에서는 사용 가능한 범위에서 `GPT-5 기반 Codex coding agent`와 `codex-cli 0.142.5`를 기록한다.

## 5. 실험 방법론

본 실험은 두 단계로 수행하였다.

### 5.1 RDF/RDFS 기준 그래프 검증

먼저 `ontology/ontology.ttl`과 `ontology/sample_data.ttl`을 하나의 RDF 그래프로 로드하였다.

그다음 30개 competency question을 SPARQL로 실행해 현재 RDF/RDFS 그래프가 연구에 필요한 질문에 답할 수 있는지 확인하였다.

실행 명령은 다음과 같다.

```bash
/home/jiwon/anaconda3/envs/RC_Ontology/bin/python experiments/codex_5_combination_2026-07-07/run_sparql_evaluation.py
```

실행 결과는 다음과 같다.

```text
graph_triples=1327
queries=30
passed=30
failed=0
```

### 5.2 5개 조합 모델 생성 및 평가

두 번째 단계에서는 기준 RDF/RDFS 모델에 4개 확장 모델을 추가하였다.

| 조합 | 추가 파일 |
| --- | --- |
| RDF/RDFS | 없음 |
| RDF/RDFS + SKOS | `models/rdf_rdfs_skos/skos_extension.ttl` |
| RDF/RDFS + OWL 2 RL | `models/rdf_rdfs_owl2rl/owl2rl_extension.ttl` |
| RDF/RDFS + OWL 2 DL | `models/rdf_rdfs_owl2dl/owl2dl_extension.ttl` |
| RDF/RDFS + SHACL | `models/rdf_rdfs_shacl/shacl_shapes.ttl` |

각 모델은 항상 기준 파일 2개를 먼저 로드한다.

```text
ontology/ontology.ttl
ontology/sample_data.ttl
```

그 뒤 각 조합별 확장 TTL을 추가로 로드한다. 평가에는 40개 SPARQL `ASK` 질의와 정답지를 사용하였다.

실행 명령은 다음과 같다.

```bash
/home/jiwon/anaconda3/envs/RC_Ontology/bin/python experiments/codex_5_combination_2026-07-07/run_model_combination_evaluation.py
```

실행 결과는 다음과 같다.

```text
models=5
queries=40
model_query_pairs=200
answer_key_matches=200
answer_key_mismatches=0
winner=RDF/RDFS + OWL 2 DL
winner_score=64.0/114.0
```

## 6. SPARQL 질문지 구성

모델 비교 실험의 40개 SPARQL 질문은 다음 5개 영역으로 구성하였다.

| 평가 영역 | 질의 수 | 배점 | 평가 내용 |
| --- | ---: | ---: | --- |
| RDF/RDFS 기본 구조 | 7 | 14 | 문서 계층, 하위 문서, 공종 구간, 규격 공유, 원가 근거 경로, 표준 행 포맷, 원본 출처 추적 |
| SKOS 용어 체계 | 7 | 14 | concept scheme, broader/narrower, 문서유형 매핑, 규격 altLabel, 인스턴스-concept 연결, 세부 분류 concept coverage, 다국어/동의어 label |
| OWL 추론 구조 | 7 | 21 | ontology 선언, inverse property, transitive property, property chain, lightweight restriction, property typing, 규격 class disjointness |
| OWL 2 DL 표현력 | 8 | 32 | equivalentClass, qualified cardinality, disjoint union, hasKey, 하위 문서 restriction, 내역 literal cardinality, 수량산출 역관계 cardinality |
| SHACL 데이터 검증 | 11 | 33 | 필수 필드, datatype, 규격 객체, 수량산출 근거, 금액 산식, 단위 변환, 직접공사비 검증, 하위 문서 qualified shape, 집계금액 필수 필드 |
| 합계 | 40 | 114 | 전체 모델 능력 평가 |

SPARQL 질문은 각 모델이 특정 표현 장치를 실제 TTL 그래프 안에 가지고 있는지 확인하는 방식으로 작성하였다. 예를 들어 OWL 2 DL 조합은 `owl:equivalentClass`, `owl:qualifiedCardinality`, `owl:disjointUnionOf`, `owl:hasKey`를 갖는지 확인하고, SHACL 조합은 `sh:NodeShape`, `sh:property`, `sh:sparql` 제약을 갖는지 확인한다.

### 6.1 모델 평가 SPARQL 질의 40개

아래 표는 5개 조합 모델 평가에 사용한 40개 SPARQL `ASK` 질의의 전체 목록이다. `정답 조합`은 해당 질의가 `true`로 평가되어야 하는 모델을 의미한다.

| ID | SPARQL 파일 | 평가 영역 | 배점 | 질의 내용 | 정답 조합 |
| --- | --- | --- | ---: | --- | --- |
| MQ01 | `mq01_core_rdfs_document_class_hierarchy.rq` | RDF/RDFS 기본 구조 | 2 | 기성서류부터 공사기성부분 내역서까지 RDFS 문서 class 계층을 보존하는가 | 5개 전체 |
| MQ02 | `mq02_core_statement_four_subdocuments.rq` | RDF/RDFS 기본 구조 | 2 | 공사기성부분 내역서가 원가계산서, 공종별집계표, 공종별내역서, 수량산출서 4개 하위 문서를 포함하는가 | 5개 전체 |
| MQ03 | `mq03_core_cross_document_worktype_sections.rq` | RDF/RDFS 기본 구조 | 2 | 공종별집계표, 공종별내역서, 수량산출서에 콘크리트공사, 철근공사, 거푸집 및 동바리공사 구간이 모두 보존되는가 | 5개 전체 |
| MQ04 | `mq04_core_shared_specification_trace.rq` | RDF/RDFS 기본 구조 | 2 | 내역 항목과 수량산출 항목이 같은 규격 객체를 공유 참조하는가 | 5개 전체 |
| MQ05 | `mq05_core_cost_basis_path.rq` | RDF/RDFS 기본 구조 | 2 | 원가 항목에서 철근콘크리트공사 집계금액까지 원가 산정 근거 경로가 존재하는가 | 5개 전체 |
| MQ06 | `mq06_skos_concept_scheme_top_concepts.rq` | SKOS 용어 체계 | 2 | 문서유형, 공종, 세부 작업 분류, 규격 유형을 top concept로 갖는 SKOS concept scheme이 있는가 | RDF/RDFS + SKOS |
| MQ07 | `mq07_skos_worktype_broader_narrower.rq` | SKOS 용어 체계 | 2 | 철근콘크리트공사와 하위 공종이 SKOS broader/narrower 관계로 관리되는가 | RDF/RDFS + SKOS |
| MQ08 | `mq08_skos_document_type_mapping.rq` | SKOS 용어 체계 | 2 | 문서유형 concept가 온톨로지 class와 SKOS mapping property로 연결되는가 | RDF/RDFS + SKOS |
| MQ09 | `mq09_skos_specification_alt_labels.rq` | SKOS 용어 체계 | 2 | 콘크리트 배합, 철근 규격, 거푸집 규격 concept에 prefLabel과 altLabel이 정의되는가 | RDF/RDFS + SKOS |
| MQ10 | `mq10_skos_instance_concept_mapping.rq` | SKOS 용어 체계 | 2 | 공종 인스턴스와 규격 인스턴스가 SKOS concept와 연결되는가 | RDF/RDFS + SKOS |
| MQ11 | `mq11_owl_ontology_declaration.rq` | OWL 추론 구조 | 3 | 조합 모델이 OWL ontology 확장으로 선언되어 있는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ12 | `mq12_owl_inverse_properties.rq` | OWL 추론 구조 | 3 | 포함 관계, 수량산출 근거 관계, 집계 관계에 inverse property가 정의되어 있는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ13 | `mq13_owl_transitive_properties.rq` | OWL 추론 구조 | 3 | 공종 계층과 원가 산정 근거 관계에 transitive property가 정의되어 있는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ14 | `mq14_owl_property_chain_trace.rq` | OWL 추론 구조 | 3 | 내역 항목에서 수량산출 근거와 집계금액을 연결하는 property chain axiom이 있는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ15 | `mq15_owl_rl_lightweight_somevalues_restrictions.rq` | OWL 추론 구조 | 3 | OWL 2 RL식 경량 `someValuesFrom` restriction으로 내역 항목의 수량산출 근거, 집계 대상, 규격 객체를 표현하는가 | RDF/RDFS + OWL 2 RL |
| MQ16 | `mq16_owl_dl_equivalent_traceable_boq_item.rq` | OWL 2 DL 표현력 | 4 | `TraceableBoQItem`을 내역 항목, 수량산출 근거, 집계 대상, 규격 객체 restriction의 intersection equivalent class로 정의하는가 | RDF/RDFS + OWL 2 DL |
| MQ17 | `mq17_owl_dl_boq_key.rq` | OWL 2 DL 표현력 | 4 | 원본 파일명, 시트명, 행 번호를 기준으로 내역 항목 식별용 OWL key를 정의하는가 | RDF/RDFS + OWL 2 DL |
| MQ18 | `mq18_owl_dl_specification_disjoint_union.rq` | OWL 2 DL 표현력 | 4 | `Specification`을 콘크리트 배합, 철근 규격, 거푸집 규격, 형강 규격의 disjoint union으로 정의하는가 | RDF/RDFS + OWL 2 DL |
| MQ19 | `mq19_owl_dl_concrete_mix_cardinality.rq` | OWL 2 DL 표현력 | 4 | 콘크리트 배합 규격의 설계기준강도, 슬럼프, 굵은골재 최대치수를 정확한 datatype cardinality로 표현하는가 | RDF/RDFS + OWL 2 DL |
| MQ20 | `mq20_owl_dl_rebar_spec_cardinality.rq` | OWL 2 DL 표현력 | 4 | 철근 규격의 강종과 직경을 정확한 datatype cardinality로 표현하는가 | RDF/RDFS + OWL 2 DL |
| MQ21 | `mq21_owl_dl_statement_subdocument_restrictions.rq` | OWL 2 DL 표현력 | 4 | 공사기성부분 내역서가 4개 필수 하위 문서 유형을 포함한다는 OWL restriction을 표현하는가 | RDF/RDFS + OWL 2 DL |
| MQ22 | `mq22_shacl_statement_metadata_shape.rq` | SHACL 데이터 검증 | 3 | 공사기성부분 내역서의 공사명, 기성회차, 기준일 필수 metadata shape가 정의되어 있는가 | RDF/RDFS + SHACL |
| MQ23 | `mq23_shacl_boq_required_literal_fields.rq` | SHACL 데이터 검증 | 3 | 내역 항목의 품명, 규격, 단위, 금회수량, 단가, 금액 필수 literal field와 datatype을 검증하는가 | RDF/RDFS + SHACL |
| MQ24 | `mq24_shacl_boq_traceability_shapes.rq` | SHACL 데이터 검증 | 3 | 내역 항목이 규격 객체, 수량산출 근거, 집계 대상과 반드시 연결되도록 검증하는가 | RDF/RDFS + SHACL |
| MQ25 | `mq25_shacl_quantity_item_shape.rq` | SHACL 데이터 검증 | 3 | 수량산출 항목의 항목명, 위치, 부재명, 산출수량, 내역 항목 역참조 필드를 검증하는가 | RDF/RDFS + SHACL |
| MQ26 | `mq26_shacl_specification_shapes.rq` | SHACL 데이터 검증 | 3 | 콘크리트 배합, 철근 규격, 거푸집 규격 객체의 필수 규격 속성을 SHACL shape로 검증하는가 | RDF/RDFS + SHACL |
| MQ27 | `mq27_shacl_boq_amount_arithmetic_constraint.rq` | SHACL 데이터 검증 | 3 | 내역 항목의 금회수량 x 단가 = 금액 산식을 SHACL SPARQL constraint로 검증하는가 | RDF/RDFS + SHACL |
| MQ28 | `mq28_shacl_cost_component_reconciliation_constraint.rq` | SHACL 데이터 검증 | 3 | 재료비, 노무비, 경비 금액 합계가 내역 항목 총금액과 일치하는지 검증하는가 | RDF/RDFS + SHACL |
| MQ29 | `mq29_shacl_quantity_basis_unit_conversion_constraint.rq` | SHACL 데이터 검증 | 3 | 수량산출 근거와 내역 항목 수량이 kg-to-ton 같은 단위 변환을 고려해 일치하는지 검증하는가 | RDF/RDFS + SHACL |
| MQ30 | `mq30_shacl_direct_cost_reconciliation_constraint.rq` | SHACL 데이터 검증 | 3 | 철근콘크리트공사 직접공사비가 철근콘크리트공사 집계금액 근거와 일치하는지 검증하는가 | RDF/RDFS + SHACL |
| MQ31 | `mq31_core_boq_table_format_required_fields.rq` | RDF/RDFS 기본 구조 | 2 | 공종별내역서 표준 행 포맷이 품명, 규격, 단위, 금회수량, 단가, 금액 필드를 정의하는가 | 5개 전체 |
| MQ32 | `mq32_core_boq_source_traceability_completeness.rq` | RDF/RDFS 기본 구조 | 2 | 모든 내역 항목이 원본 시트, 행 번호, 셀 주소, 계층 경로, 공종명, 세부 분류명 출처를 보존하는가 | 5개 전체 |
| MQ33 | `mq33_skos_detail_category_concept_coverage.rq` | SKOS 용어 체계 | 2 | SKOS 확장이 세부 작업 분류 concept를 포함하고 온톨로지 class와 매핑하는가 | RDF/RDFS + SKOS |
| MQ34 | `mq34_skos_multilingual_and_synonym_labels.rq` | SKOS 용어 체계 | 2 | 주요 공종 및 세부 분류 concept에 한국어 prefLabel과 동의어/다국어 altLabel이 있는가 | RDF/RDFS + SKOS |
| MQ35 | `mq35_owl_property_typing_for_core_relations.rq` | OWL 추론 구조 | 3 | 핵심 추적 관계는 OWL object property로, 값 필드는 datatype property로 타입 지정되는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ36 | `mq36_owl_specification_class_disjointness.rq` | OWL 추론 구조 | 3 | 콘크리트, 철근, 거푸집, 형강 규격 class 간 배타성이 OWL로 표현되는가 | RDF/RDFS + OWL 2 RL, RDF/RDFS + OWL 2 DL |
| MQ37 | `mq37_owl_dl_boq_literal_cardinality.rq` | OWL 2 DL 표현력 | 4 | 내역 항목의 단위, 금회수량, 금액이 정확한 datatype cardinality로 표현되는가 | RDF/RDFS + OWL 2 DL |
| MQ38 | `mq38_owl_dl_quantity_basis_inverse_cardinality.rq` | OWL 2 DL 표현력 | 4 | 수량산출 항목이 적어도 하나의 내역 항목 수량 근거가 되도록 OWL 2 DL cardinality로 표현되는가 | RDF/RDFS + OWL 2 DL |
| MQ39 | `mq39_shacl_statement_subdocument_qualified_shapes.rq` | SHACL 데이터 검증 | 3 | 공사기성부분 내역서가 4개 하위 문서 유형을 각각 1개씩 갖도록 SHACL qualified shape로 검증하는가 | RDF/RDFS + SHACL |
| MQ40 | `mq40_shacl_summary_amount_required_fields.rq` | SHACL 데이터 검증 | 3 | 집계금액의 금회금액, 누계금액, 기성률 필수 필드와 datatype을 SHACL shape로 검증하는가 | RDF/RDFS + SHACL |

## 7. 모델 능력 평가 결과

| 순위 | 조합 | 그래프 트리플 수 | 능력 점수 | 정규화 점수 | 정답지 일치 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | RDF/RDFS + OWL 2 DL | 1,505 | 64.0 / 114.0 | 56.14 | 40 / 40 |
| 2 | RDF/RDFS + SHACL | 1,497 | 47.0 / 114.0 | 41.23 | 40 / 40 |
| 3 | RDF/RDFS + OWL 2 RL | 1,404 | 35.0 / 114.0 | 30.70 | 40 / 40 |
| 4 | RDF/RDFS + SKOS | 1,480 | 28.0 / 114.0 | 24.56 | 40 / 40 |
| 5 | RDF/RDFS | 1,327 | 14.0 / 114.0 | 12.28 | 40 / 40 |

해석하면, 기준 RDF/RDFS는 기본 구조 10점을 모두 만족하지만 확장 기능은 없다. SKOS 조합은 용어 체계 영역을 모두 만족한다. OWL 2 RL은 경량 추론 구조를 만족한다. OWL 2 DL은 OWL 추론 구조 일부와 OWL 2 DL 표현력 영역을 만족한다. SHACL은 데이터 품질 검증 영역을 모두 만족한다.

## 8. 기준별 상세 점수

| 조합 | RDF/RDFS 기본 구조 | SKOS 용어 체계 | OWL 추론 구조 | OWL 2 DL 표현력 | SHACL 데이터 검증 |
| --- | ---: | ---: | ---: | ---: | ---: |
| RDF/RDFS | 14.0 / 14.0 | 0.0 / 14.0 | 0.0 / 21.0 | 0.0 / 32.0 | 0.0 / 33.0 |
| RDF/RDFS + SKOS | 14.0 / 14.0 | 14.0 / 14.0 | 0.0 / 21.0 | 0.0 / 32.0 | 0.0 / 33.0 |
| RDF/RDFS + OWL 2 RL | 14.0 / 14.0 | 0.0 / 14.0 | 21.0 / 21.0 | 0.0 / 32.0 | 0.0 / 33.0 |
| RDF/RDFS + OWL 2 DL | 14.0 / 14.0 | 0.0 / 14.0 | 18.0 / 21.0 | 32.0 / 32.0 | 0.0 / 33.0 |
| RDF/RDFS + SHACL | 14.0 / 14.0 | 0.0 / 14.0 | 0.0 / 21.0 | 0.0 / 32.0 | 33.0 / 33.0 |

OWL 2 DL 조합이 OWL 추론 구조에서 21점 중 18점을 받은 이유는 OWL 2 RL 전용 lightweight `someValuesFrom` 질의 1개를 의도적으로 만족하지 않도록 모델을 분리했기 때문이다. 대신 OWL 2 DL 조합은 qualified cardinality, equivalent class, disjoint union, key 등 표현력 중심 항목을 모두 만족한다.

## 9. Codex 정성 평가 지표

모델 능력 SPARQL 평가와 별도로, Codex는 연구 목적 적합성을 보기 위해 10개 정성 지표를 사용하였다. 각 항목은 10점 만점이며 총점은 100점 만점이다.

| ID | 평가지표 | 평가 내용 |
| --- | --- | --- |
| C1 | 문서 계층 표현성 | 기성서류부터 공사기성부분 내역서 및 하위 문서까지 표현하는가 |
| C2 | 공종 및 원가 분개 적합성 | 원가계산서와 공종별 문서의 분개 차이를 적절히 표현하는가 |
| C3 | 속성 및 규격 표현성 | 강도, 슬럼프, 강종, 직경 등을 노드가 아닌 속성/규격 객체로 표현하는가 |
| C4 | 추적성 | 내역 항목, 수량산출, 집계, 원가 항목을 연결할 수 있는가 |
| C5 | 값 검증 가능성 | 필수값, 자료형, 단위, 금액 산식을 검증할 수 있는가 |
| C6 | 추론 가능성 | 클래스 계층, 관계 제약, 역관계, cardinality 등을 추론할 수 있는가 |
| C7 | 질의 가능성 | SPARQL 질의 및 구조 탐색이 쉬운가 |
| C8 | 재사용 및 확장 가능성 | 다른 회차, 다른 공종, 다른 현장으로 확장 가능한가 |
| C9 | 유지보수성과 모델 복잡도 | 모델이 과도하게 복잡하지 않고 관리 가능한가 |
| C10 | 현재 연구 목적 적합성 | 의미 구조화 비교 평가 연구에 적합한가 |

## 10. Codex 정성 평가 점수

| 조합 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | 총점 | 순위 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RDF/RDFS + OWL 2 DL | 9.0 | 9.0 | 9.5 | 8.5 | 6.5 | 9.5 | 8.5 | 9.0 | 6.5 | 9.0 | 85.0 | 1 |
| RDF/RDFS + SHACL | 8.5 | 8.5 | 8.5 | 9.0 | 9.5 | 5.5 | 8.0 | 8.5 | 8.0 | 9.0 | 83.0 | 2 |
| RDF/RDFS + OWL 2 RL | 8.5 | 8.5 | 8.5 | 8.0 | 4.5 | 7.5 | 8.0 | 8.0 | 7.0 | 8.0 | 76.5 | 3 |
| RDF/RDFS + SKOS | 8.0 | 8.5 | 8.0 | 7.5 | 2.5 | 3.5 | 8.0 | 8.0 | 8.0 | 7.0 | 69.0 | 4 |
| RDF/RDFS | 8.0 | 8.0 | 7.0 | 7.0 | 2.0 | 2.0 | 7.0 | 7.0 | 9.0 | 6.0 | 63.0 | 5 |

정성 평가에서도 최종 1위는 `RDF/RDFS + OWL 2 DL`이다. SHACL은 값 검증 가능성에서 가장 강하지만, 의미 구조화와 추론 표현력 중심의 연구 목적에서는 OWL 2 DL이 더 높은 점수를 받았다.

## 11. 조합별 해석

### 11.1 RDF/RDFS

RDF/RDFS는 기준 모델로 적합하다. 문서 계층, domain/range, class hierarchy, 기본 관계를 명확히 표현할 수 있다. 그러나 필수 속성, cardinality, 산식 검증, 값 범위 검증, 역관계 추론을 직접 표현하기 어렵다.

### 11.2 RDF/RDFS + SKOS

SKOS는 문서유형, 공종, 세부 작업 분류, 규격 용어를 통제어휘로 관리하는 데 강하다. `철근공사`, `콘크리트공사`, `거푸집 및 동바리공사`, `강종-직경`, `강도-골재-슬럼프` 같은 용어를 broader/narrower, prefLabel, altLabel로 관리할 수 있다. 다만 값 검증이나 복잡한 의미 제약에는 약하다.

### 11.3 RDF/RDFS + OWL 2 RL

OWL 2 RL은 inverse property, transitive property, property chain, lightweight restriction을 통해 운영형 추론을 지원한다. 추론 비용을 낮게 유지하면서 RDF/RDFS보다 풍부한 의미 관계를 표현할 수 있다. 그러나 qualified cardinality나 disjoint union 같은 정교한 의미 모델링은 OWL 2 DL보다 제한적이다.

### 11.4 RDF/RDFS + OWL 2 DL

OWL 2 DL은 본 실험의 최종 1위 조합이다. `TraceableBoQItem`, qualified cardinality, `owl:disjointUnionOf`, `owl:hasKey`, 하위 문서 restriction 등 의미 구조화에 필요한 표현 장치를 가장 풍부하게 제공한다. 연구 목적이 공사기성부분 내역서의 의미 구조화 표현 방식 비교라면 OWL 2 DL이 가장 적합하다.

### 11.5 RDF/RDFS + SHACL

SHACL은 실무 데이터 검증에 가장 강한 조합이다. 필수 필드, datatype, 수량산출 근거, 금액 산식, 재료비/노무비/경비 합계, kg-ton 단위 변환, 직접공사비와 집계금액 일치성을 직접 검증할 수 있다. 다만 SHACL은 데이터 검증 언어이므로 OWL 2 DL 수준의 클래스 의미론과 추론 표현력은 제공하지 않는다.

## 12. 최종 결론

본 실험의 최종 결론은 다음과 같다.

```text
연구 목적의 의미 구조화 최적 조합: RDF/RDFS + OWL 2 DL
실무 데이터 품질 검증 최적 조합: RDF/RDFS + SHACL
최종 1위 조합: RDF/RDFS + OWL 2 DL
```

`RDF/RDFS + OWL 2 DL`은 문서 계층, 내역 항목, 수량산출 근거, 집계금액, 원가 항목, 규격 객체 간 관계를 가장 풍부한 의미 제약으로 표현할 수 있다. 따라서 현재 연구의 핵심 목적인 “철근콘크리트 공종 공사기성부분 내역서의 의미적 구조화 표현 방식 비교”에는 OWL 2 DL 조합이 가장 적합하다.

다만 실제 현장 데이터 품질 관리와 값 검증까지 포함하는 후속 연구에서는 `RDF/RDFS + OWL 2 DL + SHACL`의 복합 적용을 검토할 수 있다.

## 13. 실험 한계

이번 실험은 SPARQL 기반 모델 능력 평가이다. 즉, 각 모델이 필요한 표현 장치를 TTL 그래프 안에 가지고 있는지를 확인하였다.

아직 수행하지 않은 항목은 다음과 같다.

| 항목 | 수행 여부 |
| --- | --- |
| OWL 2 DL reasoner 실제 추론 실행 | 미수행 |
| OWL 2 RL rule reasoner 실제 추론 실행 | 미수행 |
| SHACL validator 실제 validation report 생성 | 미수행 |
| 실제 원본 문서 전체 데이터 자동 추출 | 미수행 |
| 모든 샘플 값의 원문 대조 검증 | 미수행 |

따라서 본 실험 결과는 “모델 표현 능력 비교”로 해석해야 하며, 실제 reasoner/validator 실행 결과와는 구분해야 한다.

## 14. 산출물 위치

| 산출물 | 파일 |
| --- | --- |
| 모델 선택 보고서 | `experiments/codex_5_combination_2026-07-07/CODEX_Model_Selection_Report.md` |
| 전체 실험 결과 JSON | `experiments/codex_5_combination_2026-07-07/codex_results.json` |
| 정성 점수 CSV | `experiments/codex_5_combination_2026-07-07/codex_scores.csv` |
| 모델 능력 점수 CSV | `experiments/codex_5_combination_2026-07-07/model_capability_scores.csv` |
| 기준별 점수 CSV | `experiments/codex_5_combination_2026-07-07/model_capability_criterion_scores.csv` |
| 모델 능력 상세 JSON | `experiments/codex_5_combination_2026-07-07/model_capability_results.json` |
| RDF/RDFS CQ 실행 결과 CSV | `experiments/codex_5_combination_2026-07-07/sparql_execution_results.csv` |
| RDF/RDFS CQ 실행 결과 JSON | `experiments/codex_5_combination_2026-07-07/sparql_execution_results.json` |
