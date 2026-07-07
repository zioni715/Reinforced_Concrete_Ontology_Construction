# 공사기성부분 내역서 데이터 정의서

## 1. 정의 원칙

이 온톨로지는 철근콘크리트 공종의 전체 기성서류가 아니라 `공사기성부분 내역서`를 우선 대상으로 한다. 분개는 원본 서류 데이터를 정의한 뒤 수행한다.

- `BoQItem`은 RDF 내부 클래스명이며, 화면과 설명에서는 공종별내역서의 원본 행 레코드를 `내역 항목`으로 표시한다.
- 공종, 세부 분류, 규격 객체는 원본 행에서 파생되는 해석 결과이다.
- 콘크리트 강도, 철근 직경, 형강 형상, 거푸집 종류는 독립 작업 분류가 아니라 규격 필드 또는 규격 객체이다.
- 분류가 불확실해도 원본 행 레코드는 유지한다.

업로드한 `BIM과 온톨로지를 활용한 표준내역항목 추론 자동화` 논문 기준으로 보면 내역서 작성 정보는 `내역항목`, `물량정보`, `단가정보`로 나뉘며, `내역항목`은 다시 `품명`과 `규격`으로 구성된다. 따라서 이 온톨로지의 분개 계층은 문서 계층과 공종 계층을 먼저 세우고, 강도·직경·유로폼 같은 값은 공종 하위분류가 아니라 내역 항목 또는 규격 객체의 속성으로 둔다.

## 2. 분개 계층

기본 분개 계층은 다음 순서로 둔다.

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

위 구조가 1차 분개이다. 이후 단계에서 공종, 표준 포맷, 규격 속성을 붙이더라도 이 문서 계층은 유지한다.

## 3. 2차 공종 분개 기준

`Documents/화성동탄(2)A4-1BL아파트신축공사/3. 기성 세부내역.xlsx` 확인 기준으로 2차 분개는 4개 하위 문서 전체에 동일한 방식으로 적용하지 않는다. 용어 분포상 `3-1.건축내역서`에는 콘크리트, 철근, 거푸집, 동바리 항목이 반복적으로 등장하지만, 원가계산서는 총괄 원가 산정 문서 성격이 강하다. 따라서 원가계산서는 콘크리트공사, 철근공사, 거푸집 및 동바리공사로 직접 쪼개지 않고, 철근콘크리트공사에 배부되는 원가 항목 구조만 따로 분개한다.

| 하위 문서 | 2차 분개 | 기준 |
| --- | --- | --- |
| 원가계산서 | 제한 적용 | 콘크리트공사, 철근공사, 거푸집 및 동바리공사로 직접 분개하지 않고, 철근콘크리트공사에 배부되는 직접공사비, 간접비/법정경비, 일반관리비/이윤, 세금/총액 항목만 둔다. |
| 공종별집계표 | 적용 | 공종별 금액을 요약하는 문서이므로 콘크리트공사, 철근공사, 거푸집 및 동바리공사 집계 구간을 둔다. |
| 공종별내역서 | 적용 | 실제 내역 항목 행이 공종별로 배열되는 문서이므로 콘크리트공사, 철근공사, 거푸집 및 동바리공사 내역 구간을 둔다. |
| 수량산출서 | 적용 | 내역 항목 수량의 산출 근거가 공종별로 대응되므로 콘크리트공사, 철근공사, 거푸집 및 동바리공사 수량산출 구간을 둔다. |

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

## 4. 규격 속성 처리 기준

규격은 추가 분개 계층으로 만들지 않는다. `콘크리트 강도`, `철근 직경`, `거푸집 종류`, `동바리 형강 형상` 같은 항목은 작업 종류가 아니라 내역 항목 또는 규격 객체의 속성이다. 또한 현재 시각화는 공종별내역서의 원본 행 전체를 펼쳐 보여주는 화면이 아니므로, 말단을 `레미콘`, `철근 재료`, `거푸집 설치` 같은 품명 예시로 고정하지 않는다.

```text
공종별내역서
  ├─ 콘크리트공사 내역 구간
  │   └─ 클릭 시 표시: designStrength, slump, maxAggregateSize, placementMethod
  ├─ 철근공사 내역 구간
  │   └─ 클릭 시 표시: steelGrade, yieldStrength, barDiameter, barType, processingType
  └─ 거푸집 및 동바리공사 내역 구간
      └─ 클릭 시 표시: formworkType, steelShape, sectionSize, materialGrade, supportMethod
```

이 처리는 정형 포맷을 바꾸지 않는다. `공종별내역서`의 원본 행은 계속 `품명`, `규격`, `단위`, `수량`, `단가`, `금액` 필드를 가지며, `레미콘`, `콘크리트 타설`, `철근 재료`, `거푸집 설치` 같은 값은 실제 원본 행이 들어왔을 때 `품명` 또는 세부 해석 결과로 다룬다. 규격 속성은 원본 `규격` 문자열을 구조화한 결과로 별도 규격 객체에 저장한다.

노드별 속성값의 위치는 아래처럼 고정한다.

| 노드/레코드 | 속성 중심 | RDF 속성 예시 |
| --- | --- | --- |
| 문서 노드 | 문서명, 공사명, 기성회차, 기준일, 파일명, 시트명 | `ppdoc:hasDocumentTitle`, `ppdoc:hasProjectName`, `ppdoc:hasProgressRound`, `ppdoc:hasBaseDate`, `ppdoc:hasSourceFileName`, `ppdoc:hasSourceSheetName` |
| 원가 항목 | 원가 항목명, 분류, 금액, 요율, 산정식, 산정 근거 | `ppdoc:hasCostItemName`, `ppdoc:hasCostCategory`, `ppdoc:hasAmount`, `ppdoc:hasRate`, `ppdoc:hasCalculationFormula`, `ppdoc:hasCostBasis` |
| 집계 항목 | 공종명, 계약금액, 전회금액, 금회금액, 누계금액, 기성률 | `ppdoc:hasWorkType`, `ppdoc:hasContractAmount`, `ppdoc:hasPreviousAmount`, `ppdoc:hasCurrentAmount`, `ppdoc:hasCumulativeAmount`, `ppdoc:hasProgressRate` |
| 내역 항목 | 품명, 규격 문자열, 단위, 수량, 단가, 금액, 비목별 단가/금액 | `ppdoc:hasItemName`, `ppdoc:hasSpecification`, `ppdoc:hasQuantityUnit`, `ppdoc:hasCurrentQuantity`, `ppdoc:hasUnitPrice`, `ppdoc:hasAmount`, `ppdoc:hasMaterialAmount` |
| 수량산출 항목 | 산출 위치, 부재, 산출식, 산출수량, 단위, 산출 근거 설명 | `ppdoc:hasLocation`, `ppdoc:hasMemberName`, `ppdoc:hasMemberType`, `ppdoc:hasCalculationFormula`, `ppdoc:hasCalculatedQuantity`, `ppdoc:hasBasisDescription` |
| 규격 객체 | 강도, 슬럼프, 골재치수, 강종, 직경, 거푸집 종류, 형강 치수 | `ppdoc:hasDesignStrength`, `ppdoc:hasSlump`, `ppdoc:hasMaxAggregateSize`, `ppdoc:hasSteelGrade`, `ppdoc:hasBarDiameter`, `ppdoc:hasFormworkType` |

## 5. 표준 포맷층과 분개층

정형화된 포맷은 분개 계층과 분리해서 유지한다.

| 층 | 역할 | 예시 |
| --- | --- | --- |
| 표준 포맷층 | 원본 서류를 항상 같은 필드 구조로 저장 | `BoQItemTableFormat`, `InformationField` |
| 원본 레코드층 | 표준 포맷에 맞춰 추출된 실제 행 | `BoQItem`, `QuantityCalculationItem`, `SummaryAmount` |
| 분개/추론층 | 원본 행에 붙는 해석 결과 | `WorkType`, `DetailCategory`, `Specification` |

