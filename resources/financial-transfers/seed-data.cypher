// =============================================
// Financial Transfers Fraud Detection Network
// Chapter 10 — Property Graphs Dataset
// =============================================
//
// Dataset statistics:
//   Nodes:         60  (:Account)
//   Relationships: 150 (:TRANSFERRED_TO)
//   Account types: Personal (31), Business (19), Merchant (9), Processor (1)
//                  (4 types: Personal, Business, Merchant, Processor)
//   Flagged:       1   (acct_2049 — Alice Chen)
//   Supernode:     processor_001 (QuickPay Hub) — 42 total edges (19 in, 23 out)
//   Fraud rings:   2
//     Ring 1 (length 3): acct_2049 → acct_3017 → acct_7801 → acct_2049
//     Ring 2 (length 4): acct_5566 → acct_1234 → acct_5678 → acct_9012 → acct_5566
//   Date range:    2024-01-05 through 2024-03-18
//   Transfer types: wire, ACH, card, crypto
//
// Format: One continuous query (no semicolons between CREATE clauses).
//         All node variables remain in scope for relationship creation.
//
// =============================================


// ---------------------------------------------
// Section 1: Core accounts (11 nodes)
// These appear in the worked example, fraud rings, and key queries.
// ---------------------------------------------

CREATE (a1:Account {id: 'acct_2049', name: 'Alice Chen', type: 'Personal', flagged: true})
CREATE (a2:Account {id: 'acct_3017', name: 'Bob Rivera', type: 'Business', flagged: false})
CREATE (a3:Account {id: 'acct_4522', name: 'Carla Diaz', type: 'Personal', flagged: false})
CREATE (a4:Account {id: 'acct_7801', name: 'David Okonkwo', type: 'Personal', flagged: false})
CREATE (a5:Account {id: 'acct_9900', name: 'Elena Rossi', type: 'Business', flagged: false})
CREATE (a6:Account {id: 'acct_5566', name: 'Frank Yamada', type: 'Personal', flagged: false})
CREATE (a7:Account {id: 'acct_8800', name: 'Grace Lin', type: 'Merchant', flagged: false})
CREATE (p1:Account {id: 'processor_001', name: 'QuickPay Hub', type: 'Processor', flagged: false})
CREATE (a8:Account {id: 'acct_1234', name: 'Hiro Tanaka', type: 'Personal', flagged: false})
CREATE (a9:Account {id: 'acct_5678', name: 'Isabella Moreno', type: 'Business', flagged: false})
CREATE (a10:Account {id: 'acct_9012', name: 'James Kim', type: 'Personal', flagged: false})


// ---------------------------------------------
// Section 2: Additional accounts (49 nodes)
// Varied types and realistic names to reach ~60 total.
// ---------------------------------------------

