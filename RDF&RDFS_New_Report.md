# RDF/RDFS New Report

## 1. 구축 목적

본 보고서는 현재 저장소의 `ontology/ontology.ttl`, `ontology/sample_data.ttl`, `visualization/ontology_graph.html`을 기준으로 작성한 RDF/RDFS 구축 설명서이다. 대상 범위는 철근콘크리트 공종 전체 기성서류가 아니라, 그중 `공사기성부분 내역서`를 중심으로 한 문서 계층, 공종 분개, 원가·집계·내역·수량산출·규격 속성 체계이다.

이 버전의 핵심 판단은 다음과 같다.

- 공종 분개는 `공사기성부분 내역서 -> 원가계산서 / 공종별집계표 / 공종별내역서 / 수량산출서`와 각 문서의 공종 구간 수준에서 멈춘다.
- 콘크리트 강도, 슬럼프, 철근 강종, 철근 직경, 유로폼, H형강 같은 값은 그래프 노드로 분개하지 않고 `Specification` 계열 객체의 속성으로 둔다.
- 시각화에서는 속성값을 별도 노드로 표시하지 않고, 노드를 클릭했을 때 오른쪽 상세 정보 패널에 속성 체계를 보여준다.
- `BoQItem`은 금액 산정의 중심 원본 행이고, `QuantityCalculationItem`은 수량 산정의 중심 원본 행이다.
- 규격 객체는 `BoQItem` 또는 `QuantityCalculationItem` 중 한쪽에 종속시키지 않고, 둘 다 공유 참조할 수 있게 `SpecifiableRecord`를 둔다.

## 2. IRI 및 Prefix 설계

현재 온톨로지는 아래 namespace를 사용한다.

| Prefix | IRI | 용도 |
| --- | --- | --- |
| `ppdoc:` | `https://example.org/rc-progress-payment#` | 본 연구에서 정의한 공사기성부분 내역서 온톨로지 |
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF 기본 타입 및 property 선언 |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Class, label, comment, domain, range, subclass 표현 |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | 문자열, 정수, 소수, 날짜, boolean 자료형 |
| `dcterms:` | `http://purl.org/dc/terms/` | 온톨로지 제목과 설명 메타데이터 |

IRI 작성 규칙은 다음과 같다.

```text
Full IRI = https://example.org/rc-progress-payment# + Local Name
예: ppdoc:ProgressPaymentStatement
 -> https://example.org/rc-progress-payment#ProgressPaymentStatement

예: ppdoc:hasProjectName
 -> https://example.org/rc-progress-payment#hasProjectName
```

현재 namespace는 연구용 예시 IRI이다. 외부 공개나 논문 부록용 배포 시에는 `example.org` 대신 연구기관, 프로젝트, 저장소 기반의 실제 namespace로 교체하는 것이 바람직하다.

## 3. RDF/RDFS 구축 범위

구축 범위는 아래 3개 파일에 나뉘어 있다.

| 파일 | 역할 |
| --- | --- |
| `ontology/ontology.ttl` | RDF/RDFS 스키마. 클래스, 관계, 속성, domain/range, subclass 구조 정의 |
| `ontology/sample_data.ttl` | 스키마에 맞춘 예시 인스턴스. 문서, 공종 구간, 내역 항목, 수량산출 항목, 규격 객체 예시 포함 |
| `visualization/ontology_graph.html` | RDF/RDFS 구조를 사람이 보기 쉽게 시각화한 HTML. 분개 노드와 클릭형 속성 패널 포함 |

현재 `ontology.ttl` 기준 구성량은 다음과 같다.

| 구분 | 수량 | 설명 |
| --- | ---: | --- |
| RDFS Class | 65개 | 문서, 레코드, 공종, 세부 분류, 규격, 수량산출, 정보필드 클래스 |
| RDF Property | 105개 | 관계형 property와 데이터 속성 property를 모두 `rdf:Property`로 선언 |
| 시각화 노드 | 22개 | 문서 계층, 원가 구간, 집계 구간, 내역 구간, 수량산출 구간 |
| 시각화 링크 | 21개 | `hasPart`, `hasWorkTypeSection`, `hasCostItem` 관계 |

RDFS만 사용하기 때문에 `owl:ObjectProperty`, `owl:DatatypeProperty`, `owl:Restriction`은 사용하지 않았다. 대신 `rdfs:domain`, `rdfs:range`, `rdfs:subClassOf`, `rdfs:subPropertyOf`로 구조를 표현했다.

## 4. 전체 분개 구조

### 4.1 1차 문서 분개

1차 분개는 문서 계층을 정의한다.

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

이 구조는 서류의 정형 포맷을 유지하기 위한 상위 계층이다. 공종 분개나 규격 속성을 붙이더라도 이 문서 계층은 변경하지 않는다.

### 4.2 2차 공종 및 원가 분개

2차 분개는 하위 문서별 성격에 맞게 다르게 적용한다.

```text
공사기성부분 내역서
  ├─ 원가계산서
  │   └─ 철근콘크리트공사 원가계산 구간
  │       ├─ 직접공사비
  │       ├─ 간접비 및 법정경비
  │       ├─ 일반관리비 및 이윤
  │       └─ 세금 및 총액
  ├─ 공종별집계표
  │   ├─ 콘크리트공사 집계 구간
  │   ├─ 철근공사 집계 구간
  │   └─ 거푸집 및 동바리공사 집계 구간
  ├─ 공종별내역서
  │   ├─ 콘크리트공사 내역 구간
  │   ├─ 철근공사 내역 구간
  │   └─ 거푸집 및 동바리공사 내역 구간
  └─ 수량산출서
      ├─ 콘크리트공사 수량산출 구간
      ├─ 철근공사 수량산출 구간
      └─ 거푸집 및 동바리공사 수량산출 구간
```

원가계산서는 콘크리트공사, 철근공사, 거푸집 및 동바리공사로 직접 쪼개지 않는다. 원가계산서는 총괄 원가 산정 성격이 강하므로, 철근콘크리트공사에 배부되는 원가 항목으로만 분개한다. 반면 공종별집계표, 공종별내역서, 수량산출서는 공종별 행 또는 공종별 산출 근거가 있으므로 콘크리트공사, 철근공사, 거푸집 및 동바리공사 구간으로 분개한다.

