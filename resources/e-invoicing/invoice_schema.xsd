<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Named simple types with restrictions -->
  <xs:simpleType name="CurrencyCodeType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="SGD"/>
      <xs:enumeration value="USD"/>
      <xs:enumeration value="EUR"/>
      <xs:enumeration value="GBP"/>
    </xs:restriction>
  </xs:simpleType>

  <xs:simpleType name="PaymentMethodCodeType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="30"/>
      <xs:enumeration value="42"/>
      <xs:enumeration value="48"/>
      <xs:enumeration value="1"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- AmountType: decimal with required currencyID attribute -->
  <xs:complexType name="AmountType">
    <xs:simpleContent>
      <xs:extension base="xs:decimal">
        <xs:attribute name="currencyID" type="CurrencyCodeType" use="required"/>
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>

  <!-- Party type (Supplier and Customer) -->
  <xs:complexType name="PartyType">
    <xs:sequence>
      <xs:element name="Name" type="xs:string"/>
      <xs:element name="Address" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>

  <!-- InvoiceLine type -->
  <xs:complexType name="InvoiceLineType">
    <xs:sequence>
      <xs:element name="ItemName" type="xs:string"/>
      <xs:element name="Quantity" type="xs:positiveInteger"/>
      <xs:element name="LineAmount" type="AmountType"/>
    </xs:sequence>
  </xs:complexType>

  <!-- InvoiceLines container -->
  <xs:complexType name="InvoiceLinesType">
    <xs:sequence>
      <xs:element name="InvoiceLine" type="InvoiceLineType"
                  minOccurs="1" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <!-- MonetaryTotal type -->
  <xs:complexType name="MonetaryTotalType">
    <xs:sequence>
      <xs:element name="LineExtensionAmount" type="AmountType"/>
      <xs:element name="TaxAmount" type="AmountType"/>
      <xs:element name="PayableAmount" type="AmountType"/>
    </xs:sequence>
  </xs:complexType>

  <!-- PaymentMeans type -->
  <xs:complexType name="PaymentMeansType">
    <xs:sequence>
      <xs:element name="PaymentMethodCode" type="PaymentMethodCodeType"/>
      <xs:element name="PaymentDueDate" type="xs:date"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Root element: Invoice -->
  <xs:element name="Invoice">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="InvoiceNumber" type="xs:string"/>
        <xs:element name="IssueDate" type="xs:date"/>
        <xs:element name="Supplier" type="PartyType"/>
        <xs:element name="Customer" type="PartyType"/>
        <xs:element name="InvoiceLines" type="InvoiceLinesType"/>
        <xs:element name="MonetaryTotal" type="MonetaryTotalType"/>
        <xs:element name="PaymentMeans" type="PaymentMeansType"
                    minOccurs="0" maxOccurs="unbounded"/>
        <xs:element name="Note" type="xs:string"
                    minOccurs="0" maxOccurs="1"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
