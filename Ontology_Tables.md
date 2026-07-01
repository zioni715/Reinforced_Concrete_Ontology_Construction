# RDF/RDFS 구축을 위한 용어표, 관계표, Domain-Range 표

## 1. 작성 기준

본 문서는 `Progress_Payment_Structure.md`, `Document_Relation.md`, `Labeled_Document_Relation.md`를 바탕으로 철근콘크리트 공종 기성서류 RDF/RDFS 구축에 필요한 핵심 용어와 관계를 정리한 것이다.

RDF local name은 Turtle 작성 시 사용할 수 있는 영문 식별자 후보이다. 실제 네임스페이스는 추후 다음과 같이 둘 수 있다.

```turtle
@prefix ppdoc: <https://example.org/rc-progress-payment#> .
```

RDFS의 `rdfs:domain`, `rdfs:range`는 추론용 기본 범위로만 사용한다. 필수성, 조건부 포함, 값 범위, 단위 검증은 RDFS보다 SHACL에서 다루는 것이 적절하다.

---

## 2. 핵심 클래스 용어표

| 한국어 용어 | RDF local name | 구분 | 상위 클래스 후보 | 설명 |
|---|---|---|---|---|
| 기성서류 온톨로지 개체 | ProgressPaymentEntity | Class | rdfs:Resource | 본 온톨로지의 최상위 개체 |
| 행위자 | Actor | Class | ProgressPaymentEntity | 문서를 작성, 제출, 검토, 승인하는 주체 |
| 시공사 | Contractor | Class | Actor | 기성서류를 작성하고 제출하는 주체 |
| 현장 | SiteOffice | Class | Actor | 시공사 기성서류를 접수하고 감리본사로 송부하는 현장 조직 |
| 감리본사 | SupervisionHeadOffice | Class | Actor | 기성서류를 검토하고 발주처 송부 문서를 구성하는 주체 |
| 본사 | HeadOffice | Class | Actor | 발주처로 공문을 송부하는 조직 |
| 발주처 | Owner | Class | Actor | 검사, 승인, 최종 수신 주체 |
| 검사자 | Inspector | Class | Actor | 기성검사를 수행하는 사람 또는 조직 |
| 문서 자원 | DocumentResource | Class | ProgressPaymentEntity | 문서군과 개별 문서를 포괄하는 상위 클래스 |
| 문서군 | DocumentGroup | Class | DocumentResource | 여러 문서를 묶는 상위 단위 |
| 문서 | Document | Class | DocumentResource | 실제 제출, 첨부, 검토되는 개별 문서 |
| 절차 | Procedure | Class | ProgressPaymentEntity | 검사, 승인, 제출 등 업무 단계 |
| 시공사 기성서류 | ContractorProgressPaymentPackage | Class | DocumentGroup | 시공사가 작성하는 기성서류 묶음 |
| 첨부서류 | AttachmentBundle | Class | DocumentGroup | 공문에 첨부되는 기성 관련 문서군 |
| 내역서 | StatementDocument | Class | DocumentGroup | 기성금액 산정의 중심이 되는 내역 문서군 |
| 공사기성부분 내역서 | ProgressPaymentStatement | Class | DocumentGroup | 원가계산서, 집계표, 공종별내역서, 수량산출서를 포함하는 문서군 |
| 주요자재 검수 및 수불부 | MaterialReceiptAndInspectionLedger | Class | DocumentGroup | 철근, 레미콘, 거푸집 등 주요자재 증빙 문서군 |
| 검측서류 및 사진대지 | InspectionAndPhotoDocumentGroup | Class | DocumentGroup | 공종별 검측서류와 사진대지를 묶는 문서군 |
| 현장-감리본사 공문발송 문서군 | SiteToSupervisionSubmissionPackage | Class | DocumentGroup | 현장에서 감리본사로 송부되는 문서군 |
| 본사-발주처 공문발송 문서군 | HeadOfficeToOwnerSubmissionPackage | Class | DocumentGroup | 본사에서 발주처로 송부되는 문서군 |
| 기성검사 결과 보고 | InspectionResultReportPackage | Class | DocumentGroup | 기성검사 후 발주처에 보고되는 문서군 |
| 공문 | OfficialLetter | Class | Document | 대표이사 명의 사용인감계 제출 직인 날인본 |
| 기성부분 검사원 | ProgressPaymentInspectionRequest | Class | Document | 기성검사 요청 문서 |
| 청구기성 요약 | ProgressPaymentClaimSummary | Class | Document | 청구 기성금액을 요약하는 문서 |
| 선금공제 내역 | AdvancePaymentDeductionStatement | Class | Document | 선금이 있는 경우 포함되는 조건부 문서 |
| 원가계산서 | CostCalculationSheet | Class | Document | 공사기성부분 내역서의 원가계산 문서 |
| 공종별집계표 | WorkTypeSummarySheet | Class | Document | 공종별 금액을 집계하는 문서 |
| 공종별내역서 | WorkTypeDetailSheet | Class | Document | 공종별 수량, 단가, 금액을 제시하는 문서 |
| 수량산출서 | QuantityCalculationSheet | Class | Document | 공종별 수량 산출 근거 문서 |
| 자재 증빙 문서 | MaterialEvidenceDocument | Class | Document | 자재 반입, 송장, 시험성적, 검수 등 증빙 문서 |
| 검측 문서 | InspectionDocument | Class | Document | 시공 확인과 검측 결과를 기록하는 문서 |
| 사진대지 | PhotoSheet | Class | Document | 검측 또는 검사 결과를 사진으로 뒷받침하는 문서 |
| 기성부분 감리조서 | SupervisionProgressPaymentReport | Class | Document | 감리 검토 문서 |
| 공사 기성검사 수행계획서 | InspectionExecutionPlan | Class | Document | 기성검사 수행 계획 문서 |
| 세부 수행계획서 | DetailedExecutionPlan | Class | Document | 수행계획서의 세부 계획 문서 |
| 사전검토 의견서 | PriorReviewOpinion | Class | Document | 기성검사원에 대한 사전검토 의견 문서 |
| 검사자 임명 및 검사일자 통보 | InspectorAppointmentNotice | Class | Document | 검사자와 검사일자를 통보하는 문서 |
| 기성검사 조서 | ProgressPaymentInspectionRecord | Class | Document | 기성검사 결과를 기록하는 조서 |
| 기성검토의견서 | ProgressPaymentReviewOpinion | Class | Document | 기성검토 결과 의견 문서 |
| 공사관리관 입회확인서 | ConstructionManagerAttendanceConfirmation | Class | Document | 공사관리관 입회 확인 문서 |
| 안전관리비 사용내역 및 증빙 | SafetyCostEvidenceDocument | Class | Document | 안전관리비 정산 또는 청구 시 포함되는 조건부 문서 |
| 보험료 납입 증명서 | InsurancePaymentCertificate | Class | Document | 보험료 정산 또는 증빙 시 포함되는 조건부 문서 |
| 기타 발주처 요청 서류 | OwnerRequestedDocument | Class | Document | 발주처 요구 조건에 따라 포함되는 문서 |
| 내역 그룹 | WorkDetailGroup | Class | ProgressPaymentEntity | 특정 공종의 내역 항목 묶음 |
| 철근공사 내역 | RebarWorkDetailGroup | Class | WorkDetailGroup | 철근공사의 수량, 단가, 금액 내역 |
| 콘크리트공사 내역 | ConcreteWorkDetailGroup | Class | WorkDetailGroup | 콘크리트공사의 수량, 단가, 금액 내역 |
| 거푸집공사 내역 | FormworkDetailGroup | Class | WorkDetailGroup | 거푸집공사의 수량, 단가, 금액 내역 |
| 공종 | WorkType | Class | ProgressPaymentEntity | 철근, 콘크리트, 거푸집 등 공사 종류 |
| 철근공사 | RebarWork | Class | WorkType | 철근 관련 공종 |
| 콘크리트공사 | ConcreteWork | Class | WorkType | 콘크리트 관련 공종 |
| 거푸집공사 | Formwork | Class | WorkType | 거푸집 관련 공종 |
| 집계금액 | SummaryAmount | Class | ProgressPaymentEntity | 공종별 또는 상위 공종의 집계 금액 |
| 산출 항목 | QuantityCalculationItem | Class | ProgressPaymentEntity | 수량산출서 내부의 계산 대상 단위 |
| 철근 수량산출 항목 | RebarQuantityCalculationItem | Class | QuantityCalculationItem | 철근 규격, 직경, 길이, 개수, 산출중량을 갖는 항목 |
| 콘크리트 수량산출 항목 | ConcreteQuantityCalculationItem | Class | QuantityCalculationItem | 위치, 부재명, 강도, 길이, 폭, 높이, 산출체적을 갖는 항목 |
| 거푸집 수량산출 항목 | FormworkQuantityCalculationItem | Class | QuantityCalculationItem | 위치, 부재명, 종류, 길이, 높이, 산출면적을 갖는 항목 |
| 정보 필드 | InformationField | Class | ProgressPaymentEntity | 문서 또는 내역 항목 내부의 속성값 정의 |
| 검측 항목 | InspectionItem | Class | ProgressPaymentEntity | 검측문서에서 확인하는 세부 항목 |
| 기성검사 | ProgressPaymentInspection | Class | Procedure | 기성검사를 수행하는 절차 |
| 서류검사 | DocumentInspection | Class | Procedure | 기성서류를 검사하는 절차 |
| 현장검사 | SiteInspection | Class | Procedure | 실제 현장을 검사하는 절차 |
| 발주처 승인 | OwnerApproval | Class | Procedure | 발주처의 최종 승인 단계 |
| 제본 제출 | BoundStatementSubmission | Class | Procedure | 기성서류 내역서 제본 제출 단계 |

---

## 3. 정보 필드 용어표

| 한국어 필드 | RDF local name | 권장 속성 유형 | 권장 range | 단위 또는 기준 |
|---|---|---|---|---|
| 품명 | hasItemName | DatatypeProperty | xsd:string | 품목명 |
| 규격 | hasSpecification | DatatypeProperty | xsd:string | 자재 또는 공종 규격 |
| 단위 | hasQuantityUnit | DatatypeProperty | xsd:string | ton, m3, m2, 개소 등 |
| 계약수량 | hasContractQuantity | DatatypeProperty | xsd:decimal | 공종별 단위 |
| 전회수량 | hasPreviousQuantity | DatatypeProperty | xsd:decimal | 공종별 단위 |
| 금회수량 | hasCurrentQuantity | DatatypeProperty | xsd:decimal | 공종별 단위 |
| 누계수량 | hasCumulativeQuantity | DatatypeProperty | xsd:decimal | 공종별 단위 |
| 단가 | hasUnitPrice | DatatypeProperty | xsd:decimal | 원/단위 |
| 금액 | hasAmount | DatatypeProperty | xsd:decimal | 원 |
| 위치 | hasLocation | DatatypeProperty | xsd:string | 동, 층, 구간, 부위 등 |
| 부재명 | hasMemberName | DatatypeProperty | xsd:string | 기둥, 보, 슬래브, 벽체 등 |
| 철근 규격 | hasRebarSpecification | DatatypeProperty | xsd:string | SD400, SD500 등 |
| 철근 직경 | hasRebarDiameter | DatatypeProperty | xsd:decimal | mm |
| 길이 | hasLength | DatatypeProperty | xsd:decimal | m 또는 mm |
| 폭 | hasWidth | DatatypeProperty | xsd:decimal | m 또는 mm |
| 높이 | hasHeight | DatatypeProperty | xsd:decimal | m 또는 mm |
| 개수 | hasCount | DatatypeProperty | xsd:integer | 개 |
| 단위중량 | hasUnitWeight | DatatypeProperty | xsd:decimal | kg/m 또는 kg/본 |
| 산출중량 | hasCalculatedWeight | DatatypeProperty | xsd:decimal | kg 또는 ton |
| 콘크리트 강도 | hasConcreteStrength | DatatypeProperty | xsd:decimal | MPa |
| 산출체적 | hasCalculatedVolume | DatatypeProperty | xsd:decimal | m3 |
| 거푸집 종류 | hasFormworkType | DatatypeProperty | xsd:string | 합판거푸집, 유로폼 등 |
| 산출면적 | hasCalculatedArea | DatatypeProperty | xsd:decimal | m2 |
| 문서명 | hasDocumentTitle | DatatypeProperty | xsd:string | 실제 문서 제목 |
| 문서 식별자 | hasDocumentIdentifier | DatatypeProperty | xsd:string | 회차, 문서번호, 제출번호 등 |
| 작성일 | hasCreationDate | DatatypeProperty | xsd:date | 문서 생성일 |
| 제출일 | hasSubmissionDate | DatatypeProperty | xsd:date | 문서 제출일 |
| 원본 파일명 | hasSourceFileName | DatatypeProperty | xsd:string | 원본 문서 파일명 |
| 원본 페이지 | hasSourcePage | DatatypeProperty | xsd:string | 페이지 번호 또는 범위 |
| 원본 시트명 | hasSourceSheetName | DatatypeProperty | xsd:string | 엑셀 시트명 |
| 원본 셀 주소 | hasSourceCellAddress | DatatypeProperty | xsd:string | 엑셀 셀 주소 |
| 통화 | hasCurrency | DatatypeProperty | xsd:string | KRW 등 |
| 단위 기호 | hasUnitSymbol | DatatypeProperty | xsd:string | mm, m2, m3, kg 등 |

---

## 4. 관계표

| 한국어 관계 라벨 | RDF local name | 속성 유형 | 관계 방향 | 의미 |
|---|---|---|---|---|
| 작성한다 | creates | ObjectProperty | Actor -> DocumentResource | 행위자가 문서 또는 문서군을 작성함 |
| 작성자이다 | createdBy | ObjectProperty | DocumentResource -> Actor | 문서 또는 문서군의 작성 주체를 연결함 |
| 포함한다 | hasPart | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 상위 개체가 하위 개체를 구성 요소로 포함함 |
| 포함된다 | isPartOf | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 하위 개체가 상위 개체에 포함됨 |
| 첨부한다 | attaches | ObjectProperty | DocumentResource -> DocumentResource | 제출 문서 또는 문서군에 다른 문서가 첨부됨 |
| 조건부 포함 | conditionallyIncludes | ObjectProperty | DocumentResource -> DocumentResource | 특정 조건이 있을 때만 문서를 포함함 |
| 제출한다 | submittedTo | ObjectProperty | DocumentResource -> Actor | 문서 또는 문서군이 특정 행위자에게 제출됨 |
| 제출자이다 | submittedBy | ObjectProperty | DocumentResource -> Actor | 문서 또는 문서군의 제출 주체를 연결함 |
| 송부한다 | forwardedTo | ObjectProperty | DocumentResource -> Actor | 검토 또는 접수 후 다음 기관으로 문서가 송부됨 |
| 송부자이다 | forwardedBy | ObjectProperty | DocumentResource -> Actor | 문서 또는 문서군의 송부 주체를 연결함 |
| 검토한다 | reviewedBy | ObjectProperty | DocumentResource -> Actor | 문서가 특정 주체에 의해 검토됨 |
| 검사한다 | inspectedBy | ObjectProperty | Procedure -> Actor | 검사 절차가 특정 검사 주체에 의해 수행됨 |
| 승인한다 | approvedBy | ObjectProperty | ProgressPaymentEntity -> Actor | 문서, 결과, 절차가 특정 주체에 의해 승인됨 |
| 후속 단계로 이어진다 | precedes | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 절차 또는 문서 흐름상 다음 단계로 이어짐 |
| 이전 단계이다 | follows | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 절차 또는 문서 흐름상 이전 단계의 역관계 |
| 집계된다 | aggregatesTo | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 하위 내역 또는 금액이 상위 집계 대상으로 합산됨 |
| 집계한다 | aggregates | ObjectProperty | ProgressPaymentEntity -> ProgressPaymentEntity | 상위 집계 대상이 하위 내역 또는 금액을 집계함 |
| 산출 근거가 된다 | isQuantityBasisFor | ObjectProperty | QuantityCalculationSheet 또는 QuantityCalculationItem -> WorkDetailGroup | 수량산출서 또는 산출 항목이 공종별 내역의 수량 근거가 됨 |
| 산출 근거를 가진다 | hasQuantityBasis | ObjectProperty | WorkDetailGroup -> QuantityCalculationSheet 또는 QuantityCalculationItem | 공종별 내역이 수량산출 근거를 가짐 |
| 증빙한다 | evidences | ObjectProperty | MaterialEvidenceDocument -> WorkDetailGroup | 자재 증빙 문서가 공종별 내역을 증빙함 |
| 증빙자료를 가진다 | hasEvidence | ObjectProperty | WorkDetailGroup -> MaterialEvidenceDocument | 공종별 내역이 관련 증빙자료를 가짐 |
| 검측 근거가 된다 | isInspectionBasisFor | ObjectProperty | InspectionDocument -> WorkDetailGroup | 검측 문서가 공종별 내역의 시공 확인 근거가 됨 |
| 검측 근거를 가진다 | hasInspectionBasis | ObjectProperty | WorkDetailGroup -> InspectionDocument | 공종별 내역이 검측 근거 문서를 가짐 |
| 사진 근거가 된다 | isPhotoEvidenceFor | ObjectProperty | PhotoSheet -> Document 또는 Procedure | 사진대지가 검측문서나 검사 결과를 뒷받침함 |
| 사진 근거를 가진다 | hasPhotoEvidence | ObjectProperty | Document 또는 Procedure -> PhotoSheet | 문서 또는 절차가 사진 근거를 가짐 |
| 정보 필드를 가진다 | hasInformationField | ObjectProperty | ProgressPaymentEntity -> InformationField | 문서, 내역, 산출 항목이 정보 필드 정의를 가짐 |
| 검측 항목을 가진다 | hasInspectionItem | ObjectProperty | InspectionDocument -> InspectionItem | 검측 문서가 세부 검측 항목을 가짐 |
| 공종을 가진다 | hasWorkType | ObjectProperty | ProgressPaymentEntity -> WorkType | 문서, 내역, 산출 항목이 특정 공종과 연결됨 |
| 관련 문서를 가진다 | hasRelatedDocument | ObjectProperty | ProgressPaymentEntity -> DocumentResource | 인스턴스가 관련 문서와 연결됨 |
| 출처 문서를 가진다 | hasSourceDocument | ObjectProperty | ProgressPaymentEntity -> DocumentResource | 추출값이나 인스턴스의 원천 문서를 연결함 |

---

## 5. Object Property Domain-Range 표

| RDF property | rdfs:domain | rdfs:range | 역관계 후보 | 비고 |
|---|---|---|---|---|
| ppdoc:creates | ppdoc:Actor | ppdoc:DocumentResource | ppdoc:createdBy | 작성 주체에서 문서로 향하는 관계 |
| ppdoc:createdBy | ppdoc:DocumentResource | ppdoc:Actor | ppdoc:creates | 실제 인스턴스에서는 문서 -> 작성자 방향이 질의에 편리함 |
| ppdoc:hasPart | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:isPartOf | 문서군-문서, 문서-항목, 절차-세부절차에 공통 사용 |
| ppdoc:isPartOf | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:hasPart | 포함 관계의 역방향 |
| ppdoc:attaches | ppdoc:DocumentResource | ppdoc:DocumentResource | 없음 | 제출 문서 또는 문서군의 첨부 관계 |
| ppdoc:conditionallyIncludes | ppdoc:DocumentResource | ppdoc:DocumentResource | 없음 | 선금공제, 안전관리비, 보험료, 기타 요청서류 등에 사용 |
| ppdoc:submittedTo | ppdoc:DocumentResource | ppdoc:Actor | 없음 | 제출 대상 기관 또는 주체 |
| ppdoc:submittedBy | ppdoc:DocumentResource | ppdoc:Actor | 없음 | 제출 주체 |
| ppdoc:forwardedTo | ppdoc:DocumentResource | ppdoc:Actor | 없음 | 송부 대상 기관 또는 주체 |
| ppdoc:forwardedBy | ppdoc:DocumentResource | ppdoc:Actor | 없음 | 송부 주체 |
| ppdoc:reviewedBy | ppdoc:DocumentResource | ppdoc:Actor | 없음 | 검토 주체 |
| ppdoc:inspectedBy | ppdoc:Procedure | ppdoc:Actor | 없음 | 검사 수행 주체 |
| ppdoc:approvedBy | ppdoc:ProgressPaymentEntity | ppdoc:Actor | 없음 | 발주처 승인 등 |
| ppdoc:precedes | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:follows | 절차 또는 문서 흐름의 순서 |
| ppdoc:follows | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:precedes | 선행 단계의 역방향 |
| ppdoc:aggregatesTo | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:aggregates | 공종별내역 -> 공종별집계표, 공종별 집계금액 -> 철근콘크리트공사 집계금액 |
| ppdoc:aggregates | ppdoc:ProgressPaymentEntity | ppdoc:ProgressPaymentEntity | ppdoc:aggregatesTo | 상위 집계 대상에서 하위 항목으로 향하는 관계 |
| ppdoc:isQuantityBasisFor | ppdoc:ProgressPaymentEntity | ppdoc:WorkDetailGroup | ppdoc:hasQuantityBasis | 수량산출서 또는 산출 항목 -> 공종별 내역 |
| ppdoc:hasQuantityBasis | ppdoc:WorkDetailGroup | ppdoc:ProgressPaymentEntity | ppdoc:isQuantityBasisFor | 공종별 내역 -> 수량산출 근거 |
| ppdoc:evidences | ppdoc:MaterialEvidenceDocument | ppdoc:WorkDetailGroup | ppdoc:hasEvidence | 자재 증빙 문서 -> 공종별 내역 |
| ppdoc:hasEvidence | ppdoc:WorkDetailGroup | ppdoc:MaterialEvidenceDocument | ppdoc:evidences | 공종별 내역 -> 자재 증빙 문서 |
| ppdoc:isInspectionBasisFor | ppdoc:InspectionDocument | ppdoc:WorkDetailGroup | ppdoc:hasInspectionBasis | 검측 문서 -> 공종별 내역 |
| ppdoc:hasInspectionBasis | ppdoc:WorkDetailGroup | ppdoc:InspectionDocument | ppdoc:isInspectionBasisFor | 공종별 내역 -> 검측 근거 문서 |
| ppdoc:isPhotoEvidenceFor | ppdoc:PhotoSheet | ppdoc:ProgressPaymentEntity | ppdoc:hasPhotoEvidence | 사진대지 -> 검측문서, 검사 결과, 절차 |
| ppdoc:hasPhotoEvidence | ppdoc:ProgressPaymentEntity | ppdoc:PhotoSheet | ppdoc:isPhotoEvidenceFor | 검측문서, 검사 결과, 절차 -> 사진대지 |
| ppdoc:hasInformationField | ppdoc:ProgressPaymentEntity | ppdoc:InformationField | 없음 | 문서, 내역 그룹, 산출 항목의 필드 정의 |
| ppdoc:hasInspectionItem | ppdoc:InspectionDocument | ppdoc:InspectionItem | 없음 | 검측체크리스트 또는 타설일보의 확인 항목 |
| ppdoc:hasWorkType | ppdoc:ProgressPaymentEntity | ppdoc:WorkType | 없음 | 철근, 콘크리트, 거푸집 공종 연결 |
| ppdoc:hasRelatedDocument | ppdoc:ProgressPaymentEntity | ppdoc:DocumentResource | 없음 | 실제 인스턴스 간 관련 문서 연결 |
| ppdoc:hasSourceDocument | ppdoc:ProgressPaymentEntity | ppdoc:DocumentResource | 없음 | 추출값 또는 인스턴스의 원천 문서 연결 |

---

## 6. Datatype Property Domain-Range 표

| RDF property | rdfs:domain | rdfs:range | 적용 대상 | 비고 |
|---|---|---|---|---|
| ppdoc:hasDocumentTitle | ppdoc:DocumentResource | xsd:string | 문서, 문서군 | 실제 문서 제목 |
| ppdoc:hasDocumentIdentifier | ppdoc:DocumentResource | xsd:string | 문서, 문서군 | 회차, 문서번호, 제출번호 |
| ppdoc:hasCreationDate | ppdoc:DocumentResource | xsd:date | 문서, 문서군 | 작성일 |
| ppdoc:hasSubmissionDate | ppdoc:DocumentResource | xsd:date | 문서, 문서군 | 제출일 |
| ppdoc:hasSourceFileName | ppdoc:ProgressPaymentEntity | xsd:string | 문서, 추출값, 산출 항목 | 원본 파일명 |
| ppdoc:hasSourcePage | ppdoc:ProgressPaymentEntity | xsd:string | 문서, 추출값, 산출 항목 | PDF/HWP 페이지 또는 범위 |
| ppdoc:hasSourceSheetName | ppdoc:ProgressPaymentEntity | xsd:string | 엑셀 기반 추출값 | 시트명 |
| ppdoc:hasSourceCellAddress | ppdoc:ProgressPaymentEntity | xsd:string | 엑셀 기반 추출값 | 셀 주소 |
| ppdoc:hasItemName | ppdoc:WorkDetailGroup | xsd:string | 공종별 내역 | 품명 |
| ppdoc:hasSpecification | ppdoc:WorkDetailGroup | xsd:string | 공종별 내역 | 규격 |
| ppdoc:hasQuantityUnit | ppdoc:WorkDetailGroup | xsd:string | 공종별 내역 | 단위 |
| ppdoc:hasContractQuantity | ppdoc:WorkDetailGroup | xsd:decimal | 공종별 내역 | 계약수량 |
| ppdoc:hasPreviousQuantity | ppdoc:WorkDetailGroup | xsd:decimal | 공종별 내역 | 전회수량 |
| ppdoc:hasCurrentQuantity | ppdoc:WorkDetailGroup | xsd:decimal | 공종별 내역 | 금회수량 |
| ppdoc:hasCumulativeQuantity | ppdoc:WorkDetailGroup | xsd:decimal | 공종별 내역 | 누계수량 |
| ppdoc:hasUnitPrice | ppdoc:WorkDetailGroup | xsd:decimal | 공종별 내역 | 원/단위 |
| ppdoc:hasAmount | ppdoc:ProgressPaymentEntity | xsd:decimal | 공종별 내역, 집계금액, 청구기성 요약 | 금액 |
| ppdoc:hasCurrency | ppdoc:ProgressPaymentEntity | xsd:string | 금액이 있는 개체 | KRW 등 |
| ppdoc:hasLocation | ppdoc:QuantityCalculationItem | xsd:string | 수량산출 항목 | 위치 |
| ppdoc:hasMemberName | ppdoc:QuantityCalculationItem | xsd:string | 수량산출 항목 | 부재명 |
| ppdoc:hasRebarSpecification | ppdoc:RebarQuantityCalculationItem | xsd:string | 철근 수량산출 항목 | 철근 규격 |
| ppdoc:hasRebarDiameter | ppdoc:RebarQuantityCalculationItem | xsd:decimal | 철근 수량산출 항목 | mm |
| ppdoc:hasLength | ppdoc:QuantityCalculationItem | xsd:decimal | 수량산출 항목 | m 또는 mm |
| ppdoc:hasWidth | ppdoc:ConcreteQuantityCalculationItem | xsd:decimal | 콘크리트 수량산출 항목 | m 또는 mm |
| ppdoc:hasHeight | ppdoc:QuantityCalculationItem | xsd:decimal | 콘크리트, 거푸집 수량산출 항목 | m 또는 mm |
| ppdoc:hasCount | ppdoc:RebarQuantityCalculationItem | xsd:integer | 철근 수량산출 항목 | 개수 |
| ppdoc:hasUnitWeight | ppdoc:RebarQuantityCalculationItem | xsd:decimal | 철근 수량산출 항목 | kg/m 또는 kg/본 |
| ppdoc:hasCalculatedWeight | ppdoc:RebarQuantityCalculationItem | xsd:decimal | 철근 수량산출 항목 | kg 또는 ton |
| ppdoc:hasConcreteStrength | ppdoc:ConcreteQuantityCalculationItem | xsd:decimal | 콘크리트 수량산출 항목 | MPa |
| ppdoc:hasCalculatedVolume | ppdoc:ConcreteQuantityCalculationItem | xsd:decimal | 콘크리트 수량산출 항목 | m3 |
| ppdoc:hasFormworkType | ppdoc:FormworkQuantityCalculationItem | xsd:string | 거푸집 수량산출 항목 | 거푸집 종류 |
| ppdoc:hasCalculatedArea | ppdoc:FormworkQuantityCalculationItem | xsd:decimal | 거푸집 수량산출 항목 | m2 |
| ppdoc:hasUnitSymbol | ppdoc:ProgressPaymentEntity | xsd:string | 수량, 금액, 산출값 보유 개체 | mm, m, m2, m3, kg, ton 등 |

---

## 7. 주요 문서 인스턴스 후보표

실제 RDF 데이터셋 작성 시 아래 항목은 클래스가 아니라 개별 인스턴스로 생성하는 것이 적절하다.

| 실제 문서 또는 항목 | 권장 타입 | 필요한 식별 정보 | 연결 관계 후보 |
|---|---|---|---|
| 제13회 기성검사 조서 | ProgressPaymentInspectionRecord | 회차, 문서번호, 제출일 | ppdoc:hasPart, ppdoc:submittedTo, ppdoc:approvedBy |
| 기성 세부내역.xlsx | WorkTypeDetailSheet | 파일명, 시트명, 행 번호 | ppdoc:hasPart, ppdoc:aggregatesTo, ppdoc:hasSourceDocument |
| 철근공사 내역 행 | RebarWorkDetailGroup | 행 번호, 품명, 규격 | ppdoc:hasWorkType, ppdoc:hasQuantityBasis, ppdoc:hasEvidence |
| 콘크리트공사 내역 행 | ConcreteWorkDetailGroup | 행 번호, 품명, 규격 | ppdoc:hasWorkType, ppdoc:hasQuantityBasis, ppdoc:hasEvidence |
| 거푸집공사 내역 행 | FormworkDetailGroup | 행 번호, 품명, 규격 | ppdoc:hasWorkType, ppdoc:hasQuantityBasis, ppdoc:hasEvidence |
| 철근 수량산출 항목 | RebarQuantityCalculationItem | 위치, 부재명, 직경, 길이 | ppdoc:isQuantityBasisFor |
| 콘크리트 수량산출 항목 | ConcreteQuantityCalculationItem | 위치, 부재명, 강도, 체적 | ppdoc:isQuantityBasisFor |
| 거푸집 수량산출 항목 | FormworkQuantityCalculationItem | 위치, 부재명, 종류, 면적 | ppdoc:isQuantityBasisFor |
| 철근 시험성적서 | MaterialEvidenceDocument | 파일명, 시험번호, 발행일 | ppdoc:evidences |
| 레미콘 납품서 | MaterialEvidenceDocument | 파일명, 납품일, 차량번호 | ppdoc:evidences |
| 철근 배근 검측체크리스트 | InspectionDocument | 파일명, 검측일, 위치 | ppdoc:isInspectionBasisFor, ppdoc:hasInspectionItem |
| 콘크리트 타설일보 | InspectionDocument | 파일명, 타설일, 타설 위치 | ppdoc:isInspectionBasisFor, ppdoc:hasInspectionItem |
| 검측 사진대지 | PhotoSheet | 파일명, 촬영일, 촬영 위치 | ppdoc:isPhotoEvidenceFor |

---

## 8. RDFS 작성 시 우선순위

1. `ProgressPaymentEntity`, `Actor`, `DocumentResource`, `DocumentGroup`, `Document`, `Procedure`, `WorkDetailGroup`, `QuantityCalculationItem`, `InspectionItem`을 먼저 클래스화한다.
2. `hasPart`, `attaches`, `submittedTo`, `forwardedTo`, `reviewedBy`, `approvedBy`, `precedes`로 문서 흐름을 구성한다.
3. `aggregatesTo`, `isQuantityBasisFor`, `evidences`, `isInspectionBasisFor`, `isPhotoEvidenceFor`로 산정 근거와 증빙 관계를 구성한다.
4. 공종별 수량과 금액 필드는 datatype property로 둔다.
5. 필수 문서 여부, 조건부 포함 여부, 단위 일관성, 값 범위는 SHACL shapes에서 별도 검증한다.