### 4.3 분개를 멈춘 지점

아래 값들은 더 이상 공종 계층으로 분개하지 않는다.

| 공종 | 노드로 만들지 않는 값 | 처리 위치 |
| --- | --- | --- |
| 콘크리트공사 | 강도, 슬럼프, 골재치수, 배합코드, 타설 방식 | `ConcreteMix` 또는 `BoQItem` 속성 |
| 철근공사 | SD400, HD13, 공칭직경, 항복강도, 철근 종류 | `RebarSpec` 속성 |
| 거푸집 및 동바리공사 | 유로폼, H형강, 단면치수, 재질, 지지 방식 | `FormworkSpec`, `SteelShapeSpec` 속성 |

이 판단을 적용한 이유는 강도, 직경, 형상, 유로폼이 작업 계층이 아니라 내역 항목의 규격 또는 산출 조건이기 때문이다. 따라서 그래프는 문서·공종 구간을 보여주고, 규격 속성은 우측 패널과 RDF 속성으로 관리한다.

## 5. RDFS Class 구성

현재 모든 클래스는 `rdfs:Class`로 선언되어 있다. 최상위 클래스는 `ppdoc:ProgressPaymentEntity`이다.

### 5.1 핵심 상위 클래스

| Class | Full IRI | 의미 |
| --- | --- | --- |
| `ppdoc:ProgressPaymentEntity` | `https://example.org/rc-progress-payment#ProgressPaymentEntity` | 전체 온톨로지 최상위 개체 |
| `ppdoc:DocumentResource` | `https://example.org/rc-progress-payment#DocumentResource` | 문서 또는 문서군 상위 클래스 |
| `ppdoc:DocumentGroup` | `https://example.org/rc-progress-payment#DocumentGroup` | 여러 문서를 묶는 문서군 |
| `ppdoc:Document` | `https://example.org/rc-progress-payment#Document` | 개별 문서 또는 시트 |
| `ppdoc:DocumentRecord` | `https://example.org/rc-progress-payment#DocumentRecord` | 문서에서 추출한 원본 행 레코드 |
| `ppdoc:SpecifiableRecord` | `https://example.org/rc-progress-payment#SpecifiableRecord` | 규격 객체를 참조할 수 있는 원본 행 |
| `ppdoc:DerivedDataRecord` | `https://example.org/rc-progress-payment#DerivedDataRecord` | 원본 행에서 파생한 분류, 규격, 연결 정보 |
| `ppdoc:CanonicalDataFormat` | `https://example.org/rc-progress-payment#CanonicalDataFormat` | 원본 표를 정형화하기 위한 표준 포맷 |
| `ppdoc:InformationField` | `https://example.org/rc-progress-payment#InformationField` | 표준 포맷이 가지는 필드 정의 |

### 5.2 문서 계층 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:ProgressPaymentDocumentSet` | `ppdoc:DocumentGroup` | 기성서류 |
| `ppdoc:ReinforcedConcreteProgressPaymentDocuments` | `ppdoc:DocumentGroup` | 철근콘크리트 공종 기성서류 |
| `ppdoc:StatementDocument` | `ppdoc:DocumentGroup` | 내역서 문서군 |
| `ppdoc:ProgressPaymentStatement` | `ppdoc:DocumentGroup` | 공사기성부분 내역서 |
| `ppdoc:CostCalculationSheet` | `ppdoc:Document` | 원가계산서 |
| `ppdoc:WorkTypeSummarySheet` | `ppdoc:Document` | 공종별집계표 |
| `ppdoc:WorkTypeDetailSheet` | `ppdoc:Document` | 공종별내역서 |
| `ppdoc:QuantityCalculationSheet` | `ppdoc:Document` | 수량산출서 |

### 5.3 원본 레코드 및 산정 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:CostCalculationRecord` | `ppdoc:DocumentRecord` | 원가계산서 행 |
| `ppdoc:WorkTypeSummaryRecord` | `ppdoc:DocumentRecord` | 공종별집계표 행 |
| `ppdoc:BoQItemRecord` | `ppdoc:DocumentRecord` | 공종별내역서 원본 행 |
| `ppdoc:QuantityCalculationRecord` | `ppdoc:DocumentRecord` | 수량산출서 원본 행 |
| `ppdoc:BoQItem` | `ppdoc:BoQItemRecord`, `ppdoc:SpecifiableRecord` | 내역 항목 원본 행 |
| `ppdoc:SummaryAmount` | `ppdoc:WorkTypeSummaryRecord` | 집계 금액 |
| `ppdoc:CostItem` | `ppdoc:CostCalculationRecord` | 원가 항목 |
| `ppdoc:DirectCostItem` | `ppdoc:CostItem` | 직접공사비 항목 |
| `ppdoc:IndirectCostItem` | `ppdoc:CostItem` | 간접비 및 법정경비 항목 |
| `ppdoc:MarkupCostItem` | `ppdoc:CostItem` | 일반관리비 및 이윤 항목 |
| `ppdoc:TaxAndTotalCostItem` | `ppdoc:CostItem` | 세금 및 총액 항목 |

### 5.4 문서 내부 공종 구간 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:DocumentWorkTypeSection` | `ppdoc:ProgressPaymentEntity` | 문서 내부 공종 분개 구간 |
| `ppdoc:CostWorkTypeSection` | `ppdoc:DocumentWorkTypeSection` | 원가계산서의 공종 원가 구간 |
| `ppdoc:SummaryWorkTypeSection` | `ppdoc:DocumentWorkTypeSection` | 공종별집계표 공종 구간 |
| `ppdoc:DetailWorkTypeSection` | `ppdoc:DocumentWorkTypeSection` | 공종별내역서 공종 구간 |
| `ppdoc:QuantityWorkTypeSection` | `ppdoc:DocumentWorkTypeSection` | 수량산출서 공종 구간 |

### 5.5 공종 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:WorkType` | `ppdoc:ProgressPaymentEntity` | 공종 |
| `ppdoc:ReinforcedConcreteWork` | `ppdoc:WorkType` | 철근콘크리트공사 |
| `ppdoc:ConcreteWork` | `ppdoc:WorkType` | 콘크리트공사 |
| `ppdoc:RebarWork` | `ppdoc:WorkType` | 철근공사 |
| `ppdoc:FormworkAndShoringWork` | `ppdoc:WorkType` | 거푸집 및 동바리공사 |