따라서 `공종별내역서`는 반드시 `BoQItemTableFormat`을 가진다. 이 포맷은 최소한 `품명`, `규격`, `단위`, `계약수량`, `전회수량`, `금회수량`, `누계수량`, `단가`, `금액`, `통화` 필드를 정의한다. 공종 분개와 규격 속성은 이 표준 행 포맷을 바꾸지 않고 내역 항목과 규격 객체에 추가 관계로 연결한다. 수량산출서에 같은 규격 단서가 있으면 수량산출 항목도 같은 규격 객체를 참조한다.

```text
공종별내역서
  ├─ 표준 행 포맷
  │   ├─ 품명
  │   ├─ 규격
  │   ├─ 단위
  │   ├─ 수량
  │   ├─ 단가
  │   └─ 금액
  └─ 내역 항목 원본 행
      ├─ 공종/세부 분류 해석
      ├─ 규격 객체/속성 해석
      ├─ 수량산출 근거
      └─ 집계금액 연결
```

## 6. 처리 순서

1. 문서군과 하위 시트를 식별한다.
2. 각 시트의 레코드 타입을 정의한다.
3. 각 레코드 타입의 필드를 정의한다.
4. 원본 행을 RDF 인스턴스로 만든다.
5. 규격 문자열을 구조화된 규격 객체로 파싱한다.
6. 공종과 세부 분류를 매핑한다.
7. 수량산출서의 산출 항목과 연결한다.
8. 공종별집계표의 금액과 집계 검증을 수행한다.

## 7. 문서 단위

| 서류 단위 | RDF 클래스 | 역할 |
| --- | --- | --- |
| 기성서류 | `ppdoc:ProgressPaymentDocumentSet` | 기성 청구, 검사, 산정, 증빙 서류의 최상위 문서군 |
| 철근콘크리트 공종 기성서류 | `ppdoc:ReinforcedConcreteProgressPaymentDocuments` | 철근콘크리트 공종에 한정한 기성서류 묶음 |
| 내역서 | `ppdoc:StatementDocument` | 공사기성부분 내역서를 포함하는 내역서 문서군 |
| 공사기성부분 내역서 | `ppdoc:ProgressPaymentStatement` | 원가계산서, 공종별집계표, 공종별내역서, 수량산출서를 묶는 문서군 |
| 원가계산서 | `ppdoc:CostCalculationSheet` | 총공사비, 기성 금액, 공제 및 청구 금액을 계산하는 시트 |
| 공종별집계표 | `ppdoc:WorkTypeSummarySheet` | 철근콘크리트공사와 하위 공종별 금액을 집계하는 시트 |
| 공종별내역서 | `ppdoc:WorkTypeDetailSheet` | 품명, 규격, 수량, 단가, 금액을 가진 원본 내역 행의 시트 |
| 수량산출서 | `ppdoc:QuantityCalculationSheet` | 공종별내역서 수량의 산출 근거를 제공하는 시트 |

## 8. 레코드 타입

| 레코드 타입 | RDF 클래스 | 기준 |
| --- | --- | --- |
| 원가계산 행 | `ppdoc:CostCalculationRecord` | 원가계산서의 금액 계산 행 |
| 공종 집계 행 | `ppdoc:WorkTypeSummaryRecord` | 공종별집계표의 공종별 금액 행 |
| 내역 행 | `ppdoc:BoQItem` | 공종별내역서의 품명/규격/수량/단가/금액 행 |
| 수량산출 행 | `ppdoc:QuantityCalculationItem` | 수량산출서의 위치/부재/치수/산출량 행 |
| 규격 객체 | `ppdoc:Specification` | 내역 행의 규격 문자열 또는 수량산출 행의 규격 단서에서 파생된 구조화 객체 |
| 분류 매핑 | `ppdoc:ClassificationMapping` | 내역 행을 공종과 세부 분류에 연결한 해석 결과 |

## 9. 공종별내역서 필드 정의

내역 항목(`BoQItem`)은 아래 필드를 가진 원본 행 레코드로 본다.