CREATE (a11:Account {id: 'acct_1001', name: 'Kenji Watanabe', type: 'Personal', flagged: false})
CREATE (a12:Account {id: 'acct_1002', name: 'Maria Santos', type: 'Personal', flagged: false})
CREATE (a13:Account {id: 'acct_1003', name: 'Omar Hassan', type: 'Business', flagged: false})
CREATE (a14:Account {id: 'acct_1004', name: 'Priya Sharma', type: 'Personal', flagged: false})
CREATE (a15:Account {id: 'acct_1005', name: 'Liam Byrne', type: 'Business', flagged: false})
CREATE (a16:Account {id: 'acct_1006', name: 'Sofia Petrov', type: 'Personal', flagged: false})
CREATE (a17:Account {id: 'acct_1007', name: 'Marcus Johnson', type: 'Personal', flagged: false})
CREATE (a18:Account {id: 'acct_1008', name: 'Aisha Bakari', type: 'Business', flagged: false})
CREATE (a19:Account {id: 'acct_1009', name: 'Chen Wei', type: 'Merchant', flagged: false})
CREATE (a20:Account {id: 'acct_1010', name: 'Yuki Nakamura', type: 'Personal', flagged: false})
CREATE (a21:Account {id: 'acct_1011', name: 'Diego Fernandez', type: 'Business', flagged: false})
CREATE (a22:Account {id: 'acct_1012', name: 'Fatima Al-Rashid', type: 'Personal', flagged: false})
CREATE (a23:Account {id: 'acct_1013', name: 'Lucas Bergman', type: 'Merchant', flagged: false})
CREATE (a24:Account {id: 'acct_1014', name: 'Nadia Kowalski', type: 'Personal', flagged: false})
CREATE (a25:Account {id: 'acct_1015', name: 'Raj Patel', type: 'Business', flagged: false})
CREATE (a26:Account {id: 'acct_1016', name: 'Emma Johansson', type: 'Personal', flagged: false})
CREATE (a27:Account {id: 'acct_1017', name: 'Tomas Herrera', type: 'Business', flagged: false})
CREATE (a28:Account {id: 'acct_1018', name: 'Leila Ahmadi', type: 'Personal', flagged: false})
CREATE (a29:Account {id: 'acct_1019', name: 'Viktor Novak', type: 'Merchant', flagged: false})
CREATE (a30:Account {id: 'acct_1020', name: 'Sonia Delgado', type: 'Personal', flagged: false})
CREATE (a31:Account {id: 'acct_1021', name: 'Andrei Volkov', type: 'Business', flagged: false})
CREATE (a32:Account {id: 'acct_1022', name: 'Hannah Mueller', type: 'Personal', flagged: false})
CREATE (a33:Account {id: 'acct_1023', name: 'Kwame Asante', type: 'Business', flagged: false})
CREATE (a34:Account {id: 'acct_1024', name: 'Mei-Ling Chang', type: 'Merchant', flagged: false})
CREATE (a35:Account {id: 'acct_1025', name: 'Patrick Brennan', type: 'Personal', flagged: false})
CREATE (a36:Account {id: 'acct_1026', name: 'Zara Ibrahim', type: 'Business', flagged: false})
CREATE (a37:Account {id: 'acct_1027', name: 'Lars Eriksson', type: 'Personal', flagged: false})
CREATE (a38:Account {id: 'acct_1028', name: 'Camila Rojas', type: 'Personal', flagged: false})
CREATE (a39:Account {id: 'acct_1029', name: 'Dmitri Kuznetsov', type: 'Business', flagged: false})
CREATE (a40:Account {id: 'acct_1030', name: 'Amara Osei', type: 'Personal', flagged: false})
CREATE (a41:Account {id: 'acct_1031', name: 'Riku Takahashi', type: 'Merchant', flagged: false})
CREATE (a42:Account {id: 'acct_1032', name: 'Nina Ivanova', type: 'Personal', flagged: false})
CREATE (a43:Account {id: 'acct_1033', name: 'Oscar Lindqvist', type: 'Business', flagged: false})
CREATE (a44:Account {id: 'acct_1034', name: 'Gabriela Lima', type: 'Personal', flagged: false})
CREATE (a45:Account {id: 'acct_1035', name: 'Samuel Oduya', type: 'Personal', flagged: false})
CREATE (a46:Account {id: 'acct_1036', name: 'Clara Hoffmann', type: 'Business', flagged: false})
CREATE (a47:Account {id: 'acct_1037', name: 'Tariq Mahmoud', type: 'Personal', flagged: false})
CREATE (a48:Account {id: 'acct_1038', name: 'Eva Sundstrom', type: 'Merchant', flagged: false})
CREATE (a49:Account {id: 'acct_1039', name: 'Jean-Pierre Dubois', type: 'Business', flagged: false})
CREATE (a50:Account {id: 'acct_1040', name: 'Mina Park', type: 'Personal', flagged: false})
CREATE (a51:Account {id: 'acct_1041', name: 'Roberto Conti', type: 'Merchant', flagged: false})
CREATE (a52:Account {id: 'acct_1042', name: 'Ingrid Larsen', type: 'Personal', flagged: false})
CREATE (a53:Account {id: 'acct_1043', name: 'Daniel Okafor', type: 'Business', flagged: false})
CREATE (a54:Account {id: 'acct_1044', name: 'Ana Vasquez', type: 'Personal', flagged: false})
CREATE (a55:Account {id: 'acct_1045', name: 'William Cheng', type: 'Personal', flagged: false})
CREATE (a56:Account {id: 'acct_1046', name: 'Svetlana Popov', type: 'Business', flagged: false})
CREATE (a57:Account {id: 'acct_1047', name: 'Ibrahim Diallo', type: 'Personal', flagged: false})
CREATE (a58:Account {id: 'acct_1048', name: 'Rachel Cohen', type: 'Merchant', flagged: false})
CREATE (a59:Account {id: 'acct_1049', name: 'Hiroshi Yamamoto', type: 'Business', flagged: false})


// ---------------------------------------------
// Section 3: Core transfers — worked example subgraph (9 edges)
// This 9-edge subgraph is traced in the chapter narrative.
// Every amount, date, and transfer_type must match exactly.
// ---------------------------------------------

// acct_2049 → acct_3017: $8K wire (Alice to Bob)
CREATE (a1)-[:TRANSFERRED_TO {amount: 8000, date: date('2024-03-01'), transfer_type: 'wire'}]->(a2)
// acct_2049 → acct_4522: $3K ACH (Alice to Carla — filtered out by $5K threshold)
CREATE (a1)-[:TRANSFERRED_TO {amount: 3000, date: date('2024-02-15'), transfer_type: 'ACH'}]->(a3)
// acct_3017 → acct_7801: $12K wire (Bob to David)
CREATE (a2)-[:TRANSFERRED_TO {amount: 12000, date: date('2024-03-05'), transfer_type: 'wire'}]->(a4)
// acct_3017 → acct_9900: $2K ACH (Bob to Elena — filtered out by $5K threshold)
CREATE (a2)-[:TRANSFERRED_TO {amount: 2000, date: date('2024-01-10'), transfer_type: 'ACH'}]->(a5)
// acct_4522 → processor_001: $6K card (Carla to QuickPay Hub)
CREATE (a3)-[:TRANSFERRED_TO {amount: 6000, date: date('2024-03-10'), transfer_type: 'card'}]->(p1)
// processor_001 → acct_7801: $15K wire (QuickPay Hub to David)
CREATE (p1)-[:TRANSFERRED_TO {amount: 15000, date: date('2024-03-12'), transfer_type: 'wire'}]->(a4)
// processor_001 → acct_5566: $9K wire (QuickPay Hub to Frank)
CREATE (p1)-[:TRANSFERRED_TO {amount: 9000, date: date('2024-03-14'), transfer_type: 'wire'}]->(a6)
// processor_001 → acct_8800: $1K ACH (QuickPay Hub to Grace)
CREATE (p1)-[:TRANSFERRED_TO {amount: 1000, date: date('2024-02-01'), transfer_type: 'ACH'}]->(a7)
// acct_7801 → acct_2049: $7K wire (David to Alice — CLOSES FRAUD RING 1)
CREATE (a4)-[:TRANSFERRED_TO {amount: 7000, date: date('2024-03-08'), transfer_type: 'wire'}]->(a1)


// ---------------------------------------------
// Section 4: Fraud ring 2 transfers (4 edges)
// Ring of length 4: acct_5566 → acct_1234 → acct_5678 → acct_9012 → acct_5566
// All transfers exceed $3,000 (detectable by cycle queries with amount > 3000).
// ---------------------------------------------

// acct_5566 → acct_1234: $6K wire (Frank to Hiro)
CREATE (a6)-[:TRANSFERRED_TO {amount: 6000, date: date('2024-02-20'), transfer_type: 'wire'}]->(a8)
// acct_1234 → acct_5678: $5.5K wire (Hiro to Isabella)
CREATE (a8)-[:TRANSFERRED_TO {amount: 5500, date: date('2024-02-25'), transfer_type: 'wire'}]->(a9)
// acct_5678 → acct_9012: $4.5K ACH (Isabella to James)
CREATE (a9)-[:TRANSFERRED_TO {amount: 4500, date: date('2024-03-01'), transfer_type: 'ACH'}]->(a10)
// acct_9012 → acct_5566: $4K wire (James to Frank — CLOSES FRAUD RING 2)
CREATE (a10)-[:TRANSFERRED_TO {amount: 4000, date: date('2024-03-05'), transfer_type: 'wire'}]->(a6)


// ---------------------------------------------
// Section 5: Supernode transfers — processor_001 (38 edges)
// These bring processor_001 (QuickPay Hub) to 42 total edges
// (19 incoming + 23 outgoing), making it the dataset's supernode.
// Combined with the 4 edges in Section 3:
//   Incoming: 1 (Section 3) + 18 (below) = 19
//   Outgoing: 3 (Section 3) + 20 (below) = 23
// ---------------------------------------------

// --- Incoming to processor_001 (18 edges) ---
CREATE (a11)-[:TRANSFERRED_TO {amount: 4200, date: date('2024-01-15'), transfer_type: 'card'}]->(p1)
CREATE (a12)-[:TRANSFERRED_TO {amount: 7800, date: date('2024-02-03'), transfer_type: 'wire'}]->(p1)
CREATE (a13)-[:TRANSFERRED_TO {amount: 2500, date: date('2024-01-22'), transfer_type: 'ACH'}]->(p1)
CREATE (a14)-[:TRANSFERRED_TO {amount: 9100, date: date('2024-03-08'), transfer_type: 'wire'}]->(p1)
CREATE (a15)-[:TRANSFERRED_TO {amount: 1800, date: date('2024-02-14'), transfer_type: 'card'}]->(p1)
CREATE (a16)-[:TRANSFERRED_TO {amount: 5300, date: date('2024-01-28'), transfer_type: 'ACH'}]->(p1)
CREATE (a17)-[:TRANSFERRED_TO {amount: 3600, date: date('2024-03-02'), transfer_type: 'card'}]->(p1)
CREATE (a18)-[:TRANSFERRED_TO {amount: 11200, date: date('2024-02-18'), transfer_type: 'wire'}]->(p1)
CREATE (a19)-[:TRANSFERRED_TO {amount: 850, date: date('2024-01-10'), transfer_type: 'card'}]->(p1)
CREATE (a20)-[:TRANSFERRED_TO {amount: 6700, date: date('2024-03-12'), transfer_type: 'wire'}]->(p1)
CREATE (a21)-[:TRANSFERRED_TO {amount: 2900, date: date('2024-02-08'), transfer_type: 'ACH'}]->(p1)
CREATE (a22)-[:TRANSFERRED_TO {amount: 4500, date: date('2024-01-18'), transfer_type: 'card'}]->(p1)
CREATE (a23)-[:TRANSFERRED_TO {amount: 8300, date: date('2024-03-05'), transfer_type: 'wire'}]->(p1)
CREATE (a24)-[:TRANSFERRED_TO {amount: 1600, date: date('2024-02-22'), transfer_type: 'crypto'}]->(p1)
CREATE (a25)-[:TRANSFERRED_TO {amount: 5900, date: date('2024-01-05'), transfer_type: 'ACH'}]->(p1)
CREATE (a26)-[:TRANSFERRED_TO {amount: 3200, date: date('2024-03-15'), transfer_type: 'card'}]->(p1)
CREATE (a27)-[:TRANSFERRED_TO {amount: 10500, date: date('2024-02-10'), transfer_type: 'wire'}]->(p1)
CREATE (a28)-[:TRANSFERRED_TO {amount: 7400, date: date('2024-01-25'), transfer_type: 'ACH'}]->(p1)

// --- Outgoing from processor_001 (20 edges) ---
CREATE (p1)-[:TRANSFERRED_TO {amount: 3800, date: date('2024-02-05'), transfer_type: 'wire'}]->(a29)
CREATE (p1)-[:TRANSFERRED_TO {amount: 6200, date: date('2024-01-20'), transfer_type: 'ACH'}]->(a30)
CREATE (p1)-[:TRANSFERRED_TO {amount: 11800, date: date('2024-03-10'), transfer_type: 'wire'}]->(a31)
CREATE (p1)-[:TRANSFERRED_TO {amount: 2400, date: date('2024-02-15'), transfer_type: 'card'}]->(a32)
CREATE (p1)-[:TRANSFERRED_TO {amount: 8900, date: date('2024-01-12'), transfer_type: 'wire'}]->(a33)
CREATE (p1)-[:TRANSFERRED_TO {amount: 1500, date: date('2024-03-02'), transfer_type: 'card'}]->(a34)
CREATE (p1)-[:TRANSFERRED_TO {amount: 5700, date: date('2024-02-20'), transfer_type: 'ACH'}]->(a35)
CREATE (p1)-[:TRANSFERRED_TO {amount: 9400, date: date('2024-01-28'), transfer_type: 'wire'}]->(a36)
CREATE (p1)-[:TRANSFERRED_TO {amount: 3100, date: date('2024-03-08'), transfer_type: 'crypto'}]->(a37)
CREATE (p1)-[:TRANSFERRED_TO {amount: 7600, date: date('2024-02-12'), transfer_type: 'wire'}]->(a38)
CREATE (p1)-[:TRANSFERRED_TO {amount: 4300, date: date('2024-01-18'), transfer_type: 'ACH'}]->(a39)
CREATE (p1)-[:TRANSFERRED_TO {amount: 12500, date: date('2024-03-14'), transfer_type: 'wire'}]->(a40)
CREATE (p1)-[:TRANSFERRED_TO {amount: 2100, date: date('2024-02-02'), transfer_type: 'card'}]->(a41)
CREATE (p1)-[:TRANSFERRED_TO {amount: 6800, date: date('2024-01-22'), transfer_type: 'wire'}]->(a42)
CREATE (p1)-[:TRANSFERRED_TO {amount: 950, date: date('2024-03-05'), transfer_type: 'card'}]->(a43)
CREATE (p1)-[:TRANSFERRED_TO {amount: 5400, date: date('2024-02-18'), transfer_type: 'ACH'}]->(a44)
CREATE (p1)-[:TRANSFERRED_TO {amount: 8100, date: date('2024-01-08'), transfer_type: 'wire'}]->(a45)
CREATE (p1)-[:TRANSFERRED_TO {amount: 3500, date: date('2024-03-12'), transfer_type: 'crypto'}]->(a46)
CREATE (p1)-[:TRANSFERRED_TO {amount: 10200, date: date('2024-02-25'), transfer_type: 'wire'}]->(a47)
CREATE (p1)-[:TRANSFERRED_TO {amount: 1300, date: date('2024-01-15'), transfer_type: 'card'}]->(a48)


// ---------------------------------------------
// Section 6: General transfers (99 edges)
// These fill out the network to ~150 total relationships.
// Varied amounts, dates, and transfer types across all accounts.
// ---------------------------------------------

// --- 6a: Core account interconnections (15 edges) ---
// Transfers among the 11 core accounts not covered above.
CREATE (a5)-[:TRANSFERRED_TO {amount: 4500, date: date('2024-01-20'), transfer_type: 'card'}]->(a7)
CREATE (a5)-[:TRANSFERRED_TO {amount: 7200, date: date('2024-02-10'), transfer_type: 'wire'}]->(a2)
CREATE (a4)-[:TRANSFERRED_TO {amount: 2800, date: date('2024-02-28'), transfer_type: 'ACH'}]->(a6)
CREATE (a7)-[:TRANSFERRED_TO {amount: 3200, date: date('2024-01-15'), transfer_type: 'card'}]->(a5)
CREATE (a8)-[:TRANSFERRED_TO {amount: 1500, date: date('2024-03-02'), transfer_type: 'ACH'}]->(a4)
CREATE (a9)-[:TRANSFERRED_TO {amount: 9500, date: date('2024-02-05'), transfer_type: 'wire'}]->(a2)
CREATE (a10)-[:TRANSFERRED_TO {amount: 2200, date: date('2024-01-25'), transfer_type: 'crypto'}]->(a8)
CREATE (a6)-[:TRANSFERRED_TO {amount: 11000, date: date('2024-03-10'), transfer_type: 'wire'}]->(a4)
CREATE (a1)-[:TRANSFERRED_TO {amount: 750, date: date('2024-01-08'), transfer_type: 'card'}]->(a7)
CREATE (a2)-[:TRANSFERRED_TO {amount: 5500, date: date('2024-02-18'), transfer_type: 'ACH'}]->(a5)
CREATE (a4)-[:TRANSFERRED_TO {amount: 8200, date: date('2024-03-15'), transfer_type: 'wire'}]->(a9)
CREATE (a10)-[:TRANSFERRED_TO {amount: 3100, date: date('2024-02-12'), transfer_type: 'ACH'}]->(a1)
CREATE (a3)-[:TRANSFERRED_TO {amount: 1800, date: date('2024-01-30'), transfer_type: 'card'}]->(a8)
CREATE (a9)-[:TRANSFERRED_TO {amount: 6700, date: date('2024-03-08'), transfer_type: 'wire'}]->(a10)
CREATE (a7)-[:TRANSFERRED_TO {amount: 2400, date: date('2024-02-22'), transfer_type: 'card'}]->(a6)

// --- 6b: Transfers among additional accounts (25 edges) ---
CREATE (a11)-[:TRANSFERRED_TO {amount: 3500, date: date('2024-01-05'), transfer_type: 'ACH'}]->(a12)
CREATE (a13)-[:TRANSFERRED_TO {amount: 8200, date: date('2024-02-12'), transfer_type: 'wire'}]->(a14)
CREATE (a15)-[:TRANSFERRED_TO {amount: 1200, date: date('2024-01-18'), transfer_type: 'card'}]->(a16)
CREATE (a17)-[:TRANSFERRED_TO {amount: 6700, date: date('2024-03-02'), transfer_type: 'wire'}]->(a18)
CREATE (a19)-[:TRANSFERRED_TO {amount: 950, date: date('2024-02-08'), transfer_type: 'card'}]->(a20)
CREATE (a21)-[:TRANSFERRED_TO {amount: 4300, date: date('2024-01-22'), transfer_type: 'ACH'}]->(a22)
CREATE (a23)-[:TRANSFERRED_TO {amount: 7800, date: date('2024-03-10'), transfer_type: 'wire'}]->(a24)
CREATE (a25)-[:TRANSFERRED_TO {amount: 2100, date: date('2024-02-15'), transfer_type: 'crypto'}]->(a26)
CREATE (a27)-[:TRANSFERRED_TO {amount: 5600, date: date('2024-01-28'), transfer_type: 'ACH'}]->(a28)
CREATE (a29)-[:TRANSFERRED_TO {amount: 3900, date: date('2024-03-05'), transfer_type: 'card'}]->(a30)
CREATE (a31)-[:TRANSFERRED_TO {amount: 11500, date: date('2024-02-20'), transfer_type: 'wire'}]->(a32)
CREATE (a33)-[:TRANSFERRED_TO {amount: 1800, date: date('2024-01-12'), transfer_type: 'card'}]->(a34)
CREATE (a35)-[:TRANSFERRED_TO {amount: 9200, date: date('2024-03-15'), transfer_type: 'wire'}]->(a36)
CREATE (a37)-[:TRANSFERRED_TO {amount: 2700, date: date('2024-02-02'), transfer_type: 'ACH'}]->(a38)
CREATE (a39)-[:TRANSFERRED_TO {amount: 6100, date: date('2024-01-25'), transfer_type: 'wire'}]->(a40)
CREATE (a41)-[:TRANSFERRED_TO {amount: 4500, date: date('2024-03-08'), transfer_type: 'card'}]->(a42)
CREATE (a43)-[:TRANSFERRED_TO {amount: 8900, date: date('2024-02-18'), transfer_type: 'wire'}]->(a44)
CREATE (a45)-[:TRANSFERRED_TO {amount: 1500, date: date('2024-01-15'), transfer_type: 'ACH'}]->(a46)
CREATE (a47)-[:TRANSFERRED_TO {amount: 3200, date: date('2024-03-12'), transfer_type: 'crypto'}]->(a48)
CREATE (a49)-[:TRANSFERRED_TO {amount: 7400, date: date('2024-02-25'), transfer_type: 'wire'}]->(a50)
CREATE (a51)-[:TRANSFERRED_TO {amount: 2800, date: date('2024-01-08'), transfer_type: 'card'}]->(a52)
CREATE (a53)-[:TRANSFERRED_TO {amount: 5300, date: date('2024-03-01'), transfer_type: 'ACH'}]->(a54)
CREATE (a55)-[:TRANSFERRED_TO {amount: 10200, date: date('2024-02-10'), transfer_type: 'wire'}]->(a56)
CREATE (a57)-[:TRANSFERRED_TO {amount: 1900, date: date('2024-01-20'), transfer_type: 'card'}]->(a58)
CREATE (a59)-[:TRANSFERRED_TO {amount: 4700, date: date('2024-03-18'), transfer_type: 'ACH'}]->(a11)

// --- 6c: Transfers between core and additional accounts (25 edges) ---
CREATE (a1)-[:TRANSFERRED_TO {amount: 2500, date: date('2024-01-12'), transfer_type: 'ACH'}]->(a11)
CREATE (a1)-[:TRANSFERRED_TO {amount: 4200, date: date('2024-02-28'), transfer_type: 'wire'}]->(a14)
CREATE (a2)-[:TRANSFERRED_TO {amount: 7500, date: date('2024-01-20'), transfer_type: 'wire'}]->(a13)
CREATE (a2)-[:TRANSFERRED_TO {amount: 3800, date: date('2024-03-05'), transfer_type: 'ACH'}]->(a15)
CREATE (a3)-[:TRANSFERRED_TO {amount: 1600, date: date('2024-02-08'), transfer_type: 'card'}]->(a17)
CREATE (a4)-[:TRANSFERRED_TO {amount: 9300, date: date('2024-03-12'), transfer_type: 'wire'}]->(a21)
CREATE (a5)-[:TRANSFERRED_TO {amount: 5100, date: date('2024-01-28'), transfer_type: 'ACH'}]->(a25)
CREATE (a6)-[:TRANSFERRED_TO {amount: 2900, date: date('2024-02-15'), transfer_type: 'card'}]->(a19)
CREATE (a7)-[:TRANSFERRED_TO {amount: 4800, date: date('2024-03-02'), transfer_type: 'card'}]->(a23)
CREATE (a8)-[:TRANSFERRED_TO {amount: 6200, date: date('2024-01-15'), transfer_type: 'wire'}]->(a27)
CREATE (a9)-[:TRANSFERRED_TO {amount: 8100, date: date('2024-02-22'), transfer_type: 'wire'}]->(a31)
CREATE (a10)-[:TRANSFERRED_TO {amount: 3400, date: date('2024-03-08'), transfer_type: 'ACH'}]->(a35)
CREATE (a11)-[:TRANSFERRED_TO {amount: 1200, date: date('2024-02-05'), transfer_type: 'card'}]->(a1)
CREATE (a16)-[:TRANSFERRED_TO {amount: 5800, date: date('2024-01-25'), transfer_type: 'wire'}]->(a2)
CREATE (a20)-[:TRANSFERRED_TO {amount: 2700, date: date('2024-03-10'), transfer_type: 'ACH'}]->(a3)
CREATE (a24)-[:TRANSFERRED_TO {amount: 7100, date: date('2024-02-18'), transfer_type: 'wire'}]->(a4)
CREATE (a28)-[:TRANSFERRED_TO {amount: 4400, date: date('2024-01-08'), transfer_type: 'ACH'}]->(a5)
CREATE (a32)-[:TRANSFERRED_TO {amount: 3600, date: date('2024-03-15'), transfer_type: 'crypto'}]->(a6)
CREATE (a36)-[:TRANSFERRED_TO {amount: 8500, date: date('2024-02-02'), transfer_type: 'wire'}]->(a7)
CREATE (a40)-[:TRANSFERRED_TO {amount: 1900, date: date('2024-01-22'), transfer_type: 'card'}]->(a8)
CREATE (a44)-[:TRANSFERRED_TO {amount: 6300, date: date('2024-03-05'), transfer_type: 'wire'}]->(a9)
CREATE (a48)-[:TRANSFERRED_TO {amount: 5200, date: date('2024-02-12'), transfer_type: 'ACH'}]->(a10)
CREATE (a52)-[:TRANSFERRED_TO {amount: 2100, date: date('2024-03-18'), transfer_type: 'card'}]->(a1)
CREATE (a56)-[:TRANSFERRED_TO {amount: 9700, date: date('2024-01-30'), transfer_type: 'wire'}]->(a2)
CREATE (a50)-[:TRANSFERRED_TO {amount: 3300, date: date('2024-02-25'), transfer_type: 'ACH'}]->(a4)

// --- 6d: Chain and cluster transfers (34 edges) ---
// These create longer traversal paths and interconnections.
CREATE (a12)-[:TRANSFERRED_TO {amount: 4100, date: date('2024-02-05'), transfer_type: 'ACH'}]->(a13)
CREATE (a14)-[:TRANSFERRED_TO {amount: 7600, date: date('2024-03-01'), transfer_type: 'wire'}]->(a15)
CREATE (a16)-[:TRANSFERRED_TO {amount: 2300, date: date('2024-01-18'), transfer_type: 'card'}]->(a17)
CREATE (a18)-[:TRANSFERRED_TO {amount: 5800, date: date('2024-02-22'), transfer_type: 'wire'}]->(a19)
CREATE (a20)-[:TRANSFERRED_TO {amount: 3700, date: date('2024-03-08'), transfer_type: 'ACH'}]->(a21)
CREATE (a22)-[:TRANSFERRED_TO {amount: 6500, date: date('2024-01-12'), transfer_type: 'wire'}]->(a23)
CREATE (a24)-[:TRANSFERRED_TO {amount: 1400, date: date('2024-02-28'), transfer_type: 'card'}]->(a25)
CREATE (a26)-[:TRANSFERRED_TO {amount: 8300, date: date('2024-03-15'), transfer_type: 'wire'}]->(a27)
CREATE (a28)-[:TRANSFERRED_TO {amount: 4900, date: date('2024-01-25'), transfer_type: 'ACH'}]->(a29)
CREATE (a30)-[:TRANSFERRED_TO {amount: 7200, date: date('2024-02-10'), transfer_type: 'wire'}]->(a31)
CREATE (a32)-[:TRANSFERRED_TO {amount: 2600, date: date('2024-03-02'), transfer_type: 'crypto'}]->(a33)
CREATE (a34)-[:TRANSFERRED_TO {amount: 5100, date: date('2024-01-20'), transfer_type: 'card'}]->(a35)
CREATE (a36)-[:TRANSFERRED_TO {amount: 9800, date: date('2024-02-15'), transfer_type: 'wire'}]->(a37)
CREATE (a38)-[:TRANSFERRED_TO {amount: 3400, date: date('2024-03-10'), transfer_type: 'ACH'}]->(a39)
CREATE (a40)-[:TRANSFERRED_TO {amount: 6800, date: date('2024-01-28'), transfer_type: 'wire'}]->(a41)
CREATE (a42)-[:TRANSFERRED_TO {amount: 1700, date: date('2024-02-08'), transfer_type: 'card'}]->(a43)
CREATE (a44)-[:TRANSFERRED_TO {amount: 8400, date: date('2024-03-05'), transfer_type: 'wire'}]->(a45)
CREATE (a46)-[:TRANSFERRED_TO {amount: 4200, date: date('2024-01-15'), transfer_type: 'ACH'}]->(a47)
CREATE (a48)-[:TRANSFERRED_TO {amount: 7100, date: date('2024-02-20'), transfer_type: 'wire'}]->(a49)
CREATE (a50)-[:TRANSFERRED_TO {amount: 2500, date: date('2024-03-12'), transfer_type: 'card'}]->(a51)
CREATE (a52)-[:TRANSFERRED_TO {amount: 5900, date: date('2024-01-08'), transfer_type: 'ACH'}]->(a53)
CREATE (a54)-[:TRANSFERRED_TO {amount: 3800, date: date('2024-02-18'), transfer_type: 'wire'}]->(a55)
CREATE (a56)-[:TRANSFERRED_TO {amount: 6400, date: date('2024-03-01'), transfer_type: 'wire'}]->(a57)
CREATE (a58)-[:TRANSFERRED_TO {amount: 1100, date: date('2024-01-22'), transfer_type: 'card'}]->(a59)
CREATE (a11)-[:TRANSFERRED_TO {amount: 4600, date: date('2024-02-12'), transfer_type: 'ACH'}]->(a21)
CREATE (a13)-[:TRANSFERRED_TO {amount: 7900, date: date('2024-03-08'), transfer_type: 'wire'}]->(a23)
CREATE (a15)-[:TRANSFERRED_TO {amount: 2200, date: date('2024-01-05'), transfer_type: 'crypto'}]->(a25)
CREATE (a17)-[:TRANSFERRED_TO {amount: 5400, date: date('2024-02-25'), transfer_type: 'wire'}]->(a27)
CREATE (a19)-[:TRANSFERRED_TO {amount: 3100, date: date('2024-03-15'), transfer_type: 'card'}]->(a29)
CREATE (a33)-[:TRANSFERRED_TO {amount: 8700, date: date('2024-01-18'), transfer_type: 'wire'}]->(a43)
CREATE (a35)-[:TRANSFERRED_TO {amount: 1300, date: date('2024-02-08'), transfer_type: 'ACH'}]->(a45)
CREATE (a37)-[:TRANSFERRED_TO {amount: 6000, date: date('2024-03-02'), transfer_type: 'wire'}]->(a47)
CREATE (a39)-[:TRANSFERRED_TO {amount: 4500, date: date('2024-01-28'), transfer_type: 'ACH'}]->(a49)
CREATE (a41)-[:TRANSFERRED_TO {amount: 9100, date: date('2024-02-15'), transfer_type: 'wire'}]->(a51)
;