### 5.6 세부 작업 분류 클래스

세부 작업 분류는 공종 계층 아래에서 반복적으로 등장하는 작업 유형을 설명하기 위한 클래스이다. 다만 이 분류는 현재 시각화에서 말단 노드로 펼치지 않는다.

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:DetailCategory` | `ppdoc:ProgressPaymentEntity` | 세부 작업 분류 |
| `ppdoc:ConcreteDetailCategory` | `ppdoc:DetailCategory` | 콘크리트 세부 작업 분류 |
| `ppdoc:ReadyMixedConcrete` | `ppdoc:ConcreteDetailCategory` | 레미콘 |
| `ppdoc:ConcretePlacement` | `ppdoc:ConcreteDetailCategory` | 콘크리트 타설 |
| `ppdoc:ConcretePumping` | `ppdoc:ConcreteDetailCategory` | 콘크리트 펌프 |
| `ppdoc:ConcreteCuring` | `ppdoc:ConcreteDetailCategory` | 콘크리트 양생 |
| `ppdoc:RebarDetailCategory` | `ppdoc:DetailCategory` | 철근 세부 작업 분류 |
| `ppdoc:RebarMaterial` | `ppdoc:RebarDetailCategory` | 철근 재료 |
| `ppdoc:RebarFabrication` | `ppdoc:RebarDetailCategory` | 철근 가공 |
| `ppdoc:RebarAssembly` | `ppdoc:RebarDetailCategory` | 철근 조립 |
| `ppdoc:RebarSplicing` | `ppdoc:RebarDetailCategory` | 철근 이음 |
| `ppdoc:FormworkDetailCategory` | `ppdoc:DetailCategory` | 거푸집 및 동바리 세부 작업 분류 |
| `ppdoc:FormworkInstallation` | `ppdoc:FormworkDetailCategory` | 거푸집 설치 |
| `ppdoc:FormworkRemoval` | `ppdoc:FormworkDetailCategory` | 거푸집 해체 |
| `ppdoc:ShoringInstallation` | `ppdoc:FormworkDetailCategory` | 동바리 설치 |
| `ppdoc:ShoringSupportMaterial` | `ppdoc:FormworkDetailCategory` | 동바리 지지재 |

### 5.7 규격 객체 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:Specification` | `ppdoc:DerivedDataRecord` | 구조화된 규격 객체 |
| `ppdoc:ConcreteMix` | `ppdoc:Specification` | 콘크리트 배합 규격 |
| `ppdoc:RebarSpec` | `ppdoc:Specification` | 철근 규격 |
| `ppdoc:SteelShapeSpec` | `ppdoc:Specification` | 형강 규격 |
| `ppdoc:FormworkSpec` | `ppdoc:Specification` | 거푸집 규격 |

### 5.8 수량산출 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:QuantityCalculationItem` | `ppdoc:QuantityCalculationRecord`, `ppdoc:SpecifiableRecord` | 수량산출 항목 |
| `ppdoc:ConcreteQuantityCalculationItem` | `ppdoc:QuantityCalculationItem` | 콘크리트 수량산출 항목 |
| `ppdoc:RebarQuantityCalculationItem` | `ppdoc:QuantityCalculationItem` | 철근 수량산출 항목 |
| `ppdoc:FormworkQuantityCalculationItem` | `ppdoc:QuantityCalculationItem` | 거푸집 및 동바리 수량산출 항목 |

### 5.9 기타 파생 클래스

| Class | 상위 클래스 | 의미 |
| --- | --- | --- |
| `ppdoc:ClassificationMapping` | `ppdoc:DerivedDataRecord` | 원본 행을 공종/세부 분류에 연결한 해석 결과 |
| `ppdoc:BoQItemTableFormat` | `ppdoc:CanonicalDataFormat` | 공종별내역서 표준 행 포맷 |

## 6. Property 구성

현재 모든 property는 `rdf:Property`로 선언되어 있다. RDFS만 사용하는 구조이므로 OWL property 타입을 별도 사용하지 않는다. 이 보고서에서는 range가 `ppdoc:` 클래스인 경우 관계형 property로, range가 `xsd:`인 경우 datatype property로 설명한다.

### 6.1 문서 및 포함 관계 Property

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasPart` | `ppdoc:ProgressPaymentEntity` | `ppdoc:ProgressPaymentEntity` | 상위 개체가 하위 개체를 포함 |
| `ppdoc:isPartOf` | `ppdoc:ProgressPaymentEntity` | `ppdoc:ProgressPaymentEntity` | 하위 개체가 상위 개체에 포함됨 |
| `ppdoc:hasRecord` | `ppdoc:DocumentResource` | `ppdoc:DocumentRecord` | 문서가 원본 행 레코드를 포함 |
| `ppdoc:hasDataFormat` | `ppdoc:DocumentResource` | `ppdoc:CanonicalDataFormat` | 문서가 표준 데이터 포맷을 가짐 |
| `ppdoc:hasWorkTypeSection` | `ppdoc:DocumentResource` | `ppdoc:DocumentWorkTypeSection` | 문서가 공종별 구간을 가짐 |
| `ppdoc:hasSourceDocument` | `ppdoc:ProgressPaymentEntity` | `ppdoc:DocumentResource` | 레코드의 출처 문서 연결 |

### 6.2 원가, 집계, 수량 근거 관계 Property

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasCostItem` | `ppdoc:ProgressPaymentEntity` | `ppdoc:CostItem` | 원가계산 구간이 원가 항목을 포함 |
| `ppdoc:hasCostBasis` | `ppdoc:CostCalculationRecord` | `ppdoc:ProgressPaymentEntity` | 원가 항목의 산정 근거 |
| `ppdoc:aggregatesTo` | `ppdoc:ProgressPaymentEntity` | `ppdoc:SummaryAmount` | 내역 항목 또는 하위 집계가 상위 집계로 합산됨 |
| `ppdoc:aggregates` | `ppdoc:SummaryAmount` | `ppdoc:ProgressPaymentEntity` | 상위 집계가 하위 항목을 집계 |
| `ppdoc:hasQuantityBasis` | `ppdoc:BoQItem` | `ppdoc:QuantityCalculationItem` | 내역 항목의 수량산출 근거 |
| `ppdoc:isQuantityBasisFor` | `ppdoc:QuantityCalculationItem` | `ppdoc:BoQItem` | 수량산출 항목이 내역 항목의 근거가 됨 |

