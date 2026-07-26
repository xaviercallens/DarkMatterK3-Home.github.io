# Synthetic Null-Variance Scan (SYNTHETIC Mock Data)

**ALL VALUES IN THIS REPORT ARE SYNTHETIC MOCK DATA — NOT A CLAIM ABOUT ANY REAL SURVEY.**

Engineering-only synthetic sanity check of the null-randomization infrastructure.

## Seed 1

### nbins=4

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        1 |      1.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        1 |      1.00 |     0.00 | N/A (no variance) |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        0 |      1.60 |     1.14 | 13.3%      |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.03 |     0.18 | 96.7%      |
| density_shuffle      |        0 |      0.00 |     0.00 | N/A (no variance) |

### nbins=8

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.03 |     0.18 | 96.7%      |
| z_shuffle            |        1 |      1.07 |     0.25 | 93.3%      |
| density_shuffle      |        1 |      1.50 |     0.72 | 63.3%      |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        8 |      0.70 |     0.74 | 100.0%     |
| z_shuffle            |        8 |      1.93 |     1.69 | 100.0%     |
| density_shuffle      |        8 |     34.97 |     4.48 | 0.0%       |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        2 |      3.57 |     1.54 | 26.7%      |
| z_shuffle            |        2 |      5.23 |     2.32 | 13.3%      |
| density_shuffle      |        2 |      0.30 |     0.46 | 100.0%     |

### nbins=16

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        4 |      3.40 |     0.92 | 90.0%      |
| z_shuffle            |        4 |      9.63 |     3.45 | 3.3%       |
| density_shuffle      |        4 |     45.93 |     5.59 | 0.0%       |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |      115 |     96.70 |    10.48 | 96.7%      |
| z_shuffle            |      115 |     73.17 |     8.48 | 100.0%     |
| density_shuffle      |      115 |     45.73 |     8.40 | 100.0%     |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      7.87 |     2.60 | 0.0%       |
| z_shuffle            |        0 |      0.73 |     0.93 | 53.3%      |
| density_shuffle      |        0 |      0.00 |     0.00 | N/A (no variance) |

## Seed 2

### nbins=4

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        1 |      1.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        1 |      1.03 |     0.18 | 96.7%      |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        0 |      2.00 |     1.37 | 16.7%      |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        0 |      0.07 |     0.25 | 93.3%      |

### nbins=8

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.03 |     0.18 | 96.7%      |
| z_shuffle            |        1 |      1.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        1 |      1.83 |     0.69 | 33.3%      |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |       10 |      0.87 |     0.85 | 100.0%     |
| z_shuffle            |       10 |      1.43 |     1.28 | 100.0%     |
| density_shuffle      |       10 |     31.13 |     4.96 | 0.0%       |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        4 |      2.33 |     1.49 | 90.0%      |
| z_shuffle            |        4 |      2.97 |     1.52 | 83.3%      |
| density_shuffle      |        4 |      0.23 |     0.50 | 100.0%     |

### nbins=16

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        8 |      3.67 |     1.89 | 96.7%      |
| z_shuffle            |        8 |     10.70 |     2.72 | 16.7%      |
| density_shuffle      |        8 |     48.80 |     6.10 | 0.0%       |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |       97 |     74.73 |     8.60 | 100.0%     |
| z_shuffle            |       97 |     78.70 |     8.01 | 100.0%     |
| density_shuffle      |       97 |     42.00 |     6.73 | 100.0%     |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |     23.30 |     4.85 | 0.0%       |
| z_shuffle            |        0 |      1.00 |     0.89 | 30.0%      |
| density_shuffle      |        0 |      0.07 |     0.25 | 93.3%      |

## Seed 3

### nbins=4

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        1 |      1.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        1 |      1.03 |     0.18 | 96.7%      |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        0 |      1.97 |     1.28 | 16.7%      |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |      0.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        0 |      0.00 |     0.00 | N/A (no variance) |
| density_shuffle      |        0 |      0.00 |     0.00 | N/A (no variance) |

### nbins=8

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        1 |      1.00 |     0.00 | N/A (no variance) |
| z_shuffle            |        1 |      1.03 |     0.18 | 96.7%      |
| density_shuffle      |        1 |      1.60 |     0.71 | 53.3%      |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        4 |      0.60 |     0.92 | 100.0%     |
| z_shuffle            |        4 |      2.33 |     1.45 | 90.0%      |
| density_shuffle      |        4 |     34.73 |     5.59 | 0.0%       |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        4 |      1.77 |     0.99 | 100.0%     |
| z_shuffle            |        4 |      3.00 |     1.57 | 83.3%      |
| density_shuffle      |        4 |      0.10 |     0.30 | 100.0%     |

### nbins=16

#### beta_0

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |       10 |      4.93 |     1.59 | 100.0%     |
| z_shuffle            |       10 |     14.63 |     2.83 | 6.7%       |
| density_shuffle      |       10 |     47.10 |     6.58 | 0.0%       |

#### beta_1

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |      133 |     89.47 |     9.75 | 100.0%     |
| z_shuffle            |      133 |     65.40 |     8.05 | 100.0%     |
| density_shuffle      |      133 |     46.60 |     7.57 | 100.0%     |

#### beta_2

| Scheme | Observed | Null Mean | Null Std | Percentile |
|--------|----------|-----------|----------|------------|
| csr                  |        0 |     23.00 |     3.95 | 0.0%       |
| z_shuffle            |        0 |      2.30 |     1.53 | 20.0%      |
| density_shuffle      |        0 |      0.03 |     0.18 | 96.7%      |