| 원본 필드 | 표준 필드 | RDF 속성 | 자료형 | 필수 | 비고 |
| --- | --- | --- | --- | --- | --- |
| 파일명 | source_file | `ppdoc:hasSourceFileName` | string | 권장 | 원본 추적용 |
| 시트명 | source_sheet | `ppdoc:hasSourceSheetName` | string | 권장 | 원본 추적용 |
| 행 번호 | source_row_number | `ppdoc:hasSourceRowNumber` | integer | 권장 | 원본 추적용 |
| 셀 범위 | source_cell_address | `ppdoc:hasSourceCellAddress` | string | 선택 | 예: A120:I120 |
| 상위 목차/헤딩 | hierarchy_path | `ppdoc:hasHierarchyPath` | string | 권장 | 공종 분류의 근거 |
| 품명 | item_name | `ppdoc:hasItemName` | string | 필수 | 원본 품명 |
| 규격 | specification_text | `ppdoc:hasSpecification` | string | 필수 | 원본 규격 문자열 |
| 단위 | quantity_unit | `ppdoc:hasQuantityUnit` | string | 필수 | m3, m2, ton 등 |
| 계약수량 | contract_quantity | `ppdoc:hasContractQuantity` | decimal | 선택 | 계약 기준 수량 |
| 전회수량 | previous_quantity | `ppdoc:hasPreviousQuantity` | decimal | 선택 | 이전 기성 누계 또는 전회 |
| 금회수량 | current_quantity | `ppdoc:hasCurrentQuantity` | decimal | 필수 | 이번 기성 수량 |
| 누계수량 | cumulative_quantity | `ppdoc:hasCumulativeQuantity` | decimal | 선택 | 누계 기성 수량 |
| 단가 | unit_price | `ppdoc:hasUnitPrice` | decimal | 선택 | 금액 검증에 사용 |
| 재료비 단가 | material_unit_price | `ppdoc:hasMaterialUnitPrice` | decimal | 선택 | 비목별 단가 |
| 노무비 단가 | labor_unit_price | `ppdoc:hasLaborUnitPrice` | decimal | 선택 | 비목별 단가 |
| 경비 단가 | expense_unit_price | `ppdoc:hasExpenseUnitPrice` | decimal | 선택 | 비목별 단가 |
| 금액 | amount | `ppdoc:hasAmount` | decimal | 필수 | 금회 또는 해당 행 금액 |
| 재료비 금액 | material_amount | `ppdoc:hasMaterialAmount` | decimal | 선택 | 비목별 금액 |
| 노무비 금액 | labor_amount | `ppdoc:hasLaborAmount` | decimal | 선택 | 비목별 금액 |
| 경비 금액 | expense_amount | `ppdoc:hasExpenseAmount` | decimal | 선택 | 비목별 금액 |
| 통화 | currency | `ppdoc:hasCurrency` | string | 권장 | 기본값 KRW |

## 10. 수량산출서 필드 정의

수량산출서는 규격 속성의 유일한 소유자가 아니라 수량 산출 근거 문서이다. 다만 산출 행이 강도, 직경, 형상 같은 규격 단서를 포함하거나 해당 규격 기준으로 수량을 산출한다면, `QuantityCalculationItem`도 내역 항목과 같은 규격 객체를 참조한다.

| 원본 필드 | 표준 필드 | RDF 속성 | 자료형 | 비고 |
| --- | --- | --- | --- | --- |
| 산출 항목명 | takeoff_item_name | `ppdoc:hasTakeoffItemName` | string | 산출 행 식별명 |
| 위치 | location | `ppdoc:hasLocation` | string | 동, 층, 구간 등 |
| 부재명 | member_name | `ppdoc:hasMemberName` | string | 보, 슬래브, 벽체 등 |
| 부재 유형 | member_type | `ppdoc:hasMemberType` | string | 보, 슬래브, 벽체, 기둥 등 |
| 길이 | length | `ppdoc:hasLength` | decimal | 산출식 구성값 |
| 폭 | width | `ppdoc:hasWidth` | decimal | 산출식 구성값 |
| 높이 | height | `ppdoc:hasHeight` | decimal | 산출식 구성값 |
| 개수 | count | `ppdoc:hasCount` | integer | 반복 수량 |
| 단위중량 | unit_weight | `ppdoc:hasUnitWeight` | decimal | 철근/형강 산출 |
| 산출식 | calculation_formula | `ppdoc:hasCalculationFormula` | string | 원본 산출식 또는 해석식 |
| 산출수량 | calculated_quantity | `ppdoc:hasCalculatedQuantity` | decimal | 산출 결과의 일반 수량값 |
| 산출중량 | calculated_weight | `ppdoc:hasCalculatedWeight` | decimal | kg 또는 ton |
| 산출체적 | calculated_volume | `ppdoc:hasCalculatedVolume` | decimal | m3 |
| 산출면적 | calculated_area | `ppdoc:hasCalculatedArea` | decimal | m2 |
| 단위 | quantity_unit | `ppdoc:hasQuantityUnit` | string | 산출 결과 단위 |
| 산출 근거 설명 | basis_description | `ppdoc:hasBasisDescription` | string | 내역 항목 수량과 연결되는 근거 |