### 6.3 공종, 세부 분류, 규격 관계 Property

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasSubWorkType` | `ppdoc:WorkType` | `ppdoc:WorkType` | 철근콘크리트공사가 하위 공종을 가짐 |
| `ppdoc:hasWorkType` | `ppdoc:ProgressPaymentEntity` | `ppdoc:WorkType` | 레코드 또는 구간이 관련 공종을 가짐 |
| `ppdoc:hasDetailCategory` | `ppdoc:WorkType` | `ppdoc:DetailCategory` | 공종이 세부 작업 분류를 가짐 |
| `ppdoc:hasCategoryItem` | `ppdoc:DetailCategory` | `ppdoc:BoQItem` | 세부 분류가 내역 항목을 포함 |
| `ppdoc:belongsToDetailCategory` | `ppdoc:BoQItem` | `ppdoc:DetailCategory` | 내역 항목이 세부 분류에 속함 |
| `ppdoc:hasClassificationMapping` | `ppdoc:BoQItem` | `ppdoc:ClassificationMapping` | 내역 항목의 분류 판단 근거 |
| `ppdoc:hasSpecificationObject` | `ppdoc:SpecifiableRecord` | `ppdoc:Specification` | 내역 항목 또는 수량산출 항목이 규격 객체를 참조 |
| `ppdoc:hasConcreteMix` | `ppdoc:SpecifiableRecord` | `ppdoc:ConcreteMix` | 콘크리트 배합 규격 참조 |
| `ppdoc:hasRebarSpec` | `ppdoc:SpecifiableRecord` | `ppdoc:RebarSpec` | 철근 규격 참조 |
| `ppdoc:hasSteelShapeSpec` | `ppdoc:SpecifiableRecord` | `ppdoc:SteelShapeSpec` | 형강 규격 참조 |
| `ppdoc:hasFormworkSpec` | `ppdoc:SpecifiableRecord` | `ppdoc:FormworkSpec` | 거푸집 규격 참조 |

`hasConcreteMix`, `hasRebarSpec`, `hasSteelShapeSpec`, `hasFormworkSpec`는 모두 `hasSpecificationObject`의 하위 property로 선언되어 있다.

### 6.4 표준 필드 관계 Property

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasInformationField` | `ppdoc:ProgressPaymentEntity` | `ppdoc:InformationField` | 문서 또는 포맷이 정보 필드를 가짐 |
| `ppdoc:definesField` | `ppdoc:CanonicalDataFormat` | `ppdoc:InformationField` | 표준 데이터 포맷이 필드를 정의 |

`definesField`는 `hasInformationField`의 하위 property이다.

## 7. Datatype Property 구성

### 7.1 문서 메타데이터 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasDocumentTitle` | `ppdoc:DocumentResource` | `xsd:string` | 문서명 |
| `ppdoc:hasDocumentIdentifier` | `ppdoc:DocumentResource` | `xsd:string` | 문서 식별자 |
| `ppdoc:hasProjectName` | `ppdoc:DocumentResource` | `xsd:string` | 공사명 |
| `ppdoc:hasProgressRound` | `ppdoc:DocumentResource` | `xsd:string` | 기성 회차 |
| `ppdoc:hasBaseDate` | `ppdoc:DocumentResource` | `xsd:date` | 기준일 |
| `ppdoc:hasSourceFileName` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 원본 파일명 |
| `ppdoc:hasSourceSheetName` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 원본 시트명 |
| `ppdoc:hasSourceCellAddress` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 원본 셀 주소 |
| `ppdoc:hasSourceRowNumber` | `ppdoc:ProgressPaymentEntity` | `xsd:integer` | 원본 행 번호 |

### 7.2 내역 항목 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasHierarchyPath` | `ppdoc:BoQItem` | `xsd:string` | 원본 계층 경로 |
| `ppdoc:hasItemCode` | `ppdoc:BoQItem` | `xsd:string` | 항목 코드 |
| `ppdoc:hasWorkTypeLabel` | `ppdoc:BoQItem` | `xsd:string` | 원본 공종명 |
| `ppdoc:hasDetailCategoryLabel` | `ppdoc:BoQItem` | `xsd:string` | 원본 세부 분류명 |
| `ppdoc:hasItemName` | `ppdoc:BoQItem` | `xsd:string` | 품명 |
| `ppdoc:hasSpecification` | `ppdoc:BoQItem` | `xsd:string` | 원본 규격 문자열 |
| `ppdoc:hasQuantityUnit` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 단위 |
| `ppdoc:hasContractQuantity` | `ppdoc:BoQItem` | `xsd:decimal` | 계약수량 |
| `ppdoc:hasPreviousQuantity` | `ppdoc:BoQItem` | `xsd:decimal` | 전회수량 |
| `ppdoc:hasCurrentQuantity` | `ppdoc:BoQItem` | `xsd:decimal` | 금회수량 |
| `ppdoc:hasCumulativeQuantity` | `ppdoc:BoQItem` | `xsd:decimal` | 누계수량 |
| `ppdoc:hasUnitPrice` | `ppdoc:BoQItem` | `xsd:decimal` | 단가 |
| `ppdoc:hasMaterialUnitPrice` | `ppdoc:BoQItem` | `xsd:decimal` | 재료비 단가 |
| `ppdoc:hasLaborUnitPrice` | `ppdoc:BoQItem` | `xsd:decimal` | 노무비 단가 |
| `ppdoc:hasExpenseUnitPrice` | `ppdoc:BoQItem` | `xsd:decimal` | 경비 단가 |
| `ppdoc:hasAmount` | `ppdoc:ProgressPaymentEntity` | `xsd:decimal` | 금액 |
| `ppdoc:hasMaterialAmount` | `ppdoc:BoQItem` | `xsd:decimal` | 재료비 금액 |
| `ppdoc:hasLaborAmount` | `ppdoc:BoQItem` | `xsd:decimal` | 노무비 금액 |
| `ppdoc:hasExpenseAmount` | `ppdoc:BoQItem` | `xsd:decimal` | 경비 금액 |
| `ppdoc:hasCurrency` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 통화 |

