
### Question 1(e):

**Which parameter setting for the tool is likely to be best (in the sense that I spend the least time on the task)?**

#### Problem Context:
- Total Archive Size: 50,000 items.
- Relevant Items: 30 items.
- Manual Time to Find Each Relevant Item (if missed): 15 minutes.
- Time Wasted on Each False Positive: 0.5 minutes (30 seconds).

**Answer: i. Just right of the center of the graph, where precision goes up again.**

**Detailed Explanation and Working:**

#### Choice-by-Choice Analysis:

1. **Option i: Just right of the center (80% precision, 90% recall):**
    - **Calculations:**
      - False Negatives: \( (1 - 0.90) \times 30 = 3 \)
      - False Positives: \( \frac{30 \times (1 - 0.80)}{0.80} = 8 \)
      - Total Time: 49 minutes.

2. **Option ii: To the right (68% precision, 90% recall):**
    - **Calculations:**
      - False Negatives: 3
      - False Positives: 14
      - Total Time: 52 minutes.

3. **Option iii: Manual search (100% recall):**
    - **Calculations:**
      - Irrelevant Items: 49,970 × 0.5 minutes
      - Total Time: 25,435 minutes.

4. **Option iv: To the left (100% precision, 17% recall):**
    - **Calculations:**
      - False Negatives: 25
      - Total Time: 450 minutes.

5. **Option v: To the left (100% precision, 17% recall with 30 seconds/item):**
    - **Calculations:**
      - False Negatives: 25
      - Total Time: 88 minutes.

**Conclusion:**
- Option (i) has the lowest time (49 minutes) and is the most efficient.

**Real-World Example:**
In search engines, balancing precision and recall helps users find the most relevant results without wasting time on irrelevant ones.

**Common Pitfalls:**
- Focusing solely on either precision or recall can lead to inefficiency.
- Misunderstanding how false positives and false negatives affect total time.

**Important Point to Remember:**
- Always consider the trade-offs between precision and recall when optimizing information retrieval tasks.