## 11. 규격 파싱 정의

규격 파싱은 내역 항목의 원본 규격 문자열과 수량산출 항목의 규격 단서를 모두 참고해 수행한다. 파싱 결과는 별도 `Specification` 객체로 두고, 내역 항목과 수량산출 항목이 같은 객체를 참조한다.

| 원본 예시 | 파생 객체 | 파싱 필드 |
| --- | --- | --- |
| 25-24-150 | `ppdoc:ConcreteMix` | 배합코드, 굵은골재 최대치수, 설계기준강도, 슬럼프 |
| SD400, HD13 | `ppdoc:RebarSpec` | 강종, 직경 표기, 공칭 직경, 철근 종류 |
| 유로폼 | `ppdoc:FormworkSpec` | 거푸집 종류 |
| H-200x200x8x12 | `ppdoc:SteelShapeSpec` | 형강 형상, 단면 치수, 재질, 용도 |

## 12. 공종별 규격 속성

논문에서 타일공사의 `타일크기`, `타일두께`, `타일유형`, `붙임공법` 등을 표준내역항목 구성 요소로 둔 것처럼, 철근콘크리트 공종에서는 아래 요소를 규격 속성으로 둔다.

| 공종 | 규격 객체/속성 | 예시 값 |
| --- | --- | --- |
| 콘크리트공사 | `ppdoc:ConcreteMix / ppdoc:hasDesignStrength` | 24 MPa |
| 콘크리트공사 | `ppdoc:ConcreteMix / ppdoc:hasSlump` | 150 mm |
| 콘크리트공사 | `ppdoc:ConcreteMix / ppdoc:hasMaxAggregateSize` | 25 mm |
| 콘크리트공사 | `ppdoc:BoQItem / ppdoc:hasPlacementMethod` | 펌프카 |
| 철근공사 | `ppdoc:RebarSpec / ppdoc:hasBarDiameter` | HD13 |
| 철근공사 | `ppdoc:RebarSpec / ppdoc:hasSteelGrade` | SD400 |
| 철근공사 | `ppdoc:RebarSpec / ppdoc:hasYieldStrength` | 400 MPa |
| 철근공사 | `ppdoc:RebarSpec / ppdoc:hasBarType` | 이형철근 |
| 철근공사 | `ppdoc:RebarSpec / ppdoc:hasProcessingType` | 현장가공 |
| 거푸집 및 동바리공사 | `ppdoc:FormworkSpec / ppdoc:hasFormworkType` | 유로폼 |
| 거푸집 및 동바리공사 | `ppdoc:FormworkSpec / ppdoc:hasMaterialGrade` | 합판 및 강재 프레임 |
| 거푸집 및 동바리공사 | `ppdoc:SteelShapeSpec / ppdoc:hasSteelShape` | H형 |
| 거푸집 및 동바리공사 | `ppdoc:SteelShapeSpec / ppdoc:hasSectionSize` | H-200x200x8x12 |
| 거푸집 및 동바리공사 | `ppdoc:SteelShapeSpec / ppdoc:hasSupportMethod` | 형강 지지 |
| 거푸집 및 동바리공사 | `ppdoc:SteelShapeSpec / ppdoc:hasMaterialGrade` | SS275 |