### 7.3 집계 금액 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasContractAmount` | `ppdoc:SummaryAmount` | `xsd:decimal` | 계약금액 |
| `ppdoc:hasPreviousAmount` | `ppdoc:SummaryAmount` | `xsd:decimal` | 전회 기성 금액 |
| `ppdoc:hasCurrentAmount` | `ppdoc:SummaryAmount` | `xsd:decimal` | 금회 기성 금액 |
| `ppdoc:hasCumulativeAmount` | `ppdoc:SummaryAmount` | `xsd:decimal` | 누계 기성 금액 |
| `ppdoc:hasProgressRate` | `ppdoc:SummaryAmount` | `xsd:decimal` | 기성률 |
| `ppdoc:hasSummaryLevel` | `ppdoc:SummaryAmount` | `xsd:string` | 집계 수준 |

### 7.4 원가 항목 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasCostItemName` | `ppdoc:CostCalculationRecord` | `xsd:string` | 원가 항목명 |
| `ppdoc:hasCostCategory` | `ppdoc:CostCalculationRecord` | `xsd:string` | 원가 항목 분류 |
| `ppdoc:hasCalculationFormula` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 원가 산정식 또는 수량 산출식 |
| `ppdoc:hasRate` | `ppdoc:CostCalculationRecord` | `xsd:decimal` | 요율 |

### 7.5 수량산출 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasTakeoffItemName` | `ppdoc:QuantityCalculationItem` | `xsd:string` | 수량산출 항목명 |
| `ppdoc:hasLocation` | `ppdoc:QuantityCalculationItem` | `xsd:string` | 위치 |
| `ppdoc:hasMemberName` | `ppdoc:QuantityCalculationItem` | `xsd:string` | 부재명 |
| `ppdoc:hasMemberType` | `ppdoc:QuantityCalculationItem` | `xsd:string` | 부재 유형 |
| `ppdoc:hasBasisDescription` | `ppdoc:QuantityCalculationItem` | `xsd:string` | 산출 근거 설명 |
| `ppdoc:hasCalculatedQuantity` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 산출수량 |
| `ppdoc:hasLength` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 길이 |
| `ppdoc:hasWidth` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 폭 |
| `ppdoc:hasHeight` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 높이 |
| `ppdoc:hasCount` | `ppdoc:QuantityCalculationItem` | `xsd:integer` | 개수 |
| `ppdoc:hasUnitWeight` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 단위중량 |
| `ppdoc:hasCalculatedWeight` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 산출중량 |
| `ppdoc:hasCalculatedVolume` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 산출체적 |
| `ppdoc:hasCalculatedArea` | `ppdoc:QuantityCalculationItem` | `xsd:decimal` | 산출면적 |

### 7.6 콘크리트 규격 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasDesignStrength` | `ppdoc:ConcreteMix` | `xsd:decimal` | 설계기준강도 |
| `ppdoc:hasStrengthUnit` | `ppdoc:ConcreteMix` | `xsd:string` | 강도 단위 |
| `ppdoc:hasSlump` | `ppdoc:ConcreteMix` | `xsd:decimal` | 슬럼프 |
| `ppdoc:hasSlumpUnit` | `ppdoc:ConcreteMix` | `xsd:string` | 슬럼프 단위 |
| `ppdoc:hasMaxAggregateSize` | `ppdoc:ConcreteMix` | `xsd:decimal` | 굵은골재 최대치수 |
| `ppdoc:hasAggregateSizeUnit` | `ppdoc:ConcreteMix` | `xsd:string` | 골재치수 단위 |
| `ppdoc:hasMixCode` | `ppdoc:ConcreteMix` | `xsd:string` | 배합 코드 |
| `ppdoc:hasPlacementMethod` | `ppdoc:BoQItem` | `xsd:string` | 타설 방식 |

### 7.7 철근 규격 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasSteelGrade` | `ppdoc:RebarSpec` | `xsd:string` | 철근 강종 또는 강도등급 |
| `ppdoc:hasBarDiameter` | `ppdoc:RebarSpec` | `xsd:string` | 철근 직경 표기 |
| `ppdoc:hasNominalDiameter` | `ppdoc:RebarSpec` | `xsd:decimal` | 공칭 직경 |
| `ppdoc:hasYieldStrength` | `ppdoc:RebarSpec` | `xsd:decimal` | 항복강도 |
| `ppdoc:hasYieldStrengthUnit` | `ppdoc:RebarSpec` | `xsd:string` | 항복강도 단위 |
| `ppdoc:hasBarType` | `ppdoc:RebarSpec` | `xsd:string` | 철근 종류 |
| `ppdoc:hasProcessingType` | `ppdoc:RebarSpec` | `xsd:string` | 가공 방식 |

### 7.8 거푸집 및 동바리 규격 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasSteelShape` | `ppdoc:SteelShapeSpec` | `xsd:string` | 형강 형상 |
| `ppdoc:hasSectionSize` | `ppdoc:SteelShapeSpec` | `xsd:string` | 단면 치수 |
| `ppdoc:hasMaterialGrade` | `ppdoc:Specification` | `xsd:string` | 재질 등급 |
| `ppdoc:hasIntendedUse` | `ppdoc:Specification` | `xsd:string` | 용도 |
| `ppdoc:hasSupportMethod` | `ppdoc:Specification` | `xsd:string` | 지지 방식 |
| `ppdoc:hasFormworkType` | `ppdoc:FormworkSpec` | `xsd:string` | 거푸집 종류 |

### 7.9 정보 필드 속성

| Property | Domain | Range | 의미 |
| --- | --- | --- | --- |
| `ppdoc:hasUnitSymbol` | `ppdoc:ProgressPaymentEntity` | `xsd:string` | 단위 기호 |
| `ppdoc:hasSourceFieldName` | `ppdoc:InformationField` | `xsd:string` | 원본 필드명 |
| `ppdoc:hasCanonicalFieldName` | `ppdoc:InformationField` | `xsd:string` | 표준 필드명 |
| `ppdoc:hasDatatypeHint` | `ppdoc:InformationField` | `xsd:string` | 자료형 힌트 |
| `ppdoc:isRequiredField` | `ppdoc:InformationField` | `xsd:boolean` | 필수 필드 여부 |

## 8. 샘플 인스턴스 구성

`ontology/sample_data.ttl`에는 현재 스키마 구조를 설명하기 위한 예시 인스턴스가 들어 있다. 일부 금액과 기성회차는 구조 확인용 예시값이므로 실제 원본 문서에서 추출한 값으로 교체해야 한다.

### 8.1 문서 인스턴스

| Instance | Type | 의미 |
| --- | --- | --- |
| `ppdoc:progress-payment-documents-sample` | `ppdoc:ProgressPaymentDocumentSet` | 기성서류 샘플 |
| `ppdoc:rc-progress-payment-documents-sample` | `ppdoc:ReinforcedConcreteProgressPaymentDocuments` | 철근콘크리트 공종 기성서류 샘플 |
| `ppdoc:statement-document-sample` | `ppdoc:StatementDocument` | 내역서 문서군 샘플 |
| `ppdoc:progress-payment-statement-sample` | `ppdoc:ProgressPaymentStatement` | 공사기성부분 내역서 샘플 |
| `ppdoc:cost-calculation-sheet-sample` | `ppdoc:CostCalculationSheet` | 원가계산서 샘플 |
| `ppdoc:work-type-summary-sheet-sample` | `ppdoc:WorkTypeSummarySheet` | 공종별집계표 샘플 |
| `ppdoc:work-type-detail-sheet-sample` | `ppdoc:WorkTypeDetailSheet` | 공종별내역서 샘플 |
| `ppdoc:quantity-calculation-sheet-sample` | `ppdoc:QuantityCalculationSheet` | 수량산출서 샘플 |

### 8.2 원가 항목 인스턴스

| Instance | Type | 의미 |
| --- | --- | --- |
| `ppdoc:cost-section-rc-work` | `ppdoc:CostWorkTypeSection` | 철근콘크리트공사 원가계산 구간 |
| `ppdoc:cost-rc-direct-cost` | `ppdoc:DirectCostItem` | 직접공사비 |
| `ppdoc:cost-rc-indirect-cost` | `ppdoc:IndirectCostItem` | 간접비 및 법정경비 |
| `ppdoc:cost-rc-markup-cost` | `ppdoc:MarkupCostItem` | 일반관리비 및 이윤 |
| `ppdoc:cost-rc-tax-total-cost` | `ppdoc:TaxAndTotalCostItem` | 세금 및 총액 |

### 8.3 공종 및 구간 인스턴스

| Instance | Type | 의미 |
| --- | --- | --- |
| `ppdoc:worktype-rc` | `ppdoc:ReinforcedConcreteWork` | 철근콘크리트공사 |
| `ppdoc:worktype-concrete` | `ppdoc:ConcreteWork` | 콘크리트공사 |
| `ppdoc:worktype-rebar` | `ppdoc:RebarWork` | 철근공사 |
| `ppdoc:worktype-formwork-shoring` | `ppdoc:FormworkAndShoringWork` | 거푸집 및 동바리공사 |
| `ppdoc:summary-section-concrete-work` | `ppdoc:SummaryWorkTypeSection` | 콘크리트공사 집계 구간 |
| `ppdoc:summary-section-rebar-work` | `ppdoc:SummaryWorkTypeSection` | 철근공사 집계 구간 |
| `ppdoc:summary-section-formwork-shoring-work` | `ppdoc:SummaryWorkTypeSection` | 거푸집 및 동바리공사 집계 구간 |
| `ppdoc:detail-section-concrete-work` | `ppdoc:DetailWorkTypeSection` | 콘크리트공사 내역 구간 |
| `ppdoc:detail-section-rebar-work` | `ppdoc:DetailWorkTypeSection` | 철근공사 내역 구간 |
| `ppdoc:detail-section-formwork-shoring-work` | `ppdoc:DetailWorkTypeSection` | 거푸집 및 동바리공사 내역 구간 |
| `ppdoc:quantity-section-concrete-work` | `ppdoc:QuantityWorkTypeSection` | 콘크리트공사 수량산출 구간 |
| `ppdoc:quantity-section-rebar-work` | `ppdoc:QuantityWorkTypeSection` | 철근공사 수량산출 구간 |
| `ppdoc:quantity-section-formwork-shoring-work` | `ppdoc:QuantityWorkTypeSection` | 거푸집 및 동바리공사 수량산출 구간 |

### 8.4 집계 금액 인스턴스

| Instance | Type | 의미 |
| --- | --- | --- |
| `ppdoc:summary-rc-work-sample` | `ppdoc:SummaryAmount` | 철근콘크리트공사 집계금액 |
| `ppdoc:summary-concrete-work-sample` | `ppdoc:SummaryAmount` | 콘크리트공사 집계금액 |
| `ppdoc:summary-rebar-work-sample` | `ppdoc:SummaryAmount` | 철근공사 집계금액 |
| `ppdoc:summary-formwork-shoring-work-sample` | `ppdoc:SummaryAmount` | 거푸집 및 동바리공사 집계금액 |

### 8.5 규격 객체 인스턴스

| Instance | Type | 주요 속성 |
| --- | --- | --- |
| `ppdoc:concrete-mix-25-24-150` | `ppdoc:ConcreteMix` | `hasMixCode`, `hasMaxAggregateSize`, `hasDesignStrength`, `hasSlump` |
| `ppdoc:rebar-spec-sd400-hd13` | `ppdoc:RebarSpec` | `hasSteelGrade`, `hasBarDiameter`, `hasNominalDiameter`, `hasYieldStrength` |
| `ppdoc:formwork-spec-euroform` | `ppdoc:FormworkSpec` | `hasFormworkType`, `hasMaterialGrade` |
| `ppdoc:steel-shape-spec-h200` | `ppdoc:SteelShapeSpec` | `hasSteelShape`, `hasSectionSize`, `hasMaterialGrade`, `hasSupportMethod` |

### 8.6 내역 항목 인스턴스

| Instance | Type | 공종 | 규격 참조 |
| --- | --- | --- | --- |
| `ppdoc:boq-concrete-ready-mix-001` | `ppdoc:BoQItem` | 콘크리트공사 | `ppdoc:concrete-mix-25-24-150` |
| `ppdoc:boq-concrete-placement-001` | `ppdoc:BoQItem` | 콘크리트공사 | `ppdoc:concrete-mix-25-24-150` |
| `ppdoc:boq-rebar-material-001` | `ppdoc:BoQItem` | 철근공사 | `ppdoc:rebar-spec-sd400-hd13` |
| `ppdoc:boq-rebar-assembly-001` | `ppdoc:BoQItem` | 철근공사 | `ppdoc:rebar-spec-sd400-hd13` |
| `ppdoc:boq-formwork-installation-001` | `ppdoc:BoQItem` | 거푸집 및 동바리공사 | `ppdoc:formwork-spec-euroform` |
| `ppdoc:boq-shoring-support-001` | `ppdoc:BoQItem` | 거푸집 및 동바리공사 | `ppdoc:steel-shape-spec-h200` |

### 8.7 수량산출 항목 인스턴스

| Instance | Type | 연결되는 내역 항목 |
| --- | --- | --- |
| `ppdoc:quantity-concrete-slab-001` | `ppdoc:ConcreteQuantityCalculationItem` | `boq-concrete-ready-mix-001`, `boq-concrete-placement-001` |
| `ppdoc:quantity-rebar-beam-001` | `ppdoc:RebarQuantityCalculationItem` | `boq-rebar-material-001`, `boq-rebar-assembly-001` |
| `ppdoc:quantity-formwork-wall-001` | `ppdoc:FormworkQuantityCalculationItem` | `boq-formwork-installation-001` |
| `ppdoc:quantity-shoring-support-001` | `ppdoc:FormworkQuantityCalculationItem` | `boq-shoring-support-001` |

## 9. 주요 RDF 연결 패턴

### 9.1 문서 계층 연결

```turtle
ppdoc:progress-payment-documents-sample
    ppdoc:hasPart ppdoc:rc-progress-payment-documents-sample .

ppdoc:rc-progress-payment-documents-sample
    ppdoc:hasPart ppdoc:statement-document-sample .

ppdoc:statement-document-sample
    ppdoc:hasPart ppdoc:progress-payment-statement-sample .

ppdoc:progress-payment-statement-sample
    ppdoc:hasPart ppdoc:cost-calculation-sheet-sample ,
        ppdoc:work-type-summary-sheet-sample ,
        ppdoc:work-type-detail-sheet-sample ,
        ppdoc:quantity-calculation-sheet-sample .
```

### 9.2 원가계산서 연결

```turtle
ppdoc:cost-calculation-sheet-sample
    ppdoc:hasWorkTypeSection ppdoc:cost-section-rc-work .

ppdoc:cost-section-rc-work
    ppdoc:hasWorkType ppdoc:worktype-rc ;
    ppdoc:hasCostItem ppdoc:cost-rc-direct-cost ,
        ppdoc:cost-rc-indirect-cost ,
        ppdoc:cost-rc-markup-cost ,
        ppdoc:cost-rc-tax-total-cost .
```

### 9.3 공종별내역서 연결

```turtle
ppdoc:work-type-detail-sheet-sample
    ppdoc:hasDataFormat ppdoc:boq-item-table-format-sample ;
    ppdoc:hasWorkTypeSection ppdoc:detail-section-concrete-work ,
        ppdoc:detail-section-rebar-work ,
        ppdoc:detail-section-formwork-shoring-work ;
    ppdoc:hasBoQItem ppdoc:boq-concrete-ready-mix-001 ,
        ppdoc:boq-rebar-material-001 ,
        ppdoc:boq-formwork-installation-001 .
```

### 9.4 규격 객체 연결

```turtle
ppdoc:boq-rebar-material-001
    a ppdoc:BoQItem ;
    ppdoc:hasSpecification "SD400, HD13" ;
    ppdoc:hasRebarSpec ppdoc:rebar-spec-sd400-hd13 .

ppdoc:quantity-rebar-beam-001
    a ppdoc:RebarQuantityCalculationItem ;
    ppdoc:hasRebarSpec ppdoc:rebar-spec-sd400-hd13 ;
    ppdoc:isQuantityBasisFor ppdoc:boq-rebar-material-001 .
```

이 구조에서 같은 `RebarSpec` 객체가 공종별내역서의 내역 항목과 수량산출서의 산출 항목에 동시에 연결된다.

## 10. 속성값 배치 기준

속성값은 아무 노드에나 붙이지 않고 아래 기준으로 분리한다.

| 대상 | 붙이는 속성 |
| --- | --- |
| 문서 노드 | 공사명, 기성회차, 문서명, 기준일, 원본 파일명, 원본 시트명 |
| 원가 항목 | 원가 항목명, 원가 분류, 금액, 요율, 산정식, 산정 근거 |
| 집계 항목 | 공종, 계약금액, 전회금액, 금회금액, 누계금액, 기성률, 집계 수준 |
| 내역 항목 | 품명, 규격 문자열, 단위, 계약수량, 전회수량, 금회수량, 누계수량, 단가, 금액, 비목별 단가·금액 |
| 수량산출 항목 | 산출 항목명, 위치, 부재명, 부재유형, 산출식, 산출수량, 산출체적·면적·중량, 산출 근거 설명 |
| 규격 객체 | 콘크리트 강도·슬럼프·골재치수, 철근 강종·직경·항복강도, 거푸집 종류, 형강 형상·치수·재질 |

따라서 `SD400`, `HD13`, `25-24-150`, `유로폼`은 그래프 말단 노드가 아니라 각각 `RebarSpec`, `ConcreteMix`, `FormworkSpec`의 속성값으로 들어간다.

## 11. 시각화 반영 내용

시각화 파일은 `visualization/ontology_graph.html`이다. 현재 시각화는 문서·공종 구간 중심으로 22개 노드를 표시한다.

### 11.1 표시되는 노드

