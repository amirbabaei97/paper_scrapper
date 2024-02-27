
### Scoring Formula

Let's denote the variables as follows:

- \( CC \) = Citations Count (scaled between 1 and 9)
- \( JIF \) = Journal Impact Factor (scaled between 0 and 3)
- \( AS \) = Author's Score (as is, assuming it's already a composite score that can be directly used)
- \( PY \) = Publication Year (with the current year considered to make newer publications score higher)
- \( CPM \) = Cross-Platform Mentions (scaled between 1 and 3)
- \( PRS \) = Peer Review Status (0 or 1)

And the weights:

- \( w_{CC} = 0.2 \)
- \( w_{JIF} = 0.2 \)
- \( w_{AS} = 0.2 \)
- \( w_{PY} = -0.05 \)
- \( w_{CPM} = 0.2 \)
- \( w_{PRS} = 0.2 \)

You can see all of them in a tabular view:

| Factor                        | Updated Usual Range        | Proposed Weight |
| ----------------------------- | -------------------------- | --------------- |
| Citations Count (CC)          | 1 - 9                      | 0.2             |
| Journal Impact Factor (JIF)   | 0 - 3                      | 0.2             |
| Author's Score (AS)           | 0 - 100+ (composite score) | 0.2             |
| Publication Year (PY)         | 0 - 40                     | \-0.05          |
| Cross-Platform Mentions (CPM) | 1 - 3                      | 0.2             |
| Peer Review Status (PRS)      | 0 or 1                     | 0.2             |

The formula to calculate the score for each paper, \( S \), would be:

\[ S = w_{CC} \cdot \left(rac{CC - 1}{8}
ight) + w_{JIF} \cdot \left(rac{JIF}{3}
ight) + w_{AS} \cdot \left(rac{AS}{100}
ight) + w_{PY} \cdot \left(1 - rac{CurrentYear - PY}{40}
ight) + w_{CPM} \cdot \left(rac{CPM - 1}{2}
ight) + w_{PRS} \cdot PRS \]

### Explanation
We tried to assign a weight to each of the variables based on the the disturibution patterns of the variables. Thus these values might need improvement, please create an issue and suggest better weights or update a common range of a variable.(A good source is usually required.) You don't have to necessarily update the code. 