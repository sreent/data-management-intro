# E-invoicing (Peppol) — Slide-Ready Seed Data

A minimal dataset for the Chapter 7 XML for Contracts topic, small enough to trace by hand on teaching slides. Designed to demonstrate key concepts: well-formedness vs validity, XSD four-check model, DTD limitations, XPath extraction, namespace handling, and JSON Schema validation.

**1 XSD contract | 1 valid invoice | 1 invalid invoice (4 planted errors) | 1 DTD | 1 namespaced invoice**

---

## File Inventory

| File | Purpose | Used in |
|------|---------|---------|
| `invoice_schema.xsd` | XSD contract — the validation rules | Lab Parts 1–2 (contract cards, validation) |
| `invoice_valid.xml` | Valid invoice passing all XSD checks | Lab Parts 2, 4 (validation, XPath) |
| `invoice_invalid.xml` | Invalid invoice with 4 planted errors | Lab Parts 2–3 (predict-then-verify, DTD comparison) |
| `invoice.dtd` | DTD equivalent — demonstrates limitations | Lab Part 3 (DTD vs XSD comparison) |
| `invoice_namespaced.xml` | Same valid invoice with `inv:` namespace prefix | Lab Part 4 Q16 (namespace trap) |

---

## Domain Context

A simplified e-invoicing portal inspired by the Peppol network and Singapore's InvoiceNow initiative. The domain sits at a **low-trust boundary** — two independent organisations exchanging structured documents where the schema is published in advance and validation is mandatory.

**Parties:**
- **Supplier:** Kopi Tech Pte Ltd, 88 Amoy Street, Singapore 069907
- **Customer:** Marina Bay Trading Co., 10 Collyer Quay, Singapore 049315
- **Currency:** SGD (Singapore Dollars)

---

## Valid Invoice (INV-2025-0042)

| Field | Value |
|-------|-------|
| InvoiceNumber | INV-2025-0042 |
| IssueDate | 2025-02-13 |
| Supplier | Kopi Tech Pte Ltd |
| Customer | Marina Bay Trading Co. |

### Invoice Lines

| # | Item | Qty | Amount (SGD) |
|---|------|-----|-------------|
| 1 | Cloud Hosting (Annual) | 1 | 12,000.00 |
| 2 | SSL Certificate | 5 | 250.00 |
| 3 | Technical Support (Hours) | 20 | 3,000.00 |

### Monetary Total

| Component | Amount (SGD) |
|-----------|-------------|
| Line Extension | 15,250.00 |
| Tax (9% GST) | 1,372.50 |
| Payable | 16,622.50 |

### Payment Terms

- Method Code: 30 (bank transfer)
- Due Date: 2025-03-15
- Note: Payment within 30 days of invoice date

---

## Invalid Invoice (INV-2025-0099) — 4 Planted Errors

| Error # | What's wrong | XSD rule violated | Four-check category |
|---------|-------------|-------------------|-------------------|
| 1 | MonetaryTotal appears before InvoiceLines | `xs:sequence` requires InvoiceLines before MonetaryTotal | Compositor check |
| 2 | Quantity = -3 | `xs:positiveInteger` rejects negative values | Content check |
| 3 | PaymentMethodCode = "bank_transfer" | `PaymentMethodCodeType` enumeration allows only "30", "42", "48", "1" | Content check |
| 4 | Two Note elements | `maxOccurs="1"` allows at most one Note | Cardinality check |

### Error Independence

Each error is independent — fixing one does not fix another. This design ensures students can identify all four using the four-check model without cascading confusion.

### DTD Detection Matrix

| Error # | XSD catches? | DTD catches? | Why DTD misses it |
|---------|-------------|-------------|-------------------|
| 1 | Yes | Yes | DTD enforces element order via content model |
| 2 | Yes | No | DTD treats Quantity as `#PCDATA` — no type checking |
| 3 | Yes | No | DTD treats PaymentMethodCode as `#PCDATA` — no enumeration |
| 4 | Yes | Yes | DTD declares Note with `?` (zero or one) |

---

## XSD Contract — Key Types

### Named Simple Types

| Type name | Base | Restriction | Allowed values |
|-----------|------|-------------|----------------|
| `CurrencyCodeType` | `xs:string` | Enumeration | SGD, USD, EUR, GBP |
| `PaymentMethodCodeType` | `xs:string` | Enumeration | 30, 42, 48, 1 |

### Named Complex Types

| Type name | Compositor | Children | Notes |
|-----------|-----------|----------|-------|
| `AmountType` | simpleContent + extension | (text: xs:decimal) | Attribute: `currencyID` (CurrencyCodeType, required) |
| `PartyType` | xs:sequence | Name, Address | Both xs:string |
| `InvoiceLineType` | xs:sequence | ItemName, Quantity, LineAmount | Quantity is xs:positiveInteger |
| `InvoiceLinesType` | xs:sequence | InvoiceLine (1..unbounded) | Container element |
| `MonetaryTotalType` | xs:sequence | LineExtensionAmount, TaxAmount, PayableAmount | All AmountType |
| `PaymentMeansType` | xs:sequence | PaymentMethodCode, PaymentDueDate | Code is enumerated; date is xs:date |

### Root Element (Invoice)

Anonymous complex type with `xs:sequence`:

| Child | Type | Cardinality |
|-------|------|-------------|
| InvoiceNumber | xs:string | 1..1 |
| IssueDate | xs:date | 1..1 |
| Supplier | PartyType | 1..1 |
| Customer | PartyType | 1..1 |
| InvoiceLines | InvoiceLinesType | 1..1 |
| MonetaryTotal | MonetaryTotalType | 1..1 |
| PaymentMeans | PaymentMeansType | 0..unbounded |
| Note | xs:string | 0..1 |

---

## Teaching Scenarios Supported

| Scenario | Concept | What to show on slide |
|----------|---------|----------------------|
| **Well-formed vs valid** | Correctness levels | `invoice_invalid.xml` is well-formed (parses) but invalid (XSD rejects). Both levels checked independently. |
| **Four-check model** | Systematic validation | Error 1 = compositor, Error 2 = content (type), Error 3 = content (enumeration), Error 4 = cardinality. All four categories represented. |
| **Contract card reading** | XSD comprehension | Fill in 8-field card for any element: name, parent, compositor, cardinality, type, children, restrictions, attributes. |
| **DTD vs XSD gap** | Technology comparison | DTD catches 2/4 errors (order, cardinality). Misses 2/4 (type, enumeration). DTD treats all content as `#PCDATA`. |
| **XPath extraction** | Data retrieval | `/Invoice/Supplier/Name/text()` → "Kopi Tech Pte Ltd". Predicate: `InvoiceLine[Quantity > 3]` → SSL Certificate, Technical Support. |
| **Namespace trap** | Qualified names | Unqualified path on `invoice_namespaced.xml` returns empty. Must use `inv:` prefix. Same data, different access pattern. |
| **Attribute vs element** | XSD design choice | `currencyID` modelled as attribute on AmountType. Could be a child element — changes XPath from `@currencyID` to `CurrencyCode/text()`. |
| **Enforcement spectrum** | Cross-chapter arc | Engine rejects (Ch5, relational) → Validator rejects (Ch7, XSD/JSON Schema) → Nothing rejects (Ch6, document). |
| **Trust boundary** | Applied scenario | E-invoicing = low trust (cross-org, schema-on-write). Internal API = high trust (same team, schema-on-read). |
| **JSON Schema mapping** | Modern equivalent | XSD `xs:positiveInteger` → JSON Schema `{"type": "integer", "exclusiveMinimum": 0}`. Same discipline, different notation. |

---

## JSON Schema Payload (Failure 3 — Malformed Payment Notification)

Used in Lab Part 5 to demonstrate JSON Schema validation as the modern equivalent of XSD.

### Invalid Payload

```json
{
    "amount": "150.00",
    "currency": "sgd",
    "payment_date": "2025-02-13",
    "merchant_id": "M-2001"
}
```

**Errors:** `amount` is string (should be number), `currency` is lowercase (not in enum), `payment_date` is wrong key (should be `paymentDate`), `merchant_id` is wrong key (should be `merchantId`). The wrong keys trigger both `additionalProperties: false` and `required` violations.

### Valid Payload

```json
{
    "amount": 150.00,
    "currency": "SGD",
    "paymentDate": "2025-02-13",
    "merchantId": "M-2001"
}
```