```text
기성서류
철근콘크리트 공종 기성서류
내역서
공사기성부분 내역서
원가계산서
공종별집계표
공종별내역서
수량산출서
철근콘크리트공사 원가계산
직접공사비
간접비 및 법정경비
일반관리비 및 이윤
세금 및 총액
콘크리트공사 집계
철근공사 집계
거푸집 및 동바리공사 집계
콘크리트공사 내역
철근공사 내역
거푸집 및 동바리공사 내역
콘크리트공사 수량산출
철근공사 수량산출
거푸집 및 동바리공사 수량산출
```

### 11.2 표시되는 관계

| 관계 | 의미 |
| --- | --- |
| `hasPart` | 상위 문서나 문서군이 하위 문서를 포함 |
| `hasWorkTypeSection` | 문서가 공종별 구간을 포함 |
| `hasCostItem` | 철근콘크리트공사 원가계산 구간이 원가 항목을 포함 |

시각화 관계명은 RDF/RDFS property 이름과 맞추기 위해 영어 local name으로 유지했다.

### 11.3 클릭형 속성 패널

각 노드를 클릭하면 오른쪽 패널에 아래 정보가 표시된다.

- 라벨
- RDF/RDFS 식별자
- 노드 유형
- 설명
- 속성 정보
- 나가는 관계
- 들어오는 관계

속성 정보에는 실제 값이 아니라 해당 노드 또는 레코드가 가져야 하는 속성 체계가 표시된다. 예를 들어 `철근공사 내역`을 클릭하면 `hasItemName`, `hasSpecification`, `hasCurrentQuantity`, `hasUnitPrice`, `hasAmount`와 함께 `RebarSpec / hasSteelGrade`, `RebarSpec / hasBarDiameter` 같은 규격 속성이 표시된다.

## 12. RDF/RDFS 모델링 판단

### 12.1 RDFS로 표현한 이유

현재 단계는 실험 비교를 위한 RDF/RDFS 기반 구축 단계이다. 따라서 OWL 2 DL의 제약, 추론 규칙, cardinality, disjointness, equivalentClass 등을 아직 넣지 않았다. 대신 RDFS의 기본 구조만으로 다음을 표현했다.

- `rdfs:Class`로 개념 정의
- `rdfs:subClassOf`로 클래스 계층 정의
- `rdf:Property`로 관계 및 속성 정의
- `rdfs:domain`으로 property가 적용되는 주체 범위 정의
- `rdfs:range`로 property의 대상 또는 값 자료형 정의
- `rdfs:subPropertyOf`로 상세 property가 상위 property에 속함을 표현
- `rdfs:label`, `rdfs:comment`로 사람이 읽을 수 있는 설명 제공

### 12.2 RDFS의 한계

현재 구조는 RDFS이므로 아래 내용을 엄격하게 검증하지는 못한다.

- 한 `BoQItem`이 반드시 하나 이상의 `Specification`을 가져야 한다는 제약
- `ConcreteMix`에는 반드시 강도와 슬럼프가 있어야 한다는 제약
- `RebarSpec`의 강종이 허용 목록 중 하나여야 한다는 제약
- `BoQItem`의 금액이 수량 x 단가와 일치해야 한다는 제약
- 콘크리트 규격과 철근 규격을 서로 배타적으로 구분하는 제약

이러한 제약은 이후 OWL 2 DL 또는 SHACL 단계에서 추가할 수 있다.

## 13. 향후 OWL 2 DL 확장 후보

현재 RDFS 구조를 OWL 2 DL로 확장할 경우 다음 요소를 추가할 수 있다.

| 확장 후보 | 적용 예 |
| --- | --- |
| `owl:ObjectProperty` | `hasConcreteMix`, `hasRebarSpec`, `hasQuantityBasis` |
| `owl:DatatypeProperty` | `hasDesignStrength`, `hasBarDiameter`, `hasCurrentQuantity` |
| `owl:Restriction` | `BoQItem`은 최소 1개의 `hasSpecificationObject`를 가짐 |
| `owl:disjointWith` | `ConcreteMix`, `RebarSpec`, `FormworkSpec`의 상호 배타성 |
| cardinality | 하나의 `SummaryAmount`는 하나의 `WorkType`에 대응 |
| controlled vocabulary | `steelGrade` 값 후보를 SD300, SD400, SD500 등으로 제한 |

다만 현재 버전에서는 RDF/RDFS 실험 비교를 위해 이러한 OWL 제약을 의도적으로 넣지 않았다.

## 14. 검증 결과

작성 후 현재 환경에서 확인한 내용은 다음과 같다.

| 검사 | 결과 |
| --- | --- |
| TTL 문장 종료 및 따옴표 정적 검사 | 통과 |
| HTML 그래프 노드 참조 검사 | 노드 22개, 링크 21개, 누락 참조 없음 |
| HTML 관계 메타데이터 검사 | 누락 relation metadata 없음 |
| JavaScript 구문 검사 | 통과 |
| RDFLib Turtle 파싱 | `rdflib` 미설치로 미수행 |

`rdflib`가 설치되면 아래 방식으로 Turtle 파싱 검사를 추가할 수 있다.

```bash
python3 - <<'PY'
import rdflib
for path in ["ontology/ontology.ttl", "ontology/sample_data.ttl"]:
    graph = rdflib.Graph()
    graph.parse(path, format="turtle")
    print(path, len(graph))
PY
```

## 15. 현재 버전의 결론

현재 RDF/RDFS 버전은 문서 계층과 공종 구간을 시각적으로 명확히 보여주고, 정형 서류 포맷은 `BoQItemTableFormat`과 `InformationField`로 보존한다. 내역 항목, 수량산출 항목, 규격 객체를 분리했기 때문에 공종 분개가 지나치게 깊어지는 문제를 피했다.

가장 중요한 구조는 아래와 같다.

```text
공종별내역서의 내역 항목
  -> BoQItem
  -> 수량, 단가, 금액, 비목별 금액
  -> hasSpecificationObject
  -> ConcreteMix / RebarSpec / FormworkSpec / SteelShapeSpec
  -> hasQuantityBasis
  -> QuantityCalculationItem
  -> aggregatesTo
  -> SummaryAmount
```

즉, 그래프의 분개는 문서와 공종 구간까지만 보여주고, 연구에서 필요한 세부값은 RDF 속성 및 클릭형 상세 패널에서 관리하는 구조이다.