## 13. 분개 기준

분개는 원본 행을 바꾸는 작업이 아니라 원본 행에 해석 관계를 붙이는 작업이다.

| 분개 대상 | 기준 필드 | RDF 관계 |
| --- | --- | --- |
| 공종 | 목차/헤딩, 품명, 시트 위치 | `ppdoc:hasWorkType`, `ppdoc:hasSubWorkType` |
| 세부 작업 분류 | 품명, 규격, 단위, 공종 | `ppdoc:belongsToDetailCategory`, `ppdoc:hasCategoryItem` |
| 규격 속성 | 원본 규격 문자열, 수량산출 규격 단서, 품명, 공종 | `ppdoc:hasConcreteMix`, `ppdoc:hasRebarSpec`, `ppdoc:hasFormworkSpec`, `ppdoc:hasSteelShapeSpec` |
| 규격 객체 | 내역 항목 또는 수량산출 항목의 규격 단서 | `ppdoc:hasSpecificationObject` |
| 수량산출 근거 | 위치, 부재, 단위, 수량 일치 | `ppdoc:hasQuantityBasis` |
| 집계 금액 | 공종, 금액 합계 | `ppdoc:aggregatesTo` |

## 14. RDF 매핑 요약

```turtle
ppdoc:progress-payment-documents-sample
    ppdoc:hasPart ppdoc:rc-progress-payment-documents-sample .

ppdoc:rc-progress-payment-documents-sample
    ppdoc:hasPart ppdoc:progress-payment-statement-sample ;
    ppdoc:hasWorkType ppdoc:worktype-rc .

ppdoc:work-type-detail-sheet-sample
    ppdoc:hasDataFormat ppdoc:boq-item-table-format-sample ;
    ppdoc:hasBoQItem ppdoc:boq-concrete-ready-mix-001 .

ppdoc:boq-item-table-format-sample
    ppdoc:definesField ppdoc:field-item-name ,
        ppdoc:field-specification ,
        ppdoc:field-current-quantity ,
        ppdoc:field-unit-price ,
        ppdoc:field-amount .

ppdoc:boq-concrete-ready-mix-001
    a ppdoc:BoQItem ;
    ppdoc:hasItemName "레미콘" ;
    ppdoc:hasSpecification "25-24-150" ;
    ppdoc:hasCurrentQuantity "120.5"^^xsd:decimal ;
    ppdoc:belongsToDetailCategory ppdoc:category-ready-mixed-concrete ;
    ppdoc:hasConcreteMix ppdoc:concrete-mix-25-24-150 ;
    ppdoc:hasQuantityBasis ppdoc:quantity-concrete-slab-001 ;
    ppdoc:aggregatesTo ppdoc:summary-concrete-work-sample .

ppdoc:quantity-concrete-slab-001
    a ppdoc:ConcreteQuantityCalculationItem ;
    ppdoc:hasCalculatedVolume "120.5"^^xsd:decimal ;
    ppdoc:hasConcreteMix ppdoc:concrete-mix-25-24-150 ;
    ppdoc:isQuantityBasisFor ppdoc:boq-concrete-ready-mix-001 .

ppdoc:concrete-mix-25-24-150
    a ppdoc:ConcreteMix ;
    ppdoc:hasDesignStrength "24"^^xsd:decimal ;
    ppdoc:hasStrengthUnit "MPa" ;
    ppdoc:hasSlump "150"^^xsd:decimal ;
    ppdoc:hasSlumpUnit "mm" ;
    ppdoc:hasMaxAggregateSize "25"^^xsd:decimal ;
    ppdoc:hasAggregateSizeUnit "mm" .
```

이 구조에서는 내역 항목(`BoQItem`)이 금액 산정 행의 중심이고, 수량산출 항목(`QuantityCalculationItem`)은 수량 근거의 중심이다. 규격 객체는 둘 중 하나에 종속시키지 않고 공유 참조한다. 분개 결과가 틀리거나 바뀌어도 원본 행과 필드 정의는 그대로 남는다.
