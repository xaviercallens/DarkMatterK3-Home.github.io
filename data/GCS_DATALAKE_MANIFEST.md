# GCS Datalake Manifest — Cryptographic Audit Trail

**Generated:** 2026-08-01T11:19:14.643731Z
**Bucket:** `gs://socrateai-datalake-gen-lang-client-0625573011`
**Audited:** 1136 objects with full SHA-256 · **Present:** 41 objects (hashes not computed)
**Pending (not yet reached by any batch):** 0 · **Quarantined:** 2 · **Absent (retracted claims):** 4
✅ Full run — no PENDING objects remain.

---

## Status Vocabulary (Closed Set)

- **AUDITED**: Full SHA-256 hash computed on download; GCS-side MD5/CRC32C cross-checked.
- **PRESENT**: Object exists in bucket; hash not computed (exceeds 100 MB or not analysis-relevant).
- **PENDING**: Analysis-relevant, ≤100MB object not yet processed by any batch so far —
  status unknown, NOT the same as PRESENT (which means "checked, no hash needed").
- **QUARANTINED**: Object flagged for audit/review before use; remains in bucket untouched.
- **ABSENT**: Retracted from 2026-07-31 status table; does not exist in bucket.

⚠️ **Never emitted: "VERIFIED"** (reserved for human review only).

---

## By Folder


### audit/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `audit/euclid_q1_data_audit_certificate.md` | 0.01 | **AUDITED** | `b6bc57c6c9d14415...` | md5=`SP5Fw2AcG0R5etU/btQXXw==` crc32c=`nQk1jg==` |
| `audit/gcp_datalake_cartography.md` | 0.01 | **AUDITED** | `a55a177d7a0495d3...` | md5=`X/hTPtLp/InqJRJFELfC3g==` crc32c=`g0MfOA==` |

### checkpoints/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `checkpoints/run_20260729_074350_gen_0109.json` | 0.01 | **AUDITED** | `839b7c23a661ed4a...` | md5=`YEWBei6nkKVvMZQuyS3KMw==` crc32c=`e+ZX5A==` |
| `checkpoints/run_20260729_074350_gen_0015.json` | 0.01 | **AUDITED** | `e926b40620447b63...` | md5=`QcAtIbpwmDMlkXs3uaA64w==` crc32c=`Un/ZZg==` |
| `checkpoints/run_20260729_074350_gen_0239.json` | 0.01 | **AUDITED** | `82429210606a3d77...` | md5=`71R3wCK56PYksHl2zuYgIQ==` crc32c=`m4X9zA==` |
| `checkpoints/run_20260729_074350_gen_0242.json` | 0.01 | **AUDITED** | `901467caf40e57d3...` | md5=`PsQv8ywoIMfX5mKH7S6UOg==` crc32c=`rCrTtw==` |
| `checkpoints/run_20260729_074350_gen_0224.json` | 0.01 | **AUDITED** | `bb50918533f2f51d...` | md5=`7PPLbdASR0yfbEqMQhC8Gg==` crc32c=`we1SGg==` |
| `checkpoints/run_20260729_074350_gen_0218.json` | 0.01 | **AUDITED** | `47a335cf97ce47d0...` | md5=`Z652wDW4vQT2XPaCEZi8vA==` crc32c=`e5GjNQ==` |
| `checkpoints/run_20260729_074350_gen_0029.json` | 0.01 | **AUDITED** | `9703ac1bf0a80c67...` | md5=`cSj7zG23ib283CD9R18fgw==` crc32c=`uXDmcw==` |
| `checkpoints/run_20260729_074350_gen_0187.json` | 0.01 | **AUDITED** | `b79cf8e4ccace9d0...` | md5=`/o06PbhQOMqt+Rv0/1BVRg==` crc32c=`BVjdPQ==` |
| `checkpoints/run_20260729_074350_gen_0019.json` | 0.01 | **AUDITED** | `fd2cc033cd6df02d...` | md5=`rczwTnHnLR/hsBLrdnexAw==` crc32c=`3EunFw==` |
| `checkpoints/run_20260729_074350_gen_0255.json` | 0.01 | **AUDITED** | `da10044ad2579317...` | md5=`XnghQUXrR5bZyi9IeOrdlg==` crc32c=`6LoV0w==` |
| `checkpoints/run_20260729_074350_gen_0007.json` | 0.01 | **AUDITED** | `b77054f2f955cfb9...` | md5=`IBSVS+0NMo4Miuncz6Zf3A==` crc32c=`37e7Lw==` |
| `checkpoints/run_20260729_074350_gen_0247.json` | 0.01 | **AUDITED** | `bdf331735a2f12ad...` | md5=`LIxyNNyXt3Cm4zgDJd36Kw==` crc32c=`a7JnyQ==` |
| `checkpoints/run_20260729_074350_gen_0169.json` | 0.01 | **AUDITED** | `bc2c17404e6302f9...` | md5=`Wv9FBwD5iLD5X4EpMEFCUg==` crc32c=`BiOenQ==` |
| `checkpoints/run_20260729_074350_gen_0074.json` | 0.01 | **AUDITED** | `7b75aa29a70a8bfd...` | md5=`c28lXdafGK1R5jP+GBHSHg==` crc32c=`vLBDMw==` |
| `checkpoints/run_20260729_074350_gen_0248.json` | 0.01 | **AUDITED** | `feefc881c89f8c8b...` | md5=`QBT03M2VuGyj79MXaCWZdg==` crc32c=`NW+AeA==` |
| `checkpoints/run_20260729_074350_gen_0230.json` | 0.01 | **AUDITED** | `34d9df58c99d4549...` | md5=`A++FS35kwRnKkf03f3LCUg==` crc32c=`N8Liug==` |
| `checkpoints/run_20260729_074350_gen_0212.json` | 0.01 | **AUDITED** | `27924dcd0fb69625...` | md5=`Ddv9Wz96ZPkYXCODR+yiwA==` crc32c=`GmeLOg==` |
| `checkpoints/run_20260729_074350_gen_0008.json` | 0.01 | **AUDITED** | `344b6412def6aeb1...` | md5=`lnTu5pIyCDZC2zoLrxxUsQ==` crc32c=`DVXO0w==` |
| `checkpoints/run_20260729_074350_gen_0126.json` | 0.01 | **AUDITED** | `14df1d1c8931bb4a...` | md5=`hGzxrr1YrhJDWTlbbf2oRA==` crc32c=`nYZ6ng==` |
| `checkpoints/run_20260729_074350_gen_0178.json` | 0.01 | **AUDITED** | `ab002443990f9d15...` | md5=`ftaSBqs0e9IiFgeOvxW9Zw==` crc32c=`I2/T2Q==` |
| `checkpoints/run_20260729_074350_gen_0193.json` | 0.01 | **AUDITED** | `0bc45f8af94f9386...` | md5=`BHxxEsYZd8e9GMyAy96UlQ==` crc32c=`dpnXeA==` |
| `checkpoints/run_20260729_074350_gen_0118.json` | 0.01 | **AUDITED** | `4a8a4bc2c930f9d5...` | md5=`C5HFg5b0hIIM0Z9hGA0hpQ==` crc32c=`z8o/+Q==` |
| `checkpoints/run_20260729_074350_gen_0134.json` | 0.01 | **AUDITED** | `8ac6c4e2581e2462...` | md5=`EBozdY+kwjKsu8gDpYKKjA==` crc32c=`nc36QA==` |
| `checkpoints/run_20260729_074350_gen_0069.json` | 0.01 | **AUDITED** | `5efc87dfd2cad332...` | md5=`YYeHhtSxLotGW2aQjs+MFw==` crc32c=`KbqKYg==` |
| `checkpoints/run_20260729_074350_gen_0165.json` | 0.01 | **AUDITED** | `42520d66cee889e4...` | md5=`gJP0639wkWJ0w5udSjWe2w==` crc32c=`3v1Msg==` |
| `checkpoints/run_20260729_074350_gen_0108.json` | 0.01 | **AUDITED** | `7dcebf0b86dd13ab...` | md5=`6ULCOipzyh2sXbjux7Tgmg==` crc32c=`EOcfMg==` |
| `checkpoints/run_20260729_074350_gen_0283.json` | 0.01 | **AUDITED** | `716e49b899c75957...` | md5=`jXSaaAftazZNYCIRzPvgxA==` crc32c=`rs+l9A==` |
| `checkpoints/run_20260729_074350_gen_0269.json` | 0.01 | **AUDITED** | `7d677969b36d6ed4...` | md5=`6ENBzZ8wctSbDHTdxVE1xg==` crc32c=`F6YnZw==` |
| `checkpoints/run_20260729_074350_gen_0233.json` | 0.01 | **AUDITED** | `cbfc5c67afff3794...` | md5=`UQOGaA8w63MO4tRcLfbm3g==` crc32c=`qzWEYA==` |
| `checkpoints/run_20260729_074350_gen_0035.json` | 0.01 | **AUDITED** | `0a1d9ec309a93968...` | md5=`SeKTOo02N97P/Or/qzUP3w==` crc32c=`pvNLqQ==` |
| `checkpoints/run_20260729_074350_gen_0039.json` | 0.01 | **AUDITED** | `cdf1561ff9e461da...` | md5=`iExqgj6bgKQpYzi9tCJe9Q==` crc32c=`YF22KA==` |
| `checkpoints/run_20260729_074350_gen_0246.json` | 0.01 | **AUDITED** | `a5f6505350a33005...` | md5=`huU5W2xYi79IoOm3HaESgw==` crc32c=`5gF/dQ==` |
| `checkpoints/run_20260729_074350_gen_0258.json` | 0.01 | **AUDITED** | `140e31b2ef3a7151...` | md5=`syw5ostpYZc4qaiisFej/w==` crc32c=`ex7cOA==` |
| `checkpoints/run_20260729_074350_gen_0297.json` | 0.01 | **AUDITED** | `ef476ae4e622b5bf...` | md5=`x4KOlJGeHETBWMAIMcF2JA==` crc32c=`wpUEOA==` |
| `checkpoints/run_20260729_074350_gen_0071.json` | 0.01 | **AUDITED** | `b5329dccd69864ac...` | md5=`LCUyIZp5BgC4gMnWZkyO2g==` crc32c=`FEBr8A==` |
| `checkpoints/run_20260729_074350_gen_0252.json` | 0.01 | **AUDITED** | `b995dc405a0e5b60...` | md5=`yq2ytr5EkYBLLM3l7LQ1yg==` crc32c=`e4RP2w==` |
| `checkpoints/run_20260729_074350_gen_0084.json` | 0.01 | **AUDITED** | `b639472b268a28bd...` | md5=`53mBSutUueAkA+ZuV3R6uA==` crc32c=`u0IgQQ==` |
| `checkpoints/run_20260729_074350_gen_0087.json` | 0.01 | **AUDITED** | `3502677e1f219542...` | md5=`D7sQVrxfHwKGiLxJMZFjLA==` crc32c=`5IrzcQ==` |
| `checkpoints/run_20260729_074350_gen_0249.json` | 0.01 | **AUDITED** | `4c56112d26574cc8...` | md5=`EFR5NUbRE0eGlvBrKr0bJQ==` crc32c=`xzQIvg==` |
| `checkpoints/run_20260729_074350_gen_0082.json` | 0.01 | **AUDITED** | `1482a31055f6c6f8...` | md5=`mb24wLv8GWLU2riSAFIBXQ==` crc32c=`Ktfz9g==` |
| `checkpoints/run_20260729_074350_gen_0160.json` | 0.01 | **AUDITED** | `799c4c23791fd9d0...` | md5=`Y3mu2p9P13613gxwo8iDyQ==` crc32c=`BoPKDQ==` |
| `checkpoints/run_20260729_074350_gen_0155.json` | 0.01 | **AUDITED** | `cf79cc7fb0620137...` | md5=`M+1/BhZJ+fgkPN5mQlIVqw==` crc32c=`fdIcpw==` |
| `checkpoints/run_20260729_074350_gen_0299.json` | 0.01 | **AUDITED** | `489725485e98d28a...` | md5=`p8ZDIz8m2fNIAAiV6Ui33Q==` crc32c=`tdryjA==` |
| `checkpoints/run_20260729_074350_gen_0017.json` | 0.01 | **AUDITED** | `20ab1e56c3bfdbf8...` | md5=`hAae4bPY6/gA0UcS4P8IaQ==` crc32c=`zIMBow==` |
| `checkpoints/run_20260729_074350_gen_0096.json` | 0.01 | **AUDITED** | `d95cff530b70198d...` | md5=`GZXntArT7Hvp2rovKj/ixQ==` crc32c=`pUKMCA==` |
| `checkpoints/run_20260729_074350_gen_0152.json` | 0.01 | **AUDITED** | `2c8b5e01c31f9ebb...` | md5=`4oZ0uAwPeoRYt/yJ3kiO9A==` crc32c=`8iVnWQ==` |
| `checkpoints/run_20260729_074350_gen_0229.json` | 0.01 | **AUDITED** | `75aaf92c447bb124...` | md5=`R84JyswKjp8Fx7Y2G3zXUw==` crc32c=`MdxWSA==` |
| `checkpoints/run_20260729_074350_gen_0223.json` | 0.01 | **AUDITED** | `a0910dd24a2bd911...` | md5=`Bdi5pmzdEJXoOS4wCo0ngg==` crc32c=`YRxqQw==` |
| `checkpoints/run_20260729_074350_gen_0138.json` | 0.01 | **AUDITED** | `70f9491b001c05a8...` | md5=`Up26zAEVqF09xCIDyFnYSQ==` crc32c=`R45gdw==` |
| `checkpoints/run_20260729_074350_gen_0197.json` | 0.01 | **AUDITED** | `c7d58b16135fb6c1...` | md5=`ZARIbFtMP2Y0uz2r7Sbz8w==` crc32c=`dGyplg==` |
| `checkpoints/run_20260729_074350_gen_0202.json` | 0.01 | **AUDITED** | `b88c308ba666a8b7...` | md5=`gB2fd8iulN/K45wCGHaeRA==` crc32c=`YqFNuQ==` |
| `checkpoints/run_20260729_074350_gen_0204.json` | 0.01 | **AUDITED** | `8a29bbf5c5e52783...` | md5=`4KOParW7otvxN7T5VI39Jg==` crc32c=`7no2Dw==` |
| `checkpoints/run_20260729_074350_gen_0093.json` | 0.01 | **AUDITED** | `4461d18983de2097...` | md5=`tC1hdy677i6lJUKRzm7lXQ==` crc32c=`eOb1HQ==` |
| `checkpoints/run_20260729_074350_gen_0009.json` | 0.01 | **AUDITED** | `6537b30e7f67107a...` | md5=`42A8FvKr3FTu2vWjJA+ccQ==` crc32c=`H9rTew==` |
| `checkpoints/run_20260729_074350_gen_0137.json` | 0.01 | **AUDITED** | `5b5fbd2161196d02...` | md5=`SGLhGRMQb4dYRuvg4SAYFg==` crc32c=`3x3K4g==` |
| `checkpoints/run_20260729_074350_gen_0148.json` | 0.01 | **AUDITED** | `b296ee0590c09736...` | md5=`SfoVJJ3Uh1+4kmjF+KFdIA==` crc32c=`oSGTqw==` |
| `checkpoints/run_20260729_074350_gen_0266.json` | 0.01 | **AUDITED** | `a2db5b79706614fd...` | md5=`HLo0YU3mMWGoTHdeC51HWA==` crc32c=`lIa/3Q==` |
| `checkpoints/run_20260729_074350_gen_0058.json` | 0.01 | **AUDITED** | `18506de79ac86d3a...` | md5=`Z0UOiDDkFifK3D44+QbQRQ==` crc32c=`6a/eaA==` |
| `checkpoints/run_20260729_074350_gen_0225.json` | 0.01 | **AUDITED** | `d3953854ff5031e3...` | md5=`BO11M9k8paKwmoCsJTk2kw==` crc32c=`t5fnDg==` |
| `checkpoints/run_20260729_074350_gen_0185.json` | 0.01 | **AUDITED** | `87d7bb437c538388...` | md5=`czXHOlnLMGYrCuIue/9wIg==` crc32c=`MJBsHA==` |
| `checkpoints/run_20260729_074350_gen_0259.json` | 0.01 | **AUDITED** | `4ba5fd3fe57eb537...` | md5=`9/SGZ2ayPYp7gC4Nt3Y6Iw==` crc32c=`XoiSbw==` |
| `checkpoints/run_20260729_074350_gen_0207.json` | 0.01 | **AUDITED** | `1fdd44d525eae484...` | md5=`ahvw33jqUTxOCfJuH5LYsQ==` crc32c=`uFKadQ==` |
| `checkpoints/run_20260729_074350_gen_0274.json` | 0.01 | **AUDITED** | `e64f36445f129592...` | md5=`G5kruAasuwoxlWCfRZvi6g==` crc32c=`/RmKeQ==` |
| `checkpoints/run_20260729_074350_gen_0244.json` | 0.01 | **AUDITED** | `d5e4c687543bbe35...` | md5=`fketeKUKEJjUz3IstsWJhQ==` crc32c=`dL6yMA==` |
| `checkpoints/run_20260729_074350_gen_0106.json` | 0.01 | **AUDITED** | `ce4a11eb26090e93...` | md5=`9v4ZXhGkVXM5P7yUlrDhZQ==` crc32c=`+6k2fA==` |
| `checkpoints/run_20260729_074350_gen_0034.json` | 0.01 | **AUDITED** | `2b0aee33a3ee8611...` | md5=`G1fg2EdHD2jmHaiAdyZDsA==` crc32c=`vZ3Ruw==` |
| `checkpoints/run_20260729_074350_gen_0275.json` | 0.01 | **AUDITED** | `693ba4393960bd2b...` | md5=`BRfciEwwgu2iP2USW/EtkA==` crc32c=`KzJnEA==` |
| `checkpoints/run_20260729_074350_gen_0256.json` | 0.01 | **AUDITED** | `53a1fb335a8d3615...` | md5=`8Kv3zpAVkM8rH0GV5/Q1tw==` crc32c=`CanbTA==` |
| `checkpoints/run_20260729_074350_gen_0196.json` | 0.01 | **AUDITED** | `938a032a9fe54298...` | md5=`SBAQazeJ9pFF+1rWenPyXQ==` crc32c=`GbgTsQ==` |
| `checkpoints/run_20260729_074350_gen_0271.json` | 0.01 | **AUDITED** | `f25c15c5db1007cb...` | md5=`nvDCDKzau03N4vKH07SXBw==` crc32c=`P/NGfQ==` |
| `checkpoints/run_20260729_074350_gen_0098.json` | 0.01 | **AUDITED** | `9b6063870e396742...` | md5=`3AMmTYjeEPG80//6f/2nww==` crc32c=`ls4CiQ==` |
| `checkpoints/run_20260729_074350_gen_0031.json` | 0.01 | **AUDITED** | `447a6d3ae2d65e3b...` | md5=`SBlAggkY8EVg3IppCTcfXg==` crc32c=`qmzVSA==` |
| `checkpoints/run_20260729_074350_gen_0044.json` | 0.01 | **AUDITED** | `404c3f17fccb9a5d...` | md5=`n47lKAY1PJmgGFLmDqgp7g==` crc32c=`qsvxEw==` |
| `checkpoints/run_20260729_074350_gen_0050.json` | 0.01 | **AUDITED** | `884a2ed0e10974b7...` | md5=`M+hZI4Fme49FeDK3/rd8Og==` crc32c=`br4yww==` |
| `checkpoints/run_20260729_074350_gen_0079.json` | 0.01 | **AUDITED** | `b46f5ade5d84958d...` | md5=`hExPHzLsryI/aNIU93xQyw==` crc32c=`sFmyhA==` |
| `checkpoints/run_20260729_074350_gen_0260.json` | 0.01 | **AUDITED** | `0d748bd570e946b8...` | md5=`nk/DSH2GMpnRfVOeDpnJYg==` crc32c=`Eq077A==` |
| `checkpoints/run_20260729_074350_gen_0294.json` | 0.01 | **AUDITED** | `8eaf5d9985ba35ba...` | md5=`oIdmsr68aarSusy9mmmIsg==` crc32c=`lt1uWQ==` |
| `checkpoints/run_20260729_074350_gen_0045.json` | 0.01 | **AUDITED** | `4f688b0312d3eb4f...` | md5=`52YJjcEc5nA+p3MIlS/QIg==` crc32c=`8bp/1Q==` |
| `checkpoints/run_20260729_074350_gen_0005.json` | 0.01 | **AUDITED** | `29264e5e507ad07c...` | md5=`Eo2uw04AMB1FQ5oimXqs+A==` crc32c=`iz/yrg==` |
| `checkpoints/run_20260729_074350_gen_0037.json` | 0.01 | **AUDITED** | `a3a861a9059093df...` | md5=`oZJB2YC8JiHCkq5FdPAxbw==` crc32c=`PmO4fQ==` |
| `checkpoints/run_20260729_074350_gen_0091.json` | 0.01 | **AUDITED** | `29c688a38d2bfd7f...` | md5=`2D4z3ZErFzlXW6x/zcVr2Q==` crc32c=`bkFeBg==` |
| `checkpoints/run_20260729_074350_gen_0254.json` | 0.01 | **AUDITED** | `4beb5780942e2de6...` | md5=`VBHWd4c+F1/N/SqY+90RIg==` crc32c=`IbNYSQ==` |
| `checkpoints/run_20260729_074350_gen_0059.json` | 0.01 | **AUDITED** | `328429a40d6f02e3...` | md5=`gB780e4BX+9B+rKHivtPOA==` crc32c=`2EOQ5A==` |
| `checkpoints/run_20260729_074350_gen_0038.json` | 0.01 | **AUDITED** | `71dbb1d932e7a562...` | md5=`GZJDNyn4gL3c2X6auQcrBg==` crc32c=`5yEdJQ==` |
| `checkpoints/run_20260729_074350_gen_0151.json` | 0.01 | **AUDITED** | `ca2e192ab96f827b...` | md5=`ebYx9Y0/M5rb32AB0Lvjgw==` crc32c=`izqMHA==` |
| `checkpoints/run_20260729_074350_gen_0289.json` | 0.01 | **AUDITED** | `961df6791e7eaa75...` | md5=`fw2Yxh4J7EudlnNJPv9XHA==` crc32c=`MpYZeg==` |
| `checkpoints/run_20260729_074350_gen_0052.json` | 0.01 | **AUDITED** | `60f66bc0fcec5b5a...` | md5=`l0Sup2rOIOv7jqp0WGRjKA==` crc32c=`oTQ1JA==` |
| `checkpoints/run_20260729_074350_gen_0147.json` | 0.01 | **AUDITED** | `7ab993eb13003d53...` | md5=`vYQyGa7+/dSmQkfSkZ/V8A==` crc32c=`McsmSg==` |
| `checkpoints/run_20260729_074350_gen_0080.json` | 0.01 | **AUDITED** | `f8026521fb7bca63...` | md5=`RQjWgq/9eO9DM9a/I/lrXg==` crc32c=`VWS20g==` |
| `checkpoints/run_20260729_074350_gen_0261.json` | 0.01 | **AUDITED** | `61ee96ac6e6a86f7...` | md5=`h0hdqrXD45FRKg8E+J+h8Q==` crc32c=`byajng==` |
| `checkpoints/run_20260729_074350_gen_0213.json` | 0.01 | **AUDITED** | `f68bf5f66f1f50ee...` | md5=`/IHkULYU/awjSArpNfuLJg==` crc32c=`t6crPQ==` |
| `checkpoints/run_20260729_074350_gen_0107.json` | 0.01 | **AUDITED** | `f11d68c95e505d2b...` | md5=`ATI5PU/kg8q34SXCRZ2GXQ==` crc32c=`ODEDDA==` |
| `checkpoints/run_20260729_074350_gen_0164.json` | 0.01 | **AUDITED** | `7afe024585656d4e...` | md5=`96Ov1Ei6znuvTMy2rcPj2Q==` crc32c=`AVagsQ==` |
| `checkpoints/run_20260729_074350_gen_0234.json` | 0.01 | **AUDITED** | `62ad983250564d5e...` | md5=`z3zODJD/MHC675q5a/utLA==` crc32c=`Y0giQg==` |
| `checkpoints/run_20260729_074350_gen_0041.json` | 0.01 | **AUDITED** | `8ae9e0f35e5be795...` | md5=`bKawr1I8dgFhMziYR9Bl+w==` crc32c=`UpgZAg==` |
| `checkpoints/run_20260729_074350_gen_0295.json` | 0.01 | **AUDITED** | `4145d76d92749197...` | md5=`N1nqbEmMES6VL/nyHPbTMA==` crc32c=`izY4hA==` |
| `checkpoints/run_20260729_074350_gen_0135.json` | 0.01 | **AUDITED** | `3900bf1ff2308771...` | md5=`6l2C32+P/qwAqzfsPEOOKw==` crc32c=`e2GBTg==` |
| `checkpoints/run_20260729_074350_gen_0264.json` | 0.01 | **AUDITED** | `a263f7c1b089f23a...` | md5=`aAvfD4tFBTvzxXpfqpboVg==` crc32c=`yA8Y6g==` |
| `checkpoints/run_20260729_074350_gen_0240.json` | 0.01 | **AUDITED** | `65d485d56571c0ea...` | md5=`yp0uugbu6pFbIaXyIYS7nQ==` crc32c=`I2Gczw==` |
| `checkpoints/run_20260729_074350_gen_0004.json` | 0.01 | **AUDITED** | `bd43085ec37699d5...` | md5=`NvhpNhZBN25joHFQLxV/Sg==` crc32c=`N0tl/A==` |
| `checkpoints/run_20260729_074350_gen_0010.json` | 0.01 | **AUDITED** | `781beee77336c7a7...` | md5=`6UTtI77YOXi1MEJq44mVUg==` crc32c=`PJuFPg==` |
| `checkpoints/run_20260729_074350_gen_0143.json` | 0.01 | **AUDITED** | `e7f117b7bbffc35a...` | md5=`bNvCErms9h5O9ece0FHWyg==` crc32c=`u94B1w==` |
| `checkpoints/run_20260729_074350_gen_0282.json` | 0.01 | **AUDITED** | `9633589c0380a983...` | md5=`uJ2moJsjZlPgmFcpqF3FBg==` crc32c=`3Erv3A==` |
| `checkpoints/run_20260729_074350_gen_0166.json` | 0.01 | **AUDITED** | `fe4413b4cbc9990a...` | md5=`4weQaS1Zu60ONuL5ZNVCrw==` crc32c=`Bj8CAw==` |
| `checkpoints/run_20260729_074350_gen_0159.json` | 0.01 | **AUDITED** | `3fbfea71f6004277...` | md5=`EnJDROJjmP/lgne1VhIDWg==` crc32c=`9cdYfg==` |
| `checkpoints/run_20260729_074350_gen_0280.json` | 0.01 | **AUDITED** | `3b129def1b2e6d22...` | md5=`wteOq9USnQp/tRKI47HNNQ==` crc32c=`dQ3XOQ==` |
| `checkpoints/run_20260729_074350_gen_0205.json` | 0.01 | **AUDITED** | `fe5f50d2aabb8558...` | md5=`BWon1anXsIgD6IV4/M335g==` crc32c=`5ruwdA==` |
| `checkpoints/run_20260729_074350_gen_0227.json` | 0.01 | **AUDITED** | `938ad8494a9a6f34...` | md5=`xpKJHg22UqJ9o9TD+KNm4A==` crc32c=`pDDRBg==` |
| `checkpoints/run_20260729_074350_gen_0001.json` | 0.0 | **AUDITED** | `b83f69e12e996e8c...` | md5=`v1MndVVYsLcCOJ4PUP4oJw==` crc32c=`BDcx2w==` |
| `checkpoints/run_20260729_074350_gen_0288.json` | 0.01 | **AUDITED** | `b61ea1508a1aa570...` | md5=`arWYbdtq28EJgZkvu9JnYw==` crc32c=`Raw/FA==` |
| `checkpoints/run_20260729_074350_gen_0228.json` | 0.01 | **AUDITED** | `1c28b831d7d0dd59...` | md5=`NO3RT+RpWPtCiGEjD5yG7Q==` crc32c=`TMYqsw==` |
| `checkpoints/run_20260729_074350_gen_0077.json` | 0.01 | **AUDITED** | `f34bca8010f55ab0...` | md5=`Z3RA5hXFs6nn5kfUruTfUg==` crc32c=`hWu+YQ==` |
| `checkpoints/run_20260729_074350_gen_0238.json` | 0.01 | **AUDITED** | `8c97279aea93d3fa...` | md5=`zuQZdH1TxSQ9h4t7Xesbcg==` crc32c=`+O03KQ==` |
| `checkpoints/run_20260729_074350_gen_0245.json` | 0.01 | **AUDITED** | `8cab6e5225547978...` | md5=`GhGcOyG1phoRa1X6WaWGjw==` crc32c=`cpUAjw==` |
| `checkpoints/run_20260729_074350_gen_0085.json` | 0.01 | **AUDITED** | `720efb7fbe09638f...` | md5=`lJy1wHeOf1XsDJFSqkazSA==` crc32c=`3FRBcQ==` |
| `checkpoints/run_20260729_074350_gen_0063.json` | 0.01 | **AUDITED** | `f17a36708780fc22...` | md5=`wzRRjluo3ucKdpNyg+PfRA==` crc32c=`WfJ36w==` |
| `checkpoints/run_20260729_074350_gen_0075.json` | 0.01 | **AUDITED** | `8e973eb6cfec7002...` | md5=`Ocjigcf6uadWH9C+TslMIg==` crc32c=`F09kzA==` |
| `checkpoints/run_20260729_074350_gen_0190.json` | 0.01 | **AUDITED** | `27e0330615affe08...` | md5=`fMoDRKKbES1PeLE/UCO0VA==` crc32c=`/Nh3qw==` |
| `checkpoints/run_20260729_074350_gen_0020.json` | 0.01 | **AUDITED** | `7f1076bbe714ceb6...` | md5=`x18I7L8HmY8RlRWpSASH+Q==` crc32c=`zJxJtQ==` |
| `checkpoints/run_20260729_074350_gen_0139.json` | 0.01 | **AUDITED** | `18ff9243ae03639f...` | md5=`EpykfloeO+HFR7GaO4/19A==` crc32c=`PwNtfQ==` |
| `checkpoints/run_20260729_074350_gen_0028.json` | 0.01 | **AUDITED** | `ca68406de5c4d3d3...` | md5=`ILt4pzhppECrGp9rNkG4Bg==` crc32c=`QwrOWw==` |
| `checkpoints/run_20260729_074350_gen_0198.json` | 0.01 | **AUDITED** | `ebedb0c1208dfc5a...` | md5=`9WcANRL5pKF4m5EQOigSeQ==` crc32c=`gXF71g==` |
| `checkpoints/run_20260729_074350_gen_0123.json` | 0.01 | **AUDITED** | `54a15eab603db9b5...` | md5=`Hj59zvU2V7kyHr8EPh1IaA==` crc32c=`LOtbmA==` |
| `checkpoints/run_20260729_074350_gen_0262.json` | 0.01 | **AUDITED** | `e3e4a3997a3b7cb8...` | md5=`G17bQotYRCHdyErCVwkZjw==` crc32c=`e9zw/g==` |
| `checkpoints/run_20260729_074350_gen_0268.json` | 0.01 | **AUDITED** | `5aba5a4d15c83e26...` | md5=`yNdwgTTblSqmN4gJANSXAw==` crc32c=`XGrUCw==` |
| `checkpoints/run_20260729_074350_gen_0156.json` | 0.01 | **AUDITED** | `ba4e529938f02757...` | md5=`UAH6EDYmYGzW43oai3gxMg==` crc32c=`5ndJfQ==` |
| `checkpoints/run_20260729_074350_gen_0072.json` | 0.01 | **AUDITED** | `eb5eba5e049fd283...` | md5=`j86Gz2MfMzXqN+oZQH1aug==` crc32c=`MIgOZQ==` |
| `checkpoints/run_20260729_074350_gen_0180.json` | 0.01 | **AUDITED** | `8a65b66985dd8d3b...` | md5=`MJDUKYwbf7ysbxZxtBLufQ==` crc32c=`TY2NlA==` |
| `checkpoints/run_20260729_074350_gen_0284.json` | 0.01 | **AUDITED** | `fde5de10738c0821...` | md5=`/+8ZewFRVEd0nnDx/s4S6g==` crc32c=`zHxqFA==` |
| `checkpoints/run_20260729_074350_gen_0231.json` | 0.01 | **AUDITED** | `04fa4e3398b826b9...` | md5=`ldz0XOqa6DXbxKOXfxzekA==` crc32c=`S5ZIrQ==` |
| `checkpoints/run_20260729_074350_gen_0014.json` | 0.01 | **AUDITED** | `f2bd258bef1dd02f...` | md5=`k8LS/ul79OIr4arImavF9Q==` crc32c=`dIi7Sw==` |
| `checkpoints/run_20260729_074350_gen_0157.json` | 0.01 | **AUDITED** | `da703f33084a7b51...` | md5=`QU0bdD24EfaWuUORUyXSMQ==` crc32c=`vYPjFg==` |
| `checkpoints/run_20260729_074350_gen_0236.json` | 0.01 | **AUDITED** | `3535967a8cf81de8...` | md5=`W+rOpoGCiax9LrUT+0+GxQ==` crc32c=`NX9ApA==` |
| `checkpoints/run_20260729_074350_gen_0272.json` | 0.01 | **AUDITED** | `02f24dc3c243ea9e...` | md5=`fY3I2MELmYPiAMdDr6ZyIg==` crc32c=`4Idx1A==` |
| `checkpoints/run_20260729_074350_gen_0150.json` | 0.01 | **AUDITED** | `185154c0950e2c7a...` | md5=`wrgScxAFB2szaweWhd+B/w==` crc32c=`QjbJeQ==` |
| `checkpoints/run_20260729_074350_gen_0142.json` | 0.01 | **AUDITED** | `6b2e39ed52b7aaf6...` | md5=`bc7wvGXSlLhkeJDFzduTsg==` crc32c=`q1QqjQ==` |
| `checkpoints/run_20260729_074350_gen_0144.json` | 0.01 | **AUDITED** | `d8a360703fa45f1c...` | md5=`rawHMrR2LYHxRf6GuPFJfA==` crc32c=`bceCEw==` |
| `checkpoints/run_20260729_074350_gen_0251.json` | 0.01 | **AUDITED** | `d3faf843b8931202...` | md5=`L5Ptoj6XPvRXgycm8jNdIg==` crc32c=`Mc/YJA==` |
| `checkpoints/run_20260729_074350_gen_0276.json` | 0.01 | **AUDITED** | `a724da1f318267e3...` | md5=`ySNCYoIwnV+zVml31WYCuQ==` crc32c=`a+xCXg==` |
| `checkpoints/run_20260729_074350_gen_0285.json` | 0.01 | **AUDITED** | `7249af7268c6fab8...` | md5=`xgXKlQN6UwpLfrFXyOTj7A==` crc32c=`dw4yEw==` |
| `checkpoints/run_20260729_074350_gen_0049.json` | 0.01 | **AUDITED** | `72edff4159211901...` | md5=`cwE59lYRELNOMm/TqMm5ZQ==` crc32c=`Jvqifw==` |
| `checkpoints/run_20260729_074350_gen_0092.json` | 0.01 | **AUDITED** | `ec8171e74a217bcb...` | md5=`4/eQS9guqwFlyfVXkgBuFg==` crc32c=`NSNZMA==` |
| `checkpoints/run_20260729_074350_gen_0200.json` | 0.01 | **AUDITED** | `a8f5951f53c28cd6...` | md5=`9SbrK3S+uDJ1mmGscF3U1w==` crc32c=`btSjCg==` |
| `checkpoints/run_20260729_074350_gen_0018.json` | 0.01 | **AUDITED** | `d137422eac893b54...` | md5=`iQok7G/HkQtHSn8kpMSeMg==` crc32c=`c23+4w==` |
| `checkpoints/run_20260729_074350_gen_0070.json` | 0.01 | **AUDITED** | `7bc4aefa3a36b7fd...` | md5=`ej71T7cBW7Wt6gnoPdn6YA==` crc32c=`wAL4ig==` |
| `checkpoints/run_20260729_074350_gen_0203.json` | 0.01 | **AUDITED** | `aafb376c2cb3cad9...` | md5=`cWvuWp9oVg6zqGwCuLHgrA==` crc32c=`OoaJaw==` |
| `checkpoints/run_20260729_074350_gen_0243.json` | 0.01 | **AUDITED** | `831d054762567d42...` | md5=`bnkVpb4K+x/DkgI/E9ZZsg==` crc32c=`sdhz4Q==` |
| `checkpoints/run_20260729_074350_gen_0208.json` | 0.01 | **AUDITED** | `7667d6f9497415d8...` | md5=`TtgvarLVsJqJZ4ASAbW70g==` crc32c=`tPMdHQ==` |
| `checkpoints/run_20260729_074350_gen_0023.json` | 0.01 | **AUDITED** | `814b2fca68c8557b...` | md5=`MtlDAtc5opN7K5nffZ1yOw==` crc32c=`ERxh7w==` |
| `checkpoints/run_20260729_074350_gen_0140.json` | 0.01 | **AUDITED** | `ae6406d98f8f8daf...` | md5=`N8pkjfYFxbFnSZhzVCEC/A==` crc32c=`Se9NDw==` |
| `checkpoints/run_20260729_074350_gen_0099.json` | 0.01 | **AUDITED** | `14dbe7ce1e254e63...` | md5=`6PLp6APWiCJZcZq8/NS/dQ==` crc32c=`GG/mXA==` |
| `checkpoints/run_20260729_074350_gen_0189.json` | 0.01 | **AUDITED** | `dd974c77e14b386f...` | md5=`JNQh/swP/MRux3j/DjVrEg==` crc32c=`B+woUg==` |
| `checkpoints/run_20260729_074350_gen_0040.json` | 0.01 | **AUDITED** | `1c0a2e48d367ad49...` | md5=`LYiLRYgQenii5sSka2s4sA==` crc32c=`yBWhhQ==` |
| `checkpoints/run_20260729_074350_gen_0241.json` | 0.01 | **AUDITED** | `8ef8506889fd0f61...` | md5=`L5DKSHNsbjoNnjlNlx8GDQ==` crc32c=`57Mw6Q==` |
| `checkpoints/run_20260729_074350_gen_0220.json` | 0.01 | **AUDITED** | `6595afd3d355487b...` | md5=`gq9ix5awRn0A7peBJBvRyg==` crc32c=`HYIXog==` |
| `checkpoints/run_20260729_074350_gen_0163.json` | 0.01 | **AUDITED** | `b3efdd25f513bd70...` | md5=`MyKUyUdBC79/YEyiQkduOQ==` crc32c=`Yx8Cxg==` |
| `checkpoints/run_20260729_074350_gen_0131.json` | 0.01 | **AUDITED** | `fb851b0926291355...` | md5=`Z2+U3YhUmOA/5iXT9VPLuw==` crc32c=`TIkHJg==` |
| `checkpoints/run_20260729_074350_gen_0153.json` | 0.01 | **AUDITED** | `22b7903e5dab6fa6...` | md5=`6KmtJQpCqXCklwF8K3Rjpw==` crc32c=`OgILuA==` |
| `checkpoints/run_20260729_074350_gen_0278.json` | 0.01 | **AUDITED** | `50a586323a7d6896...` | md5=`yOdiDHd7M/t+6t81KOO6fA==` crc32c=`1/sWpA==` |
| `checkpoints/run_20260729_074350_gen_0066.json` | 0.01 | **AUDITED** | `a9bc525261d704ac...` | md5=`ZJ6GTTMg2NgXC0vL+ApMkw==` crc32c=`Z7zlkg==` |
| `checkpoints/run_20260729_074350_gen_0105.json` | 0.01 | **AUDITED** | `da14df6f68c59e56...` | md5=`yFUm1afGJaCO6EVvhheZfg==` crc32c=`GAcYLw==` |
| `checkpoints/run_20260729_074350_gen_0117.json` | 0.01 | **AUDITED** | `2b03fa4a6ad73a4e...` | md5=`BH6MT+9Pfedq0pWNMJUU3g==` crc32c=`WFwkwQ==` |
| `checkpoints/run_20260729_074350_gen_0002.json` | 0.0 | **AUDITED** | `14efd6a873508ca3...` | md5=`NxQCDvtTNCQpg/rl/WNKEQ==` crc32c=`d6NvRQ==` |
| `checkpoints/run_20260729_074350_gen_0113.json` | 0.01 | **AUDITED** | `8c17ed75ea655fc9...` | md5=`sCHSV+h+AAkd79X7g/FyHg==` crc32c=`67gWHg==` |
| `checkpoints/run_20260729_074350_gen_0177.json` | 0.01 | **AUDITED** | `856a537f081efaf3...` | md5=`McwxoC26m+ViJWVvJNlP9Q==` crc32c=`jmkgGg==` |
| `checkpoints/run_20260729_074350_gen_0048.json` | 0.01 | **AUDITED** | `8147b74e6b472d13...` | md5=`1il2VKr+Dhta5g/9jItYKw==` crc32c=`3jaHYQ==` |
| `checkpoints/run_20260729_074350_gen_0114.json` | 0.01 | **AUDITED** | `86dd2263e3a36b79...` | md5=`l4UkMcypl0dhCWTlkajYeQ==` crc32c=`hXK+Cw==` |
| `checkpoints/run_20260729_074350_gen_0051.json` | 0.01 | **AUDITED** | `7f06b9195c59c804...` | md5=`niMmtsQecD7B3fIlygpIwQ==` crc32c=`lvSAdw==` |
| `checkpoints/run_20260729_074350_gen_0167.json` | 0.01 | **AUDITED** | `1de8131ab7a40150...` | md5=`aJnLk9ai+w0w2gqPdHWhGg==` crc32c=`nVfUQg==` |
| `checkpoints/run_20260729_074350_gen_0293.json` | 0.01 | **AUDITED** | `c07aee3bce01b81f...` | md5=`JYaBG7ug5NZKlI7iBAkCkA==` crc32c=`ykmxWA==` |
| `checkpoints/run_20260729_074350_gen_0209.json` | 0.01 | **AUDITED** | `6a796cba958b3d54...` | md5=`VQb/96COP0SV0De8uwHF2g==` crc32c=`nBOJgw==` |
| `checkpoints/run_20260729_074350_gen_0168.json` | 0.01 | **AUDITED** | `03aa5f60cffb8d8c...` | md5=`k3gKCcAafJt8O+6maML1Jg==` crc32c=`udD6Wg==` |
| `checkpoints/run_20260729_074350_gen_0214.json` | 0.01 | **AUDITED** | `cebb26c486cbfa94...` | md5=`JUwPG3LTSwTlzSBE2HNnIA==` crc32c=`lyEQzw==` |
| `checkpoints/run_20260729_074350_gen_0076.json` | 0.01 | **AUDITED** | `01623c4f1049a321...` | md5=`Ntc+roE59/YBoDfYyKRwRQ==` crc32c=`pSlyyg==` |
| `checkpoints/run_20260729_074350_gen_0286.json` | 0.01 | **AUDITED** | `b6ef153eb74a2ea6...` | md5=`ysEd53OUOW5uqgPHVp3gdQ==` crc32c=`vcVS/A==` |
| `checkpoints/run_20260729_074350_gen_0089.json` | 0.01 | **AUDITED** | `2fc87f098a75a489...` | md5=`+aGOVDyCa7Rr6cW2sIAAPw==` crc32c=`1JGEDQ==` |
| `checkpoints/run_20260729_074350_gen_0115.json` | 0.01 | **AUDITED** | `b62b68cdc34a15dc...` | md5=`vC//DNq1EEJoEBhog+MbYA==` crc32c=`+L8N/A==` |
| `checkpoints/run_20260729_074350_gen_0141.json` | 0.01 | **AUDITED** | `77dbd95823d758f2...` | md5=`bBfCUXv7FK/sdgPHkl+xLQ==` crc32c=`xG7dRQ==` |
| `checkpoints/run_20260729_074350_gen_0296.json` | 0.01 | **AUDITED** | `6ab8b13e917d4a23...` | md5=`2yZvvs3Y7Uu95dw1BViBUQ==` crc32c=`qaimWQ==` |
| `checkpoints/run_20260729_074350_gen_0088.json` | 0.01 | **AUDITED** | `614e231817f5ebf0...` | md5=`KuT5c7vLgsdST4ntH/ZDQg==` crc32c=`EoNdOA==` |
| `checkpoints/run_20260729_074350_gen_0149.json` | 0.01 | **AUDITED** | `f34b56679ade9972...` | md5=`oqFcgygT8/R7SwWPghRUWw==` crc32c=`QAxdLA==` |
| `checkpoints/run_20260729_074350_gen_0186.json` | 0.01 | **AUDITED** | `4e47d2d3ebda951b...` | md5=`eo9mQpFzqnfbqIsfutS5Bg==` crc32c=`SE+XkA==` |
| `checkpoints/run_20260729_074350_gen_0215.json` | 0.01 | **AUDITED** | `cd3cfcee0ccc4620...` | md5=`lEcjVbSbnOu9Ag2xB76OKw==` crc32c=`aroR+Q==` |
| `checkpoints/run_20260729_074350_gen_0011.json` | 0.01 | **AUDITED** | `5e7f8411767c6ff6...` | md5=`VTiANDeQ0/h85IaUcZlrWQ==` crc32c=`3UqSEQ==` |
| `checkpoints/run_20260729_074350_gen_0217.json` | 0.01 | **AUDITED** | `6bd6e641ada89ed9...` | md5=`CusijOrM0nyG/XqMhuKiKA==` crc32c=`I429TQ==` |
| `checkpoints/run_20260729_074350_gen_0121.json` | 0.01 | **AUDITED** | `00a7c3bb343a23c7...` | md5=`RnhmGnkpYjleLVEOuTsxFA==` crc32c=`WdOf0g==` |
| `checkpoints/run_20260729_074350_gen_0219.json` | 0.01 | **AUDITED** | `a7abe6fdebe83266...` | md5=`CT1iHQTlED7MhPINyc9/wQ==` crc32c=`hKmL8A==` |
| `checkpoints/run_20260729_074350_gen_0235.json` | 0.01 | **AUDITED** | `31cafd4030d8ef87...` | md5=`lxR2I7/UWkcapvi8VLJF0w==` crc32c=`nacFwA==` |
| `checkpoints/run_20260729_074350_gen_0221.json` | 0.01 | **AUDITED** | `dd8c82f97ac5e17d...` | md5=`gtbm2cQTxs9tnSkh6vC7QA==` crc32c=`J0gpMg==` |
| `checkpoints/run_20260729_074350_gen_0298.json` | 0.01 | **AUDITED** | `b1a82e40997d3480...` | md5=`CblVmTZsczFJGjO0WG51Ww==` crc32c=`2AnN7w==` |
| `checkpoints/run_20260729_074350_gen_0124.json` | 0.01 | **AUDITED** | `30e97f9ed9f58677...` | md5=`vkGyeXb0+TjmHhynGSbW+g==` crc32c=`LND6GQ==` |
| `checkpoints/run_20260729_074350_gen_0250.json` | 0.01 | **AUDITED** | `7e83ba3a0050112d...` | md5=`edU59jrHKqy6MGOvUS+XEg==` crc32c=`QnmOyg==` |
| `checkpoints/run_20260729_074350_gen_0145.json` | 0.01 | **AUDITED** | `601a620877043324...` | md5=`g0RjpkRXJE6V15WHsYBEug==` crc32c=`4ViEpw==` |
| `checkpoints/run_20260729_074350_gen_0101.json` | 0.01 | **AUDITED** | `35215492f68b981c...` | md5=`wy8wm5Ly4zIrlPJ7880JQg==` crc32c=`s+eZbQ==` |
| `checkpoints/run_20260729_074350_gen_0201.json` | 0.01 | **AUDITED** | `fe9c744bef56fb58...` | md5=`o4vXcdMmykSmCl1Bn7QZMg==` crc32c=`pYpzmA==` |
| `checkpoints/run_20260729_074350_gen_0022.json` | 0.01 | **AUDITED** | `7b0a5e86da90148d...` | md5=`9iZsh/HCq33sjkeQVtgtBg==` crc32c=`J2LjQQ==` |
| `checkpoints/run_20260729_074350_gen_0146.json` | 0.01 | **AUDITED** | `e0b2f961761abd82...` | md5=`GHfHgaygLAvCUsmikDuZmA==` crc32c=`eeToRA==` |
| `checkpoints/run_20260729_074350_gen_0078.json` | 0.01 | **AUDITED** | `ab4a8561f954a6d0...` | md5=`DV6FO9MGfkiys/X85KyZDA==` crc32c=`NUAo2A==` |
| `checkpoints/run_20260729_074350_gen_0006.json` | 0.01 | **AUDITED** | `7e7de23062f32db3...` | md5=`GuwghilVm0Gr01fHVwKIwA==` crc32c=`QiYykA==` |
| `checkpoints/run_20260729_074350_gen_0095.json` | 0.01 | **AUDITED** | `c3dab78be90be358...` | md5=`iCSZW68x5VodMgcx1u6ILw==` crc32c=`OWaDOw==` |
| `checkpoints/run_20260729_074350_gen_0179.json` | 0.01 | **AUDITED** | `16838692b0faacf5...` | md5=`K7k6sZ31WbbGiPfQmN9ToQ==` crc32c=`WnbmOw==` |
| `checkpoints/run_20260729_074350_gen_0192.json` | 0.01 | **AUDITED** | `5ee3f00281030221...` | md5=`cYKWSZFevreTFXTpgwX4pA==` crc32c=`1gb4kw==` |
| `checkpoints/run_20260729_074350_gen_0175.json` | 0.01 | **AUDITED** | `a24b646be3ec4091...` | md5=`wBh5XUnaeJW9KACEHj6OaA==` crc32c=`IfTOMQ==` |
| `checkpoints/run_20260729_074350_gen_0226.json` | 0.01 | **AUDITED** | `5c88678c9ea9b2e8...` | md5=`61lLNFAxO+/4ZJeydkVsDA==` crc32c=`v07GhA==` |
| `checkpoints/run_20260729_074350_gen_0003.json` | 0.0 | **AUDITED** | `cdadb8ec0a69e6bf...` | md5=`AolqarufmsxNVm0Bw1ZFRA==` crc32c=`EHxB1Q==` |
| `checkpoints/run_20260729_074350_gen_0170.json` | 0.01 | **AUDITED** | `fb31f6a29bfe9d45...` | md5=`Zzl6pwhLatRJE9h1zmW4wQ==` crc32c=`sa54Zw==` |
| `checkpoints/run_20260729_074350_gen_0116.json` | 0.01 | **AUDITED** | `db6f946de35d0a27...` | md5=`+jOuWa7piJkZsXu1/oYYCQ==` crc32c=`WzUeKw==` |
| `checkpoints/run_20260729_074350_gen_0064.json` | 0.01 | **AUDITED** | `a116a64542a3efc0...` | md5=`13+DgRSQJyn3ffyeK2SECw==` crc32c=`UmbIRA==` |
| `checkpoints/run_20260729_074350_gen_0277.json` | 0.01 | **AUDITED** | `473bf8ece8d8c16f...` | md5=`qsRjbVM2k65zHyeMdb5LjA==` crc32c=`RsdtUw==` |
| `checkpoints/run_20260729_074350_gen_0211.json` | 0.01 | **AUDITED** | `a33120117beb46ca...` | md5=`Julo4x4n1XZ5Y+Tcty3YPw==` crc32c=`sMjvgg==` |
| `checkpoints/run_20260729_074350_gen_0174.json` | 0.01 | **AUDITED** | `58e210be41ca2620...` | md5=`HmhpWvTjKpWOMRKvFhkO7Q==` crc32c=`OOHExA==` |
| `checkpoints/run_20260729_074350_gen_0206.json` | 0.01 | **AUDITED** | `16dee69e99cd6fa0...` | md5=`qi+YaPtAiP5y7wTigsQKJA==` crc32c=`lzxzSw==` |
| `checkpoints/run_20260729_074350_gen_0055.json` | 0.01 | **AUDITED** | `cf8eb9da6aaa087c...` | md5=`QCkQV0e4GxiMcHivWq4GXw==` crc32c=`aOO7LQ==` |
| `checkpoints/run_20260729_074350_gen_0068.json` | 0.01 | **AUDITED** | `a09066fd0638c254...` | md5=`zh4enEpZv7z2xME6WOCWIA==` crc32c=`PvY3HQ==` |
| `checkpoints/run_20260729_074350_gen_0171.json` | 0.01 | **AUDITED** | `5249d1a28fd25e6d...` | md5=`3N37TJkoH17FsTtC83Wdzg==` crc32c=`H0oRXw==` |
| `checkpoints/run_20260729_074350_gen_0025.json` | 0.01 | **AUDITED** | `6fda475c86f18893...` | md5=`Np8N6JlLhzQz0skN2MphEg==` crc32c=`i1qn6Q==` |
| `checkpoints/run_20260729_074350_gen_0013.json` | 0.01 | **AUDITED** | `dc039319dd9fe743...` | md5=`pMHfHUzlbL7D5OPr2qbr+A==` crc32c=`pbuKFA==` |
| `checkpoints/run_20260729_074350_gen_0154.json` | 0.01 | **AUDITED** | `b61c51c28b3736f9...` | md5=`mqwHaXPCvbcSimy4IjFq0g==` crc32c=`iLFmOw==` |
| `checkpoints/run_20260729_074350_gen_0129.json` | 0.01 | **AUDITED** | `2bdd41cab36fdf5d...` | md5=`GeVKBON+1y4fQnyNxZjPdw==` crc32c=`OGrJ5Q==` |
| `checkpoints/run_20260729_074350_gen_0094.json` | 0.01 | **AUDITED** | `847c3c671fd59ff3...` | md5=`a0CfNLi5NUi8c3mYCWcWog==` crc32c=`f2eytQ==` |
| `checkpoints/run_20260729_074350_gen_0232.json` | 0.01 | **AUDITED** | `d12603890983be5f...` | md5=`aGSJ60xfkqulUB49/d5mFQ==` crc32c=`3QXB8A==` |
| `checkpoints/run_20260729_074350_gen_0024.json` | 0.01 | **AUDITED** | `8031501844161cd4...` | md5=`QL4NVTv+2g01p/okskr0sw==` crc32c=`YiTDMQ==` |
| `checkpoints/run_20260729_074350_gen_0184.json` | 0.01 | **AUDITED** | `6fbb4655a72bab36...` | md5=`hdwk+IA1awPLeCqC2nAZoA==` crc32c=`9EnSsA==` |
| `checkpoints/run_20260729_074350_gen_0016.json` | 0.01 | **AUDITED** | `e88c7becea3919ba...` | md5=`V9xc5RuCZrtJ465Bp9hbcg==` crc32c=`W2PRjw==` |
| `checkpoints/run_20260729_074350_gen_0287.json` | 0.01 | **AUDITED** | `e52f72218181ee19...` | md5=`8MwRs9oWeLfkDyNOndTzZQ==` crc32c=`jNgkLw==` |
| `checkpoints/run_20260729_074350_gen_0292.json` | 0.01 | **AUDITED** | `af86f225d0cc620f...` | md5=`ypK2PcQs5K8nW/jvO+evqQ==` crc32c=`oz56Dg==` |
| `checkpoints/run_20260729_074350_gen_0111.json` | 0.01 | **AUDITED** | `48706da518d5f2dd...` | md5=`0T6nU/m6AVHaMQCUz/IzZA==` crc32c=`MBF/fQ==` |
| `checkpoints/run_20260729_074350_gen_0042.json` | 0.01 | **AUDITED** | `f48d768755b8ab71...` | md5=`5c9WwJtKifKrEPF9PVdA+g==` crc32c=`dHERuA==` |
| `checkpoints/run_20260729_074350_gen_0021.json` | 0.01 | **AUDITED** | `c2e5a4fcbb5f82a3...` | md5=`8MgmQVGOyxDPz9LOlU+Zrg==` crc32c=`QzDA2A==` |
| `checkpoints/run_20260729_074350_gen_0043.json` | 0.01 | **AUDITED** | `4df4cbe573eddb26...` | md5=`zEY8XfGtmxTo8A3uZjjsPQ==` crc32c=`dv0l6A==` |
| `checkpoints/run_20260729_074350_gen_0090.json` | 0.01 | **AUDITED** | `056e18c8264e3063...` | md5=`SNjaWzbo6caJpIh7r+iufw==` crc32c=`9yx1Aw==` |
| `checkpoints/run_20260729_074350_gen_0062.json` | 0.01 | **AUDITED** | `9cec4294f955f8fd...` | md5=`dYSvzSOwiQtSlT8ArrgCUQ==` crc32c=`BOdYGA==` |
| `checkpoints/run_20260729_074350_gen_0104.json` | 0.01 | **AUDITED** | `25197e56cd9c0696...` | md5=`A+mWBA1QQeBBQRsvXA4d+Q==` crc32c=`VjpCSg==` |
| `checkpoints/run_20260729_074350_gen_0176.json` | 0.01 | **AUDITED** | `041702781ff39469...` | md5=`3Bz/qyuS8elmTX0QucFSbA==` crc32c=`E2mL9g==` |
| `checkpoints/run_20260729_074350_gen_0086.json` | 0.01 | **AUDITED** | `f242ea7d85b28ea4...` | md5=`XKuk6LL6yjgztxuOsrd7MA==` crc32c=`7jM4Dg==` |
| `checkpoints/run_20260729_074350_gen_0046.json` | 0.01 | **AUDITED** | `d6a18521e4456752...` | md5=`FzLm+q9Nn8hIeQpm9ge9+A==` crc32c=`/PnEFA==` |
| `checkpoints/run_20260729_074350_gen_0125.json` | 0.01 | **AUDITED** | `e16f8c757c396c60...` | md5=`V2bU2H6EyCQ2nXdjejbjyg==` crc32c=`X+IoVQ==` |
| `checkpoints/run_20260729_074350_gen_0061.json` | 0.01 | **AUDITED** | `a0c09a7d643bb0eb...` | md5=`hLvlM2EvV3H/C1Bx3PL9Tg==` crc32c=`8gY7Cg==` |
| `checkpoints/run_20260729_074350_gen_0083.json` | 0.01 | **AUDITED** | `be1798e9598cffc3...` | md5=`mlXadlOLp064s13nRA8P6w==` crc32c=`jBrgAQ==` |
| `checkpoints/run_20260729_074350_gen_0033.json` | 0.01 | **AUDITED** | `904f24e16acfeb82...` | md5=`RyZsLTw5qCkJ+Uh/CrX9Fg==` crc32c=`CYG+pA==` |
| `checkpoints/run_20260729_074350_gen_0030.json` | 0.01 | **AUDITED** | `aab3489bee32fdbb...` | md5=`MN7PkuUJ/hRG7YmDgnsB+A==` crc32c=`iyfF8Q==` |
| `checkpoints/run_20260729_074350_gen_0173.json` | 0.01 | **AUDITED** | `b4845535e2dcbfb8...` | md5=`0E0gbqIdy4J7bgTRhGCFqw==` crc32c=`3eswrQ==` |
| `checkpoints/run_20260729_074350_gen_0097.json` | 0.01 | **AUDITED** | `ec61d8e46a630e16...` | md5=`b01ZjfmgKxQXNBWinDQ1lw==` crc32c=`At1ckw==` |
| `checkpoints/run_20260729_074350_gen_0132.json` | 0.01 | **AUDITED** | `3ab71df12b605f36...` | md5=`yP5tiIqVm4mVFORruCpOyA==` crc32c=`+a002Q==` |
| `checkpoints/run_20260729_074350_gen_0100.json` | 0.01 | **AUDITED** | `b00c8b74d9df176d...` | md5=`opdby/UDxRXtciTprORgkw==` crc32c=`BHCxjg==` |
| `checkpoints/run_20260729_074350_gen_0237.json` | 0.01 | **AUDITED** | `e5aa3d49c20fa6e7...` | md5=`B3VpDjUfpW/2CVCCHB0pkg==` crc32c=`AGZWcA==` |
| `checkpoints/run_20260729_074350_gen_0183.json` | 0.01 | **AUDITED** | `97d057a811288ee2...` | md5=`8d0+6MkPN29G+0nw9a/pkA==` crc32c=`h+qJ0g==` |
| `checkpoints/run_20260729_074350_gen_0270.json` | 0.01 | **AUDITED** | `2ebe6beca1f98a6b...` | md5=`zasBYUgHCRusiBKuhZS+eA==` crc32c=`jilc1w==` |
| `checkpoints/run_20260729_074350_gen_0119.json` | 0.01 | **AUDITED** | `665e7304cde2fad2...` | md5=`sHDVjM1W5OGwiKnrKvWJDQ==` crc32c=`mvSErQ==` |
| `checkpoints/run_20260729_074350_gen_0112.json` | 0.01 | **AUDITED** | `b79d16b827d3c946...` | md5=`HJKzJM0Rjlm7XN0QGv/jAg==` crc32c=`OkLRXA==` |
| `checkpoints/run_20260729_074350_gen_0127.json` | 0.01 | **AUDITED** | `d1f8a921b9994044...` | md5=`9e2N9A1qlJLA5xaPU37LQA==` crc32c=`i8QQ4Q==` |
| `checkpoints/run_20260729_074350_gen_0056.json` | 0.01 | **AUDITED** | `70427bb22b21761e...` | md5=`h1X87z351EiKtw7YSdEKVw==` crc32c=`lrrNEg==` |
| `checkpoints/run_20260729_074350_gen_0161.json` | 0.01 | **AUDITED** | `7f784c483822b804...` | md5=`Ooef6Hrmdo0y9mL6YMZ5Wg==` crc32c=`M6+5nA==` |
| `checkpoints/run_20260729_074350_gen_0122.json` | 0.01 | **AUDITED** | `49e7e2a8ecef55ff...` | md5=`DhuzN3ZxSIOcq1Fx2ABuzA==` crc32c=`Mtjtjw==` |
| `checkpoints/run_20260729_074350_gen_0181.json` | 0.01 | **AUDITED** | `3f1809b60e6e759c...` | md5=`xmy8DSFzPdwIz9Ja6MFG4Q==` crc32c=`11olIQ==` |
| `checkpoints/run_20260729_074350_gen_0036.json` | 0.01 | **AUDITED** | `bffdf83a0698765e...` | md5=`nAnXkQl3R4BkC9MhCXEXIw==` crc32c=`R5Sp+w==` |
| `checkpoints/run_20260729_074350_gen_0032.json` | 0.01 | **AUDITED** | `b0660f74f29bd828...` | md5=`AktyWGd7Q9xxwbSAwwsBew==` crc32c=`iRf3/g==` |
| `checkpoints/run_20260729_074350_gen_0054.json` | 0.01 | **AUDITED** | `bb3efc26167c40f7...` | md5=`tiOqbyOhha4IGwuBN/4C8Q==` crc32c=`+oWEjw==` |
| `checkpoints/run_20260729_074350_gen_0057.json` | 0.01 | **AUDITED** | `03a01616d06e00f8...` | md5=`oZIOxussat/tezj9nKySjw==` crc32c=`Ky/NSQ==` |
| `checkpoints/run_20260729_074350_gen_0194.json` | 0.01 | **AUDITED** | `967fb867dfddb6b4...` | md5=`XBv5B/RlqIRgSfoCCEo4SA==` crc32c=`0eT3Sg==` |
| `checkpoints/run_20260729_074350_gen_0210.json` | 0.01 | **AUDITED** | `97b191ca0c3a858a...` | md5=`5+txCJ5KBTSUvV4+eYZ/Aw==` crc32c=`thvBWA==` |
| `checkpoints/run_20260729_074350_gen_0065.json` | 0.01 | **AUDITED** | `d882ceb61978539f...` | md5=`CJF/c9/tSlUY31Z6w1absA==` crc32c=`1Fn+uQ==` |
| `checkpoints/run_20260729_074350_gen_0281.json` | 0.01 | **AUDITED** | `1e98f285327771f2...` | md5=`loULlGYjam8SRgzalv5Q2A==` crc32c=`noE1RQ==` |
| `checkpoints/run_20260729_074350_gen_0300.json` | 0.01 | **AUDITED** | `0496af82e4683844...` | md5=`fatpxznvkVarlOcbD34R5A==` crc32c=`OzyaEQ==` |
| `checkpoints/run_20260729_074350_gen_0158.json` | 0.01 | **AUDITED** | `5449209bbd26654b...` | md5=`mkT3EAPtD6yM7UCcZPP0kg==` crc32c=`iJxVmQ==` |
| `checkpoints/run_20260729_074350_gen_0216.json` | 0.01 | **AUDITED** | `d331bc4ca408cd04...` | md5=`ExZIvfC32revbTlpOdhbYA==` crc32c=`8UO77Q==` |
| `checkpoints/run_20260729_074350_gen_0172.json` | 0.01 | **AUDITED** | `e0268412c6244a3d...` | md5=`hqoGQoU8cHuYeJFjCVdbjg==` crc32c=`iHwqQQ==` |
| `checkpoints/run_20260729_074350_gen_0191.json` | 0.01 | **AUDITED** | `ce261d9f9c171bea...` | md5=`8mAQUctZms7eBShywBPl8w==` crc32c=`oaSayA==` |
| `checkpoints/run_20260729_074350_gen_0253.json` | 0.01 | **AUDITED** | `379ac2118228cd94...` | md5=`LPh9GNjzOiB1Idx7bnJ4fg==` crc32c=`bYWg/w==` |
| `checkpoints/run_20260729_074350_gen_0026.json` | 0.01 | **AUDITED** | `969fa9de762a4a82...` | md5=`IVix4Ju24nMtHuv2jJR/tw==` crc32c=`5jPiKw==` |
| `checkpoints/run_20260729_074350_gen_0199.json` | 0.01 | **AUDITED** | `1e3f56056284d7c3...` | md5=`kvToo+QKjCD88o/mXoeqFw==` crc32c=`JWVfpw==` |
| `checkpoints/run_20260729_074350_gen_0265.json` | 0.01 | **AUDITED** | `e9330d340aea9ef8...` | md5=`XzsuUVDg6aYRsbQujl1JBQ==` crc32c=`YsIkDA==` |
| `checkpoints/run_20260729_074350_gen_0222.json` | 0.01 | **AUDITED** | `be42571c5d32bab9...` | md5=`c6HbRRbrdJm2NDzd9+qhbQ==` crc32c=`cXx28A==` |
| `checkpoints/run_20260729_074350_gen_0263.json` | 0.01 | **AUDITED** | `b398d06e5d1cdec5...` | md5=`/Jr8WYftZ44dnL14CgoYZA==` crc32c=`hDLNXw==` |
| `checkpoints/run_20260729_074350_gen_0060.json` | 0.01 | **AUDITED** | `83f5635b3a9d3a7b...` | md5=`NAFrOs7M2JNin9n8WhD70Q==` crc32c=`Zpiy6g==` |
| `checkpoints/run_20260729_074350_gen_0136.json` | 0.01 | **AUDITED** | `c16756b4e496b915...` | md5=`PQ0col/j50vuOC0N5PjtSA==` crc32c=`ndJY+A==` |
| `checkpoints/run_20260729_074350_gen_0081.json` | 0.01 | **AUDITED** | `068c5e5fbf0482fd...` | md5=`f4i4yWnQy2wnY3N/XBM0EQ==` crc32c=`IeL1SA==` |
| `checkpoints/run_20260729_074350_gen_0067.json` | 0.01 | **AUDITED** | `4178bd77e8b03c93...` | md5=`pI9J3abGvQtbbGj/o35Lvg==` crc32c=`exJbcQ==` |
| `checkpoints/run_20260729_074350_gen_0012.json` | 0.01 | **AUDITED** | `2687519c32862360...` | md5=`ArPs4MEe7ViJlg/eVhdhyQ==` crc32c=`GOOC+g==` |
| `checkpoints/run_20260729_074350_gen_0128.json` | 0.01 | **AUDITED** | `7a58481c0a1d6de2...` | md5=`f8oCTpt/Fsfp0u3ZCxutRQ==` crc32c=`lJ3d1A==` |
| `checkpoints/run_20260729_074350_gen_0188.json` | 0.01 | **AUDITED** | `14e9d9c3fce12318...` | md5=`BdxKDXW0hsNKlmaU209NCA==` crc32c=`Cxwuiw==` |
| `checkpoints/run_20260729_074350_gen_0073.json` | 0.01 | **AUDITED** | `27853ea0069fd622...` | md5=`HDaEwdapGeBN9/OlSJ5/ow==` crc32c=`WfkCLA==` |
| `checkpoints/run_20260729_074350_gen_0103.json` | 0.01 | **AUDITED** | `f9526622ce779959...` | md5=`HP42xThgoo8gVvcijVQ1bw==` crc32c=`11L2JQ==` |
| `checkpoints/run_20260729_074350_gen_0102.json` | 0.01 | **AUDITED** | `6836da8e5393bcf9...` | md5=`2355PmFQuOh4P1QdVDnxUQ==` crc32c=`26XAHA==` |
| `checkpoints/run_20260729_074350_gen_0027.json` | 0.01 | **AUDITED** | `004c12f01171e09c...` | md5=`2R5N6iig5/EffKz248THXQ==` crc32c=`5N6CdQ==` |
| `checkpoints/run_20260729_074350_gen_0257.json` | 0.01 | **AUDITED** | `2fe89576303a05e7...` | md5=`eF65m5LiQ/XGAbnfzkkohw==` crc32c=`5VF5Ag==` |
| `checkpoints/run_20260729_074350_gen_0182.json` | 0.01 | **AUDITED** | `702c84162c3bce55...` | md5=`C/1wkYpCv7Jc1QAfQIvcsg==` crc32c=`frJCpQ==` |
| `checkpoints/run_20260729_074350_gen_0130.json` | 0.01 | **AUDITED** | `32df62c917430f1b...` | md5=`+H7R9Wr6vglq5VUpbWzcHQ==` crc32c=`bMPQOQ==` |
| `checkpoints/run_20260729_074350_gen_0279.json` | 0.01 | **AUDITED** | `07101aa8bdbffef7...` | md5=`wxQhN03EVhxN7OWmlCcdzQ==` crc32c=`hznoBg==` |
| `checkpoints/run_20260729_074350_gen_0047.json` | 0.01 | **AUDITED** | `ba202b39233ccd59...` | md5=`XFBQQBY3tmrDuhcwQZL+GA==` crc32c=`MWUMnQ==` |
| `checkpoints/run_20260729_074350_gen_0110.json` | 0.01 | **AUDITED** | `78109426f84ebfa9...` | md5=`TOjEAWrAlzIo3ZjEc8KHhw==` crc32c=`ezHarw==` |
| `checkpoints/run_20260729_074350_gen_0053.json` | 0.01 | **AUDITED** | `23fe4cd95e79f0d2...` | md5=`aQ9A26DgHZuW0l2FLkA/5Q==` crc32c=`i0KrpA==` |
| `checkpoints/run_20260729_074350_gen_0162.json` | 0.01 | **AUDITED** | `e3b549d4862e2a5c...` | md5=`Z1Zd43DJ7s+tH0CquynE6g==` crc32c=`woE6Vg==` |
| `checkpoints/run_20260729_074350_gen_0120.json` | 0.01 | **AUDITED** | `95f4395eaeb23ce0...` | md5=`k5rNqmMmBjp3s8VAEaLwxQ==` crc32c=`VTtPEg==` |
| `checkpoints/run_20260729_074350_gen_0267.json` | 0.01 | **AUDITED** | `9fa2bdf3cea53ebb...` | md5=`a/2VmHhya/hciyYp9hSv4w==` crc32c=`+XlbrA==` |
| `checkpoints/run_20260729_074350_gen_0290.json` | 0.01 | **AUDITED** | `8a82c5ce37cd061d...` | md5=`+M97IhOEb2saZXxcBG/tyg==` crc32c=`y9B+Lw==` |
| `checkpoints/run_20260729_074350_gen_0195.json` | 0.01 | **AUDITED** | `e48823897a282311...` | md5=`W1rLEjMouPwSB0ZvacQINw==` crc32c=`/oF9RQ==` |
| `checkpoints/run_20260729_074350_gen_0133.json` | 0.01 | **AUDITED** | `2f567fcf435b9748...` | md5=`EH160ZUF+/NDW9MEgH2mhA==` crc32c=`Mz6crg==` |
| `checkpoints/run_20260729_074350_gen_0273.json` | 0.01 | **AUDITED** | `bf3ec9992ab21c08...` | md5=`6jw0WpAqWAhaTb0eQUC0VQ==` crc32c=`epzq/Q==` |
| `checkpoints/run_20260729_074350_gen_0291.json` | 0.01 | **AUDITED** | `a9713cfd83f599b6...` | md5=`Frfkic2M//pakghTutLhEg==` crc32c=`+JmRIg==` |

### dark_matter/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2745.pt` | 0.0 | **AUDITED** | `eff54b3425d96e95...` | md5=`yHNi+G4+NuvaB2gxsRJsAg==` crc32c=`2HTYhg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_755.pt` | 0.0 | **AUDITED** | `a63cbfb3729193eb...` | md5=`Prxsh76ZqEdXUS7q5NhrkA==` crc32c=`bcihLQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2085.pt` | 0.0 | **AUDITED** | `5afd4f009d95c940...` | md5=`m4URfdUD1NxcE1D7jXalXA==` crc32c=`hdrv4g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_5.pt` | 0.0 | **AUDITED** | `f25273f6fccd421b...` | md5=`QYxT+f31zp7b1wO+x2D4hw==` crc32c=`SATGpw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2330.pt` | 0.0 | **AUDITED** | `6fda5e365d51af6f...` | md5=`irOdg+OLGmcHFj/Ggww2JQ==` crc32c=`goerUA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_740.pt` | 0.0 | **AUDITED** | `5c3791c4f91f8f24...` | md5=`Bd7pT+G58P++sUn/xPE2cg==` crc32c=`G/48tw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1685.pt` | 0.0 | **AUDITED** | `fee8f9e98cd8c0e2...` | md5=`RYb/bq5j5Giwgg9BfNJhWA==` crc32c=`Cowo2w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_545.pt` | 0.0 | **AUDITED** | `5a8d696a0a9368de...` | md5=`iNaeDvBi5ILqkf0sLNHUIg==` crc32c=`UpP7Ew==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3075.pt` | 0.0 | **AUDITED** | `4340c66a8b9d3693...` | md5=`kYRe8k9/zsziOEqVJPGLSA==` crc32c=`V0yatQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2135.pt` | 0.0 | **AUDITED** | `899431094de55756...` | md5=`B3c6bfKPaM2ETCZezsRd7g==` crc32c=`pzu9mw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2055.pt` | 0.0 | **AUDITED** | `1aa856869ca438a5...` | md5=`j10N/lYbZ/Bt4GSJLFa9CQ==` crc32c=`/XQJeA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1725.pt` | 0.0 | **AUDITED** | `5ba2d4d6f9f3e8c4...` | md5=`uGfWzURpmJE29m3R6ZwXig==` crc32c=`I9EaIA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2375.pt` | 0.0 | **AUDITED** | `56904cedd7cad34b...` | md5=`nSMWjbZwUmKuEFGYxg8Z1Q==` crc32c=`TkfQTQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_390.pt` | 0.0 | **AUDITED** | `9ad6df4d6d95e41e...` | md5=`Y0lxEPmK3ACeJUEWzyIcCA==` crc32c=`h3qgag==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_255.pt` | 0.0 | **AUDITED** | `706c118a612e3c8f...` | md5=`29Ft4/hWraSxxkYd7LlTzw==` crc32c=`XYldVg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2995.pt` | 0.0 | **AUDITED** | `c8c2b2bdf59a3a48...` | md5=`e9bUiEIN11dP2fKhGxf0Vg==` crc32c=`/aNc5A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3120.pt` | 0.0 | **AUDITED** | `1e9d31342fb6b1c6...` | md5=`LAeMQOmWLLHZW62jswsJHQ==` crc32c=`8/Z2xQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2925.pt` | 0.0 | **AUDITED** | `7ef5be6a1b874bc8...` | md5=`QmtoxDfSSaBsaMrA7Rgj4A==` crc32c=`vIT5cg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1265.pt` | 0.0 | **AUDITED** | `5e0fa14719c072e9...` | md5=`z8L+cMIuUTHMxqhgNdoNVQ==` crc32c=`5BHGig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_110.pt` | 0.0 | **AUDITED** | `7add0893a7fc810d...` | md5=`3Pk+PGZal6GrWyNSkUnPZA==` crc32c=`ZZFzeg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1755.pt` | 0.0 | **AUDITED** | `c620fc532252eecf...` | md5=`g32N38utZMoMNAlWahFYZA==` crc32c=`EeQ5rg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2395.pt` | 0.0 | **AUDITED** | `683d19fd46fbc605...` | md5=`sqHGzx8jKEw9TbsPjAsSqQ==` crc32c=`Ki2XUQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2715.pt` | 0.0 | **AUDITED** | `d588cdda04ff8f67...` | md5=`cS2H9TYV2Nm/3Ud6eLNafg==` crc32c=`/Tk6DA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1730.pt` | 0.0 | **AUDITED** | `07dc9379c0a568b0...` | md5=`/9Lj0jR07ZfienwKBsOdaA==` crc32c=`ylyDtw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_575.pt` | 0.0 | **AUDITED** | `1ab8ee6951fd9d30...` | md5=`J3OXCRgAP3hgjDs/E3L6Fg==` crc32c=`z6SQrA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2720.pt` | 0.0 | **AUDITED** | `c6aa67c4353fcf05...` | md5=`dTHngJRKt7Ivom8MnnJ/+A==` crc32c=`A8xinw==` |
| `dark_matter/hypergraph/processing/hypergraph/continuum_limits/__pycache__/vacuum_energy_calculator.cpython-310.pyc` | 0.0 | **AUDITED** | `68782ec1b450f9ff...` | md5=`u0xpnqkbr8Bn2ujulp5ppg==` crc32c=`tPLEpw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2485.pt` | 0.0 | **AUDITED** | `fe57e38b0067ba2c...` | md5=`JGJKFWZaFq2dOx/q7OVieQ==` crc32c=`Dy1Grw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1170.pt` | 0.0 | **AUDITED** | `70645e9496d31510...` | md5=`p9C7qigYiQj6gMS5+7bRTA==` crc32c=`qddHLA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1565.pt` | 0.0 | **AUDITED** | `e71b509791a3d72a...` | md5=`uoMne7CqpPfwskSMQfbcKQ==` crc32c=`yq139g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2535.pt` | 0.0 | **AUDITED** | `6c6bbd5cc37600d4...` | md5=`0MeVuNK45H6FFAZJ3jJAGA==` crc32c=`LcwU1g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_765.pt` | 0.0 | **AUDITED** | `952adfd136c4c133...` | md5=`w5b+zW/pRIHMugQ9rhjF/Q==` crc32c=`8P/Kkg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2365.pt` | 0.0 | **AUDITED** | `4ba82656d17cf420...` | md5=`XUUjF96WBz8mMvEWEx66bQ==` crc32c=`Rfuwzw==` |
| `dark_matter/hypergraph/results/brief/report.md` | 0.0 | **AUDITED** | `be9614738a5a08bb...` | md5=`A6mVB3EYwkrqCGLnrSJoSA==` crc32c=`rtH9bw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_495.pt` | 0.0 | **AUDITED** | `cb33dbbaa1c58028...` | md5=`AnbtM0h97KpDKbeCxPUIZA==` crc32c=`/labtQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1680.pt` | 0.0 | **AUDITED** | `feffefa63cb0fa97...` | md5=`5NU7DL1KRWeD8gQHyC8edw==` crc32c=`6L3Rzg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1905.pt` | 0.0 | **AUDITED** | `ee0c5ac860c9d6b7...` | md5=`UwOCuEp8HWnTbV20PWrrTw==` crc32c=`adC53A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_100.pt` | 0.0 | **AUDITED** | `192084b4dadf58a1...` | md5=`7yrJrvKvaGnAwhN1ElR6Ww==` crc32c=`7dh4QA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2880.pt` | 0.0 | **AUDITED** | `ce46029d76f16977...` | md5=`a45FCBPt20FfsFyRjyk5zw==` crc32c=`d+gynA==` |
| `dark_matter/hypergraph/results/deepmind_scientific_review_report.md` | 0.01 | **AUDITED** | `d25fb48353f0f363...` | md5=`KzF6DD3grYx/Mq2HqpzmeA==` crc32c=`eoNPgw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1795.pt` | 0.0 | **AUDITED** | `7ad562db5e9e8213...` | md5=`hKLAgufS1arSvGlv/TmVkg==` crc32c=`Yva/tg==` |
| `dark_matter/hypergraph/processing/hypergraph/phase0_tensor_masking.py` | 0.01 | **AUDITED** | `7c8259b487c17420...` | md5=`6i3Lcnumh8lHmHozG6+daA==` crc32c=`QC5LIg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2965.pt` | 0.0 | **AUDITED** | `385600d5485c6a7a...` | md5=`0mb363o71C/Cr7kiTDdlUQ==` crc32c=`knV7eg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1735.pt` | 0.0 | **AUDITED** | `3c8ce99128c8804d...` | md5=`xbHlZMSc/IU4wJVdrGzcGQ==` crc32c=`KG16og==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_670.pt` | 0.0 | **AUDITED** | `f7c4f73542b271ef...` | md5=`qVegyw8GkmzlqVT/Z/9oAg==` crc32c=`3UB/ig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2505.pt` | 0.0 | **AUDITED** | `a36fe0b76c04f087...` | md5=`7ahzkxhbWRK1OFLtq0LXTA==` crc32c=`MQi1UA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2195.pt` | 0.0 | **AUDITED** | `6cd07de085194554...` | md5=`Z3fTpknsdvOHZoR9GE6Chg==` crc32c=`7aB4jw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1785.pt` | 0.0 | **AUDITED** | `501570d1bf26d65d...` | md5=`A3WQBtYQA7y8sPL5QFRViw==` crc32c=`aUrfNA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1055.pt` | 0.0 | **AUDITED** | `29e43979b188e868...` | md5=`b/YhyZeQ8zx7A55b8G04JA==` crc32c=`P1iI0g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2270.pt` | 0.0 | **AUDITED** | `42e4bd1466a9108d...` | md5=`3rnxgu4NZRLj9FQrVUECLA==` crc32c=`z7Detw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2710.pt` | 0.0 | **AUDITED** | `a5a636cba6da3073...` | md5=`BTDVhh18/nDVajUNhgVjAA==` crc32c=`HwjDGQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_265.pt` | 0.0 | **AUDITED** | `11516f4536766efb...` | md5=`BtzljQhxS7DcZug7qRp2ow==` crc32c=`wL426Q==` |
| `dark_matter/hypergraph/results/wpp_computational_essay.md` | 0.01 | **AUDITED** | `db14754ee5182c5e...` | md5=`2HthLJBxGKmGCQ9RnVocrQ==` crc32c=`HgMAgA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2565.pt` | 0.0 | **AUDITED** | `d887d284d3b6d45e...` | md5=`HnOOqoMJ4/SVIinQVOIEPg==` crc32c=`CIH2XA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1665.pt` | 0.0 | **AUDITED** | `8fc1fc93e8e7df45...` | md5=`6bDRHgCWbgb7jOxDE0JYeg==` crc32c=`buZvxw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1885.pt` | 0.0 | **AUDITED** | `cacd16252b7f114a...` | md5=`W4aO2qvii+w67RTinbiUUw==` crc32c=`V/VKIw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_785.pt` | 0.0 | **AUDITED** | `ce5026ad3969a16a...` | md5=`J2x3fgOevrCWRZEe9PQgHQ==` crc32c=`moTpCQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1985.pt` | 0.0 | **AUDITED** | `c256ef4a9e14efee...` | md5=`HbYCsEYY6L9j4b77TEbI9g==` crc32c=`NDO9zA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_155.pt` | 0.0 | **AUDITED** | `88fe7e65c665fe55...` | md5=`2UG+s9Zdl9NhDySYa+EX1w==` crc32c=`sRIk0A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_115.pt` | 0.0 | **AUDITED** | `fc1cf4a047af7ce5...` | md5=`3qmA9zCTFkKImVHBvf8q5g==` crc32c=`m+7l2g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1850.pt` | 0.0 | **AUDITED** | `4695a8f702afdca4...` | md5=`xZ/z5L3mLz6LUZD8otF1Cg==` crc32c=`zWpVrA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1805.pt` | 0.0 | **AUDITED** | `1dbb543c2abb0928...` | md5=`eCc9o3P1oWSxbqQs01Z5Ew==` crc32c=`ChZOMw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_240.pt` | 0.0 | **AUDITED** | `28fedbd6eb292c8d...` | md5=`owqdpIqN56GoU26b+Ren1w==` crc32c=`K7/AzA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_50.pt` | 0.0 | **AUDITED** | `b4e76c6135d3a696...` | md5=`0OOwrftmaG1rnircC3V7VA==` crc32c=`mFqM1g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_280.pt` | 0.0 | **AUDITED** | `171e569f8941da98...` | md5=`8WJwzG0lJ3QZK4O91gLrng==` crc32c=`VLqD0g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_375.pt` | 0.0 | **AUDITED** | `cce20e7c29b50065...` | md5=`a3M7t1VxeX8al2Isw794Ow==` crc32c=`E34VUQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2385.pt` | 0.0 | **AUDITED** | `5782af0c30f467a6...` | md5=`9QCFnCPeKGhkhYbni1NPtQ==` crc32c=`IZH30w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_985.pt` | 0.0 | **AUDITED** | `c948daf4017dec04...` | md5=`ZF0sjbPkDAtE8ziry33tZA==` crc32c=`kc/FBg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2430.pt` | 0.0 | **AUDITED** | `f6027dcf1ea7b395...` | md5=`siWRkCNuGYQmpzBwqtDYHw==` crc32c=`rDsaLA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1365.pt` | 0.0 | **AUDITED** | `72259c11a599e511...` | md5=`C5y4qD3l5CQchk+wfaOkHg==` crc32c=`h9cxZQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3025.pt` | 0.0 | **AUDITED** | `d35e8c0d00bcc630...` | md5=`eih9YAkoqbPu9Hd7p1scuQ==` crc32c=`cgF4Pw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_900.pt` | 0.0 | **AUDITED** | `895536a06e8b5a4c...` | md5=`ZqEKiY6kNdrdcLn2KVB09w==` crc32c=`OknRsg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_975.pt` | 0.0 | **AUDITED** | `93652e54f2cb0c71...` | md5=`HjlphsoSTGreE3dANEGJEQ==` crc32c=`c/3tpw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2340.pt` | 0.0 | **AUDITED** | `bcbeaffe4a526d7c...` | md5=`+HHRnxvdCxEpgE/NueEqbg==` crc32c=`sLKI3g==` |
| `dark_matter/hypergraph/results/brief/g_extraction_results.json` | 0.0 | **AUDITED** | `3bc28a5c4bf02679...` | md5=`eLRMqWXj9SawVaQBv+wz+w==` crc32c=`4Farvg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3055.pt` | 0.0 | **AUDITED** | `ed38f7b647060e62...` | md5=`kk2LqMvgICEjvJzoGlqByQ==` crc32c=`QDRbsQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_955.pt` | 0.0 | **AUDITED** | `185402e27594c71b...` | md5=`l4OZCQComvhYulth4km/ng==` crc32c=`ZoONIg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_135.pt` | 0.0 | **AUDITED** | `050f1984907a0627...` | md5=`5VXpOkH03w4BDzPj4iTa0w==` crc32c=`jpCFXw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1260.pt` | 0.0 | **AUDITED** | `4b6eb773a4c0fc8b...` | md5=`9OSgzxn6QH01fZYsqbvVdw==` crc32c=`BiA/nw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2945.pt` | 0.0 | **AUDITED** | `42dde6cc33dc5393...` | md5=`oF+9ytl4ga2chuRMSaPK+A==` crc32c=`hQ26fg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3045.pt` | 0.0 | **AUDITED** | `6d2006b199420185...` | md5=`1YXiNn1FWcQ6IK66ImWTUw==` crc32c=`S4g7Mw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_420.pt` | 0.0 | **AUDITED** | `5971a46fb6eb2362...` | md5=`6r1zaIsmNXu3Q++TXB71jA==` crc32c=`yOfkvg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1915.pt` | 0.0 | **AUDITED** | `d50c5824e492ecb7...` | md5=`7yZWkQKYrpyxT/foCVkLnQ==` crc32c=`YmzZXg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_890.pt` | 0.0 | **AUDITED** | `9d77ab469e6ffb64...` | md5=`smwf7oh9tfhJD7ERnQfm2g==` crc32c=`vHBwHg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2285.pt` | 0.0 | **AUDITED** | `63383b166a6cf2da...` | md5=`3SskcREwpxf2Z6Tjx5Jxjg==` crc32c=`QlcAPA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1975.pt` | 0.0 | **AUDITED** | `01b9312ef8832f3e...` | md5=`6FWU0vctumh6IIXbzmGAPg==` crc32c=`W+WaUg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3030.pt` | 0.0 | **AUDITED** | `a7aedc9127ac622d...` | md5=`dxLXCHy+VNeCFwXdHL40LQ==` crc32c=`m4zhqA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3115.pt` | 0.0 | **AUDITED** | `710650f482964c8d...` | md5=`veesNLy2Wt5srXFr9ZH9mw==` crc32c=`DQMuVg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_395.pt` | 0.0 | **AUDITED** | `8ebafd09a7dedf02...` | md5=`w/NJHjMcSHwUs65qQyoLsg==` crc32c=`eQU2yg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1045.pt` | 0.0 | **AUDITED** | `47d258119fa40e9a...` | md5=`N6Kp1QXYLD23z9IqXl04dw==` crc32c=`NOToUA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3110.pt` | 0.0 | **AUDITED** | `59853517b86a07bc...` | md5=`YKmVX3RvMCMgplh4D1zydw==` crc32c=`7zLXQw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_595.pt` | 0.0 | **AUDITED** | `f0d411860dd6030c...` | md5=`UuWyhTFWLKWU2sGlfD0k6A==` crc32c=`pd+zNw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_865.pt` | 0.0 | **AUDITED** | `7569779e0835daba...` | md5=`0F4tfyzI/DMirZD7teD7DQ==` crc32c=`oD3OHw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1050.pt` | 0.0 | **AUDITED** | `3bdfe2c918df4d54...` | md5=`vOiNgKRJem/Ga+kYoWGqpQ==` crc32c=`3Wlxxw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2180.pt` | 0.0 | **AUDITED** | `c8be3c11b8a43386...` | md5=`NzL4eUI3Q14EyE3EzOodew==` crc32c=`BC3hGA==` |
| `dark_matter/hypergraph/results/deepmind_scientific_audit_brief.md` | 0.01 | **AUDITED** | `606028f1962506b4...` | md5=`0GU5SFIU7t7iCZ2+G/drRA==` crc32c=`YiNMSA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1465.pt` | 0.0 | **AUDITED** | `03eb5c77cbc3a360...` | md5=`yeUcndiS8mQiWAALYnzg4A==` crc32c=`qWuAGQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1200.pt` | 0.0 | **AUDITED** | `91a73d89be59978b...` | md5=`DFXEVFNOVzzNDBG75Gs6PA==` crc32c=`P6l8kw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2510.pt` | 0.0 | **AUDITED** | `0c69fcfae4a8d17b...` | md5=`+Qhbz6C82YaWQt2fbTPGhg==` crc32c=`2IUsxw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_600.pt` | 0.0 | **AUDITED** | `5c0654ed784a4ba0...` | md5=`VZv314eMfns/79PTn+EB6A==` crc32c=`aovVPw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_635.pt` | 0.0 | **AUDITED** | `894713be2918ee6a...` | md5=`7Fd7LSG6DiHHfVEwLIhHWg==` crc32c=`CcMoIA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_650.pt` | 0.0 | **AUDITED** | `56da20d18cd063e8...` | md5=`Xwlm5vb5sgBTNQwoHw9m1g==` crc32c=`yD4fDw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_910.pt` | 0.0 | **AUDITED** | `60f0dd8849937447...` | md5=`l0zqwohFsLZ6HmE4GAQENA==` crc32c=`sgDaiA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1720.pt` | 0.0 | **AUDITED** | `4b9ad6cdcb58cd1d...` | md5=`hkEGsAYaSuWLE1Tz8svj7Q==` crc32c=`weDjNQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1715.pt` | 0.0 | **AUDITED** | `8c43923e045b7c00...` | md5=`g9+8sFBpU71jQFlN1Ml8GQ==` crc32c=`PxW7pg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2895.pt` | 0.0 | **AUDITED** | `46a22f5a5b6cddff...` | md5=`gs24fzUhY2rI39xnSUP7DA==` crc32c=`nmWrCw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1530.pt` | 0.0 | **AUDITED** | `b92379d360dfdb04...` | md5=`4rDXcgnaJYTIVmxgQ4WWWg==` crc32c=`DdFsaQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2490.pt` | 0.0 | **AUDITED** | `067df20ca81d1306...` | md5=`cDz2AVhCwyJaKQTrqrRoHQ==` crc32c=`5qDfOA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3150.pt` | 0.0 | **AUDITED** | `cedd1350de06e069...` | md5=`S0cjEDaBPP1cnNcyX4KscA==` crc32c=`wcNVSw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_640.pt` | 0.0 | **AUDITED** | `c6c9da6c03ee8953...` | md5=`uq20KVS2/r/xo2pM9jyHbQ==` crc32c=`QHcUNQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1210.pt` | 0.0 | **AUDITED** | `ffabc7f01f4045d9...` | md5=`QaZ49sjEwNGVfOFcPW7BsQ==` crc32c=`NBUcEQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2840.pt` | 0.0 | **AUDITED** | `eef686b5a882a8e8...` | md5=`TbI+LJGJp+0JMe8ceFFZjw==` crc32c=`BPq0hA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2765.pt` | 0.0 | **AUDITED** | `6a93ee61500e89ed...` | md5=`hf4hqUwjWksf7K5dRKsnDg==` crc32c=`zwwZgg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1220.pt` | 0.0 | **AUDITED** | `26dc13e7b88b7a1e...` | md5=`pZIKLNUI/yBbuEa4N/4mgQ==` crc32c=`KNG9lw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_725.pt` | 0.0 | **AUDITED** | `0c3031646043e72d...` | md5=`l+Y1gFDBCihOpVnKZkS88A==` crc32c=`2gMLmA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2405.pt` | 0.0 | **AUDITED** | `364c8528ccef964e...` | md5=`kpC5Be+HO2HWJoo5Hjn3JQ==` crc32c=`Us5Cvw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2560.pt` | 0.0 | **AUDITED** | `141c7e1ab2a1107a...` | md5=`a+mZ/6jLQvKvwM1bLHkDnw==` crc32c=`6rAPSQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2070.pt` | 0.0 | **AUDITED** | `1e8bf065f011047d...` | md5=`nISoaiqRSBTKEt6tOO3MWw==` crc32c=`CD0xaQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1335.pt` | 0.0 | **AUDITED** | `b19c2f90631da44d...` | md5=`Lv19QkymNU3aFD81w7nJ9g==` crc32c=`oprT7w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2530.pt` | 0.0 | **AUDITED** | `2648f1056a74a4f8...` | md5=`0/18IogAPWIMCMCuOLAXJQ==` crc32c=`z/3tww==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1075.pt` | 0.0 | **AUDITED** | `f4c9329a635b007f...` | md5=`cV2dP6da4n7qvLiIIxD5hA==` crc32c=`KCBJ1g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2230.pt` | 0.0 | **AUDITED** | `6384e2377dd60e40...` | md5=`wwIyKkzJplz2KMKCSxaG7g==` crc32c=`4UFcvw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1560.pt` | 0.0 | **AUDITED** | `c7e8dd066a083943...` | md5=`kuS2JOReC+ZFCvGnYg0EXQ==` crc32c=`KJyO4w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_305.pt` | 0.0 | **AUDITED** | `bcfac38f4012b79a...` | md5=`y+n1Vc2XjF+gFpOG68Kh+A==` crc32c=`pLW/5A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2350.pt` | 0.0 | **AUDITED** | `773f61ebd7f56113...` | md5=`XajA255a/hva78mCCHwt9w==` crc32c=`uw7oXA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1255.pt` | 0.0 | **AUDITED** | `a177a2a458e45bd8...` | md5=`nIvoZOyH/w254MnYdRelXw==` crc32c=`+NVnDA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1625.pt` | 0.0 | **AUDITED** | `9de90085c1cac044...` | md5=`L6l7MMdG+EbM+rouKAMQqw==` crc32c=`QBftzw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2000.pt` | 0.0 | **AUDITED** | `79b16b1a3ec3a443...` | md5=`nJ0VO3Tj1OhI9NbaPqW7IQ==` crc32c=`OggS5w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2845.pt` | 0.0 | **AUDITED** | `8cbfc05f41c86231...` | md5=`QFYHfx/mTyJJvw2Y6JXklw==` crc32c=`5stNkQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_705.pt` | 0.0 | **AUDITED** | `dd7891b4ee705ef8...` | md5=`ANq6EBUZKYbnMNKxLNgyyQ==` crc32c=`z31rHQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2105.pt` | 0.0 | **AUDITED** | `f4e2a67ebe9f572b...` | md5=`bftQiIvL997kQeFY6xCK0Q==` crc32c=`u/8cHQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2640.pt` | 0.0 | **AUDITED** | `0a7d6f2a0b0a861f...` | md5=`bEyn4bgxDv0Ydg/wU4s+DA==` crc32c=`WYPWfA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2520.pt` | 0.0 | **AUDITED** | `13788a6a185eb416...` | md5=`dd2gGgJqDLZxe0uPtzfkWg==` crc32c=`xEGNQQ==` |
| `dark_matter/hypergraph/results/brief/deepmind_deepthink_review.md` | 0.01 | **AUDITED** | `80cc74384ac1e167...` | md5=`rdqUEby4Frm21kFlmiG+AA==` crc32c=`X94lJw==` |
| `dark_matter/hypergraph/results/mfdm_cross_validation.json` | 0.0 | **AUDITED** | `743d52b772b81ec6...` | md5=`gFFaLd3oyRRWPaWbTXT4cA==` crc32c=`gQ1TtQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1920.pt` | 0.0 | **AUDITED** | `42ee140fcf472c72...` | md5=`DVcsNMZPYmVll1JLCtKVhQ==` crc32c=`nJmBzQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_370.pt` | 0.0 | **AUDITED** | `a985669cbbe83322...` | md5=`BsSca0R8yHUDriuwSslveQ==` crc32c=`7QGD8Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1620.pt` | 0.0 | **AUDITED** | `10edcae237e21b7a...` | md5=`fnJNT0scNm9zv8HUMXL0SA==` crc32c=`oiYU2g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1060.pt` | 0.0 | **AUDITED** | `c616c1ac0cf8d68c...` | md5=`1ch7FObiT8TLX6sxleo+FA==` crc32c=`wa3QQQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_560.pt` | 0.0 | **AUDITED** | `dcfc6fdec0dbf160...` | md5=`870iS8b6PmbDadeUEulLBg==` crc32c=`uZINNg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_435.pt` | 0.0 | **AUDITED** | `51d6e766c067a09d...` | md5=`Ajtj39lWaKSwYGs66KjHFQ==` crc32c=`vtF5JA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_655.pt` | 0.0 | **AUDITED** | `869b7946610d1474...` | md5=`s9N9h6lSL1/Gv2l/cvjR8g==` crc32c=`NkGJrw==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/__init__.py` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2075.pt` | 0.0 | **AUDITED** | `a82040cf6b590592...` | md5=`Ccnw0N2Y2dSf0AP0SxHfIQ==` crc32c=`6gzIfA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2870.pt` | 0.0 | **AUDITED** | `4bf9c297417c4227...` | md5=`aFAvzqehVJESxLo9STDzxw==` crc32c=`GD4VAg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1570.pt` | 0.0 | **AUDITED** | `d648db04d5a68f78...` | md5=`j+ddIHJMPbzIR1zMqMfU6Q==` crc32c=`IyDuYQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2675.pt` | 0.0 | **AUDITED** | `21e7346586d0f07a...` | md5=`pEpgq2luXgUxfgiAYtNrDw==` crc32c=`p3aO7w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2090.pt` | 0.0 | **AUDITED** | `b749b0de37277be7...` | md5=`p2OMUWae+J2KV+BFRpsEKQ==` crc32c=`bFd2dQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_980.pt` | 0.0 | **AUDITED** | `04bd3d5f03cf957a...` | md5=`asj4+HVUOdLmKZgC6/8lmA==` crc32c=`b7BTpg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2730.pt` | 0.0 | **AUDITED** | `1759730db624b41c...` | md5=`p5X1axe4pyYBPv65zwSJfQ==` crc32c=`CHACHQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2050.pt` | 0.0 | **AUDITED** | `91a8f1296b2ab2b6...` | md5=`PSDDuWWj3bKSlU8WtWRuYg==` crc32c=`H0XwbQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1090.pt` | 0.0 | **AUDITED** | `fb704ab87c1c5bfe...` | md5=`a0k0kDakh2ToVIWJE2QzEw==` crc32c=`rnv33w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2020.pt` | 0.0 | **AUDITED** | `060096a07cb108ae...` | md5=`xJAPd/6bg9tKksqH0ZszeA==` crc32c=`LXDT4w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2970.pt` | 0.0 | **AUDITED** | `c2790f379afcea1c...` | md5=`xKhrbtK4tMvjchUhHcuPLA==` crc32c=`e/ji7Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1315.pt` | 0.0 | **AUDITED** | `83ebd8d333b80245...` | md5=`qBGpSLEStRSE9QMDpbu9tA==` crc32c=`teIS6w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1235.pt` | 0.0 | **AUDITED** | `53dc085025f8751e...` | md5=`Hvit23TBK1CKl94dn59z/g==` crc32c=`wVwkAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1270.pt` | 0.0 | **AUDITED** | `0c85e698494a8667...` | md5=`VRFASB2yFWunI19i3StE3A==` crc32c=`DZxfHQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_65.pt` | 0.0 | **AUDITED** | `8de2a9b29da5b747...` | md5=`j9OHD7GOLGG4L78rGVYb6w==` crc32c=`9ozCwQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1370.pt` | 0.0 | **AUDITED** | `17325fe0fb8947c7...` | md5=`I4PN+0l3HG2Nc9ZdOG/37Q==` crc32c=`blqo8g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1410.pt` | 0.0 | **AUDITED** | `54331d810bad46f1...` | md5=`Sv6fWnwhM93leXJraXeGKw==` crc32c=`eW9agg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1350.pt` | 0.0 | **AUDITED** | `bc7b33fa80155493...` | md5=`P+rX6E0RnIKFCyjwCk8jcg==` crc32c=`eSJp9g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1970.pt` | 0.0 | **AUDITED** | `869496388ebca222...` | md5=`mRnE+y2cELI2bb6n1OuaUw==` crc32c=`udRjRw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2205.pt` | 0.0 | **AUDITED** | `d5f46b3f69f94e79...` | md5=`dJvejmu//fYe6SF/OMEp1g==` crc32c=`H7QELA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_270.pt` | 0.0 | **AUDITED** | `bba68ee1e599626f...` | md5=`+TOzRySiUEFwEt5MA2CWJw==` crc32c=`toircw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1165.pt` | 0.0 | **AUDITED** | `a42e6832a4360b7e...` | md5=`Y88I4PiGSTKoyEwiWPlRBw==` crc32c=`QFreuw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2440.pt` | 0.0 | **AUDITED** | `e1214b9789ad1647...` | md5=`kHUy3hOv8pdnEJFaR7e92A==` crc32c=`ng45og==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2930.pt` | 0.0 | **AUDITED** | `0f81c09d4449db7c...` | md5=`SCC1FB1x4G1h3ZDbASITJA==` crc32c=`VQlg5Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_810.pt` | 0.0 | **AUDITED** | `34a7dd6119be03f4...` | md5=`4zNd1BJTTTy4oxuSbLbHSA==` crc32c=`6YnyCg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1810.pt` | 0.0 | **AUDITED** | `ae1fa4bf0f61ed7e...` | md5=`7df3XXpJgwz2VDSlQZ9ziA==` crc32c=`45vXpA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_950.pt` | 0.0 | **AUDITED** | `b8fee977dd9a0bbe...` | md5=`3witcslVhNOMTRN6KWGQ5g==` crc32c=`mPwbgg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1135.pt` | 0.0 | **AUDITED** | `fe8c4342159efc7f...` | md5=`FSP4jVwBoECWjKKj0RBN/w==` crc32c=`ZRc8MQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1195.pt` | 0.0 | **AUDITED** | `a53a5b20a307b269...` | md5=`WiletMfuOg10fbq8zg5epQ==` crc32c=`L4z5JQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1820.pt` | 0.0 | **AUDITED** | `a5110bb2d8d60b6c...` | md5=`lIGd5KM/7TCzzcCljE9umA==` crc32c=`/192Ig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2215.pt` | 0.0 | **AUDITED** | `7370b3243693930b...` | md5=`FYuG8wyaXI3ULAJOIHMn6w==` crc32c=`FAhkrg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2185.pt` | 0.0 | **AUDITED** | `26b2dccdd67c95a6...` | md5=`m1OFgJ80BPG29/gZGf3CjA==` crc32c=`5hwYDQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1245.pt` | 0.0 | **AUDITED** | `8a0278128a4d545a...` | md5=`/bULr7Q1+SLOfhedcSK6og==` crc32c=`82kHjg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1470.pt` | 0.0 | **AUDITED** | `5c03b3bcea319bfb...` | md5=`zzewOGdFNg/HJFxdaUQPYw==` crc32c=`QOYZjg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2005.pt` | 0.0 | **AUDITED** | `81d4e294785edbd5...` | md5=`GlMFLg7KFUoCgg0u6pW7xA==` crc32c=`2Dnr8g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2265.pt` | 0.0 | **AUDITED** | `cd0e947b1c435f7d...` | md5=`+lPfksfDn6FW5T9eVWarww==` crc32c=`Jj1HIA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1285.pt` | 0.0 | **AUDITED** | `023b8bbb6b063d99...` | md5=`ovMcIKf8PeWZZrnLZH6Czg==` crc32c=`gHuBlg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1650.pt` | 0.0 | **AUDITED** | `a19aae91c220ca2d...` | md5=`kR3Opfj8H5Rt8sfAPEVUew==` crc32c=`kBM3VA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2035.pt` | 0.0 | **AUDITED** | `6ca516898f4adaa5...` | md5=`IaNngEF/oTP9OuDq6ylMLw==` crc32c=`xP1KdA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_515.pt` | 0.0 | **AUDITED** | `c1edfb5e21f2f6f3...` | md5=`sE4q2XgGHKMavV39SQTWig==` crc32c=`8CYxIw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_70.pt` | 0.0 | **AUDITED** | `703247e88a60d6e9...` | md5=`zyZvAg5Hb07rAlkgEYVgQA==` crc32c=`BYkEnQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2120.pt` | 0.0 | **AUDITED** | `0fa2c283a03ca474...` | md5=`jqRIu0N1kX1VgbIkUwQFrA==` crc32c=`TrYkDA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2830.pt` | 0.0 | **AUDITED** | `079faeea508360cc...` | md5=`DUjt1KhemGTvMM0lOGRbiQ==` crc32c=`Ns+XCg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_150.pt` | 0.0 | **AUDITED** | `394f9be6fc0cf75a...` | md5=`tXyv8KyZ6eacmn7+vcGbGw==` crc32c=`T22ycA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2610.pt` | 0.0 | **AUDITED** | `fbcf27fc5a5edad3...` | md5=`V9iXEj0cNjEWOdfjUeDQHQ==` crc32c=`fM409g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1495.pt` | 0.0 | **AUDITED** | `66350f484327cf8d...` | md5=`Qi5ncv/rara4Vq10vgbd6A==` crc32c=`xr2nhw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_835.pt` | 0.0 | **AUDITED** | `0441c8cbe34af51e...` | md5=`sLQ9CwaV3aLYfbG86046BA==` crc32c=`AogELw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_320.pt` | 0.0 | **AUDITED** | `3ab7a782b60e69ca...` | md5=`mdcvoMKbSAmpHDFNgQ/HZA==` crc32c=`T7RJwQ==` |
| `dark_matter/hypergraph/results/brief/emergent_g_coupling.png` | 0.19 | **AUDITED** | `7bb692a343a51306...` | md5=`y8hU/uZ8O1dgS20luh7/eg==` crc32c=`2/OmMw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2080.pt` | 0.0 | **AUDITED** | `f49d80b7f1cef1dc...` | md5=`egToTOVa2XoWVnjIa0dkBQ==` crc32c=`Z+sW9w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2390.pt` | 0.0 | **AUDITED** | `b5620ac5ec3f4b95...` | md5=`1IE4QIvqH/9KoCsBFZuMHg==` crc32c=`yBxuRA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_945.pt` | 0.0 | **AUDITED** | `b0982c4d595771be...` | md5=`hpzLU7wcfCnb7uHOdG+hHw==` crc32c=`7sqGGA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1925.pt` | 0.0 | **AUDITED** | `8428ff5b35184553...` | md5=`zL3TC/z91Zo/8/U5X9WFgg==` crc32c=`fqh42A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_825.pt` | 0.0 | **AUDITED** | `1ca51211694afcb3...` | md5=`HKvE4o3/tmSeSxaQDiiEpw==` crc32c=`isEPFQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2980.pt` | 0.0 | **AUDITED** | `94d3dd9d8521f131...` | md5=`OVkdajm//tWdm1GluJOZuQ==` crc32c=`FC7Fcw==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/__pycache__/oligon_defect_sim.cpython-310.pyc` | 0.0 | **AUDITED** | `4925661495b3ff36...` | md5=`KHGQaiwN5WvvfB1CobpN+Q==` crc32c=`V9hx8A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2025.pt` | 0.0 | **AUDITED** | `7446d4fd2fb0dafa...` | md5=`Maf2GscYHhI9grhfupL5eg==` crc32c=`z0Eq9g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_405.pt` | 0.0 | **AUDITED** | `e62d56e23c810015...` | md5=`UDERiE7L9i6B0NDF1tRUWg==` crc32c=`I+YSmw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1940.pt` | 0.0 | **AUDITED** | `bbb454b72b5a228e...` | md5=`inOkVwWGtP1yE5MulJohNA==` crc32c=`pRDCwQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1550.pt` | 0.0 | **AUDITED** | `bd4e6f9bfeed662e...` | md5=`CFaEIKWCCPkzxox9oUOpow==` crc32c=`NFgvZQ==` |
| `dark_matter/hypergraph/processing/hypergraph/rate_limiter.py` | 0.0 | **AUDITED** | `6ee3f36ae1a29c65...` | md5=`fVWPUYFQ95ulppfhAJsjug==` crc32c=`atSRMA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1695.pt` | 0.0 | **AUDITED** | `15a8a6bf73b7b59a...` | md5=`u3LcClFCg/YKEPitI339Rw==` crc32c=`ATBIWQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2585.pt` | 0.0 | **AUDITED** | `4ea12161f97fc3cb...` | md5=`+ifZDvW3d59l9iOvR/RkZw==` crc32c=`bOuxQA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_525.pt` | 0.0 | **AUDITED** | `bb20e478118f0727...` | md5=`LtZn5jnlY9SSWLBwGcvIPg==` crc32c=`bRFanA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1780.pt` | 0.0 | **AUDITED** | `0382d4f43fa33864...` | md5=`uEqw3dSie/zXpmJ7NXyyzA==` crc32c=`i3smIQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2245.pt` | 0.0 | **AUDITED** | `b910d528d7ee0eba...` | md5=`CKKS0VfFVXY+U3LSi3uPPQ==` crc32c=`MUWGJA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1450.pt` | 0.0 | **AUDITED** | `6c2be795d69d1909...` | md5=`MjDQbeetYA269rzOjScjDg==` crc32c=`V57Yig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_815.pt` | 0.0 | **AUDITED** | `83b3de256758e962...` | md5=`vdtAiQNP7//uOKWHrC8ejg==` crc32c=`F/Zkqg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1035.pt` | 0.0 | **AUDITED** | `7206c1ce576684df...` | md5=`djbdgc5PYtdW64qCoDaFWQ==` crc32c=`BtHL3g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1430.pt` | 0.0 | **AUDITED** | `89c586510c85734b...` | md5=`uABNU5Tdkh6uwWNkW+0n8Q==` crc32c=`bhebhg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1490.pt` | 0.0 | **AUDITED** | `df0bb90f26db4326...` | md5=`6eB+SE/NWkqvVCAXKclZtw==` crc32c=`JIxekg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2655.pt` | 0.0 | **AUDITED** | `01b1b33bd07bcca1...` | md5=`7PU5P5Yy1grjwzuOw7MyXA==` crc32c=`sA5P6w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1535.pt` | 0.0 | **AUDITED** | `3011f4f9812bbc33...` | md5=`gpCIa9/hOnlWSbk65eP2aQ==` crc32c=`7+CVfA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_620.pt` | 0.0 | **AUDITED** | `7d2f0eddf5ed42b2...` | md5=`M5FE7bwSYnihSGvSisx0Ow==` crc32c=`f/W1ug==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1515.pt` | 0.0 | **AUDITED** | `aa1cea42aa2bd0d9...` | md5=`4xlKLH/cXUJ230BEd4gFHQ==` crc32c=`+JhUeA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1140.pt` | 0.0 | **AUDITED** | `14eeafe203b10433...` | md5=`/1VrTo5+npm/DnNbqV44DQ==` crc32c=`tRPmqg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2475.pt` | 0.0 | **AUDITED** | `e993c6f6a2de5fba...` | md5=`mxa6gUQsQ3h6qz14f59UWQ==` crc32c=`YPthMQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_10.pt` | 0.0 | **AUDITED** | `eabb8dc2c1860fc3...` | md5=`8/+vlP1Mf4WLvVGHvj8FEA==` crc32c=`phHqsQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_665.pt` | 0.0 | **AUDITED** | `9931824e42e8af0b...` | md5=`Rz64P8YgzVqn5tqWp8GyEQ==` crc32c=`q3biEA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2775.pt` | 0.0 | **AUDITED** | `a5498c1c20a217e7...` | md5=`IolpR9Y9FqPK9QlXloAHyA==` crc32c=`xLB5AA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_860.pt` | 0.0 | **AUDITED** | `ecab788a452d4b65...` | md5=`QmqLSfAyH0Pn+wyMRuxvIQ==` crc32c=`XkJYvw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_870.pt` | 0.0 | **AUDITED** | `1ced2b2a43077f3e...` | md5=`j9wQxpmVJkaUbqDoc+/q4w==` crc32c=`1gtThQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1590.pt` | 0.0 | **AUDITED** | `1d26c43b0aafe528...` | md5=`W7MHXJTDR5pKqQkDajvYvA==` crc32c=`R0qpfQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1770.pt` | 0.0 | **AUDITED** | `8193981b9d4ab78a...` | md5=`9l5TzaujQzI3TE4vFa54tA==` crc32c=`5K0Bvw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1380.pt` | 0.0 | **AUDITED** | `148775f4e0ca7de8...` | md5=`49r5z/R8k3v0JIE8uU/IgA==` crc32c=`AYyPbA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2030.pt` | 0.0 | **AUDITED** | `20bb0e1cb04a35b2...` | md5=`gXyPGQ+eMhW6207R/mLECg==` crc32c=`JsyzYQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1145.pt` | 0.0 | **AUDITED** | `76ce9ec06e7f9504...` | md5=`OUPom3OswBRYn6gZ3yPLEg==` crc32c=`VyIfvw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2955.pt` | 0.0 | **AUDITED** | `0736c56321e5d761...` | md5=`EOygkKFIeoGo9eqW6VLXOw==` crc32c=`jrHa/A==` |
| `dark_matter/hypergraph/results/brief/MFDM_Continuum_Limit_Paper.md` | 0.0 | **AUDITED** | `741ad01dd66adf27...` | md5=`UePdxLcuO32zpWaJoIZmUg==` crc32c=`cbQWtg==` |
| `dark_matter/hypergraph/processing/hypergraph/continuum_limits/__init__.py` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2470.pt` | 0.0 | **AUDITED** | `5213419a6426b331...` | md5=`OAl3lIvUYA8gBFVviirZBg==` crc32c=`gsqYJA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1280.pt` | 0.0 | **AUDITED** | `8637ba408292668d...` | md5=`eokGWEZeyHWJPo2Lx943aw==` crc32c=`Ykp4gw==` |
| `dark_matter/hypergraph/results/brief/n_body_clustering_halo.png` | 1.24 | **AUDITED** | `766372693f2c1c9e...` | md5=`VUf6DAUHx40OuZcePaiYLQ==` crc32c=`c7nrBg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_120.pt` | 0.0 | **AUDITED** | `ac7c6bb3d7fcd464...` | md5=`/qkqALbU7QQ2zb4gIWp7FQ==` crc32c=`+KYYxQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2410.pt` | 0.0 | **AUDITED** | `0678ca6323b26fd9...` | md5=`+AxiB/p+alHrdEiy1RTOrQ==` crc32c=`u0PbKA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1955.pt` | 0.0 | **AUDITED** | `47d5bedf463b6016...` | md5=`RzMDukzazwMsz0IS2jBkZg==` crc32c=`TJ1bVg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1330.pt` | 0.0 | **AUDITED** | `7f5685934effac42...` | md5=`wzh/VYqvpMc/SuIkUooweQ==` crc32c=`QKsq+g==` |
| `dark_matter/hypergraph/processing/hypergraph/dry_run_local_mvp.py` | 0.01 | **AUDITED** | `d6c3b9baadba0903...` | md5=`e44+Jo8wd8R9p0jpwFiMHA==` crc32c=`0CmaQA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_990.pt` | 0.0 | **AUDITED** | `6afb446442b8e338...` | md5=`MmbpNWRVYP5Ny0dtA68pog==` crc32c=`5/lYnA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1895.pt` | 0.0 | **AUDITED** | `7bb4217100252961...` | md5=`u6v/ymrCjCK0ZhDkDO6IkA==` crc32c=`XEkqoQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2515.pt` | 0.0 | **AUDITED** | `92b48dc0aea43b24...` | md5=`fXiHbSVIK/pqey9LX//pSA==` crc32c=`OrTV0g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_180.pt` | 0.0 | **AUDITED** | `aaf23d7857c2afbf...` | md5=`Iqs8zQ/gco/SP8clSBqn3A==` crc32c=`uCH6VA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1545.pt` | 0.0 | **AUDITED** | `09e8328e7797dba7...` | md5=`SbakBIfRkcy7khu5H/fsRg==` crc32c=`3dW28g==` |
| `dark_matter/hypergraph/results/wpp_computational_essay.wl` | 0.01 | **AUDITED** | `228456060155d275...` | md5=`/loIDgBdoDVLxN9ksW5fRg==` crc32c=`4ieW7Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2735.pt` | 0.0 | **AUDITED** | `1ef0bbe95bbf26c7...` | md5=`/GF1BZh7/oBVWYD+z1O2QA==` crc32c=`6kH7CA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2760.pt` | 0.0 | **AUDITED** | `09b926b4a78b3a75...` | md5=`0uiyVxLpXIz1eGOS08zjPQ==` crc32c=`LT3glw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1070.pt` | 0.0 | **AUDITED** | `2d6dbd4b9c4f887a...` | md5=`98mlnRgXNsQFmlrEEGMpSA==` crc32c=`yhGwww==` |
| `dark_matter/hypergraph/processing/hypergraph/cost_monitoring.py` | 0.0 | **AUDITED** | `409b61e126b041f2...` | md5=`mMxKw3MYiujXAHmS08y4bA==` crc32c=`u1BuHg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2625.pt` | 0.0 | **AUDITED** | `425b04dde445420f...` | md5=`BYbEwXBEJPTouBE0SHEbQQ==` crc32c=`gjtsZQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1485.pt` | 0.0 | **AUDITED** | `0138827f107df27d...` | md5=`PUn4vh6i3vvIXyZCtOfIQA==` crc32c=`zQHHBQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_880.pt` | 0.0 | **AUDITED** | `ea001e4b95f1abef...` | md5=`6uK/imScvzrxIc8/FahFfw==` crc32c=`NDl7JA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_90.pt` | 0.0 | **AUDITED** | `45f13c779e687020...` | md5=`8z7qPO7AVAe064PKyCieBw==` crc32c=`2ocmfw==` |
| `dark_matter/hypergraph/results/brief/n_body_clustering_results.json` | 0.0 | **AUDITED** | `5a64808396eebdc5...` | md5=`SKCRT2fSoV3l/TPk4QbrkA==` crc32c=`NQnAHw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_145.pt` | 0.0 | **AUDITED** | `04f7527aea3017d9...` | md5=`M3XM9UUJ2Dbu31A9+C0G4w==` crc32c=`OVsv6g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2800.pt` | 0.0 | **AUDITED** | `67600e6eeb059de5...` | md5=`8CLAF4tpIJSF7wmcDtxZDQ==` crc32c=`Kgs2jA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_675.pt` | 0.0 | **AUDITED** | `4103a49633bcd71f...` | md5=`io9fj9pgLRpqMTiXzP2Gbg==` crc32c=`Iz/pKg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_75.pt` | 0.0 | **AUDITED** | `dc1ccd3d70a67da2...` | md5=`hV9mrHeXXC7lQsyBUMx7wg==` crc32c=`OpM9nA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1005.pt` | 0.0 | **AUDITED** | `33aec52537fed65b...` | md5=`z+rf8e4SLOmj9WtXALCGWw==` crc32c=`GhVqWA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3010.pt` | 0.0 | **AUDITED** | `9f0de54083f69ea4...` | md5=`E+E7JRLrV/4ItjYkYqzPqw==` crc32c=`jPQgrA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2835.pt` | 0.0 | **AUDITED** | `c6276e9966b8d761...` | md5=`gm42M5QUVROxYPxN/aHlSw==` crc32c=`1P5uHw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_715.pt` | 0.0 | **AUDITED** | `b5d3067216a57cbf...` | md5=`3va/9kQxwLduQUHARo6LMA==` crc32c=`RzRgJw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_790.pt` | 0.0 | **AUDITED** | `c3a11ee0857e010c...` | md5=`L/DquH3CHlLKtmTMJmqvqQ==` crc32c=`7LJ0kw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2545.pt` | 0.0 | **AUDITED** | `2a4243b61c68c245...` | md5=`ZQU5OLsrMhKKzRYYm50yAA==` crc32c=`H/k3WA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2380.pt` | 0.0 | **AUDITED** | `31c3a8f265c2da86...` | md5=`t4H7uhGsdqdOFx39emVpXQ==` crc32c=`w6AOxg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_130.pt` | 0.0 | **AUDITED** | `bd0e5cdf13a9ff89...` | md5=`LxLQbA9RD3dXcTlyjvx/TQ==` crc32c=`cO8T/w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_580.pt` | 0.0 | **AUDITED** | `f810937d2e22ade6...` | md5=`l/KHnIK6eLozYFthjZnZ4Q==` crc32c=`0+kurQ==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/oligon_mfdm_mapper.py` | 0.0 | **AUDITED** | `59e6f5d581668d95...` | md5=`dpSBiwOuJckKhzm9qwV2fg==` crc32c=`M7T4Cg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2125.pt` | 0.0 | **AUDITED** | `54508cf73fb99e44...` | md5=`w7ARMCp2uMrZBPlLjPIlGQ==` crc32c=`rIfdGQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2580.pt` | 0.0 | **AUDITED** | `688e76f9c1bb4656...` | md5=`M9PkikFoms+yM4wEvOHm+A==` crc32c=`jtpIVQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2040.pt` | 0.0 | **AUDITED** | `71ab22e01c12114b...` | md5=`xJXeM1U0s9QGX+D8mOcuZw==` crc32c=`FPmQ7w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2425.pt` | 0.0 | **AUDITED** | `46c2e6954d31615c...` | md5=`FFyLJssQXC7oiCiO+IMWVw==` crc32c=`RbaDuw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2275.pt` | 0.0 | **AUDITED** | `f1052e9955d1b237...` | md5=`K2f9PSDeAZZlR+YBr3vi4g==` crc32c=`LYEnog==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1945.pt` | 0.0 | **AUDITED** | `409608d1a2d9d009...` | md5=`5390le0dEocRgmZnRBvzQw==` crc32c=`RyE71A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2705.pt` | 0.0 | **AUDITED** | `840d7bc461379e3c...` | md5=`Bfi82Kac/99jVhc+hb/WkQ==` crc32c=`9oVajg==` |
| `dark_matter/hypergraph/results/batch_status.json` | 0.0 | **AUDITED** | `5cf1a1df81f60f10...` | md5=`XkEWMz82Uesv7Q8DwbyJJg==` crc32c=`B10N5g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1870.pt` | 0.0 | **AUDITED** | `9830d233b83ee8cf...` | md5=`q1FGxXS/u008btmv+Zi/+w==` crc32c=`2hKUqA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1605.pt` | 0.0 | **AUDITED** | `bc1bb5c002c1cfa5...` | md5=`RI5+ZmEflcbKt3fGiLVGlg==` crc32c=`V28syw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1360.pt` | 0.0 | **AUDITED** | `2c6fb556ae61ab86...` | md5=`CXU35zSxMcukT9GQYS4s+g==` crc32c=`ZebIcA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1750.pt` | 0.0 | **AUDITED** | `8eca214bdc000015...` | md5=`BmQxbS/Q77geu4cWoc1KIg==` crc32c=`89XAuw==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/multiway_rules.py` | 0.0 | **AUDITED** | `e163aef610755597...` | md5=`j5MTdjf8Se77zPY3xY1JXQ==` crc32c=`iB9bew==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1640.pt` | 0.0 | **AUDITED** | `35c87e6d2c73e0a5...` | md5=`qr0LfF27jNp3rSQ0/4TgXA==` crc32c=`m69X1g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_365.pt` | 0.0 | **AUDITED** | `aad8b926c5261b0a...` | md5=`voeJjAJrNw6bTHbnurwelg==` crc32c=`mzceaw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1415.pt` | 0.0 | **AUDITED** | `992a033aa5d6cd35...` | md5=`SN6hfLJM0AhAWplBUmzZlQ==` crc32c=`m16jlw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_500.pt` | 0.0 | **AUDITED** | `1407773b7fe29eeb...` | md5=`EDWzn+PBwJ0VJsYLYZZgUA==` crc32c=`hhCsuQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1845.pt` | 0.0 | **AUDITED** | `dad0d6869c0d84d6...` | md5=`xWOCkozn6bCyxu4HcElJsg==` crc32c=`JOfMOw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_775.pt` | 0.0 | **AUDITED** | `0f3e95d962817eb2...` | md5=`DGdxS+/uwGPYkicEwx5ncA==` crc32c=`eLbBqA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2690.pt` | 0.0 | **AUDITED** | `471ab9f383c5df48...` | md5=`vd6fA7cE59+IXN5imdZl8Q==` crc32c=`IS0w5g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_485.pt` | 0.0 | **AUDITED** | `2397dfd1d589d73f...` | md5=`wD0jyV2fiXF2lGL1pIsU1g==` crc32c=`dh+Qjw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2345.pt` | 0.0 | **AUDITED** | `f2fa0dbc7f2ebb01...` | md5=`MlVFD6jpvcChpZo/j1dmFA==` crc32c=`UoNxyw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2220.pt` | 0.0 | **AUDITED** | `d54980817ee5dc2d...` | md5=`C5WlNWAAPGeL/dSMzLUjDg==` crc32c=`6v08PQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2225.pt` | 0.0 | **AUDITED** | `6f29ace381799fc9...` | md5=`2ZDUcY++Pyvpt/cBjWBofg==` crc32c=`CMzFKA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2815.pt` | 0.0 | **AUDITED** | `0e6309c88f58337a...` | md5=`aH9IOZSVC+iZPvhBOA+/5w==` crc32c=`w4avGw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2825.pt` | 0.0 | **AUDITED** | `bc1168ef72f3c848...` | md5=`57Z/nWzMsmEnhTeu8mtBXQ==` crc32c=`30IOnQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1775.pt` | 0.0 | **AUDITED** | `ed1a108e18e80d7c...` | md5=`cuWr5VFUAxDfgeN812FCVA==` crc32c=`Bpz4qg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1175.pt` | 0.0 | **AUDITED** | `10c842114e5518ee...` | md5=`brwRwcQbp5UiR8DFHJL1kg==` crc32c=`S+a+OQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_295.pt` | 0.0 | **AUDITED** | `1d629b245cc826c7...` | md5=`3R0+i1ztqlKN/AD0ixiXSg==` crc32c=`IoweSA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2940.pt` | 0.0 | **AUDITED** | `d6acf2cbb6e9a61f...` | md5=`xYxh+Ks+cHABJ+VPTcIiiQ==` crc32c=`ZzxDaw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2855.pt` | 0.0 | **AUDITED** | `17bde683582d321e...` | md5=`qt1UcnzE5D+SVsoTS1MPTw==` crc32c=`7XctEw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1765.pt` | 0.0 | **AUDITED** | `259e90c336beb60b...` | md5=`UFkkehMDE+phmsA356LLFg==` crc32c=`DSCYKA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_105.pt` | 0.0 | **AUDITED** | `5b600e0e6233fb52...` | md5=`FR8JO2byKslGHNfEUxI9Gw==` crc32c=`E6fu4A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3020.pt` | 0.0 | **AUDITED** | `79c552110bd8b74b...` | md5=`+ozukF8Ps4YCj4u4pSFKjw==` crc32c=`kDCBKg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2740.pt` | 0.0 | **AUDITED** | `f6cbf74cb1388c17...` | md5=`00f0uA43mk4KZCITUF2vyQ==` crc32c=`OkUhkw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2635.pt` | 0.0 | **AUDITED** | `7e3aefa84d3af5ce...` | md5=`Cm4KTvI4jqHkzk3XhuN4kw==` crc32c=`iYcM5w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2320.pt` | 0.0 | **AUDITED** | `56e3caf81aa2820e...` | md5=`eIxsgWKJxQjOQco0+KRZjA==` crc32c=`iTvL0g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1480.pt` | 0.0 | **AUDITED** | `61b7162703547e7a...` | md5=`IIyZ5FO83FkfPsfUQmXtFg==` crc32c=`LzA+EA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2045.pt` | 0.0 | **AUDITED** | `fca1aebe05d73503...` | md5=`PWkAV4/0g/Hm4ukqKACtwQ==` crc32c=`9shp+g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_695.pt` | 0.0 | **AUDITED** | `f432e05a54ec963f...` | md5=`75ZS0Dq/EYxbs9JLQr8qGA==` crc32c=`SUTKsQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2885.pt` | 0.0 | **AUDITED** | `9916c7e8d6844bf9...` | md5=`izaZHH8ApTUHabnrRhs8Qg==` crc32c=`ldnLiQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_585.pt` | 0.0 | **AUDITED** | `ba3acca90a24cc90...` | md5=`lo0x+AJND7AN+k0JplEziw==` crc32c=`LZa4DQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_20.pt` | 0.0 | **AUDITED** | `92e886d7d73ac010...` | md5=`my7TOH7Wa5CcMGMZiEfjVg==` crc32c=`992dpw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_505.pt` | 0.0 | **AUDITED** | `05fc51feca417b1a...` | md5=`vFsv1FYLVveTuzPn+55IMw==` crc32c=`eG86GQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2190.pt` | 0.0 | **AUDITED** | `9b9f0e139277b705...` | md5=`jJNF+YheRgoL+kxXq7I7gw==` crc32c=`D5GBmg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2200.pt` | 0.0 | **AUDITED** | `4c9d0213d12434e3...` | md5=`ky+T/Wu7UMvoe6DWuBAxwQ==` crc32c=`/YX9OQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_325.pt` | 0.0 | **AUDITED** | `f50eb9e6a021a87b...` | md5=`zC+aMIQOUs6f1X2bppMxkg==` crc32c=`scvfYQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_15.pt` | 0.0 | **AUDITED** | `7155b60687dcfcce...` | md5=`U0NDiKCX5l0ZABWIBxlM+g==` crc32c=`mQvTsA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_450.pt` | 0.0 | **AUDITED** | `110ad50ca5fe812d...` | md5=`Q5DHEx4yxqh7xJT2TOIHsQ==` crc32c=`fyxOCw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3065.pt` | 0.0 | **AUDITED** | `5a425545a3179247...` | md5=`vulFWaL0FxIKsh+xcRktCQ==` crc32c=`XPD6Nw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_170.pt` | 0.0 | **AUDITED** | `2447a57ea4ef60c5...` | md5=`h66kO+mchSOkUYZ7BMZghQ==` crc32c=`WhPS9Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1830.pt` | 0.0 | **AUDITED** | `a0d41847a13e6c31...` | md5=`++stBiiqZeeNe0r/gnrAQA==` crc32c=`9OMWoA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_830.pt` | 0.0 | **AUDITED** | `582f35d9d444688b...` | md5=`HgnNFtjt8HAcQi89b9KmhA==` crc32c=`/PeSjw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_380.pt` | 0.0 | **AUDITED** | `0736447ea78f01bb...` | md5=`NFMiCSkUkOQnCA7cIHNsgQ==` crc32c=`DzOrUA==` |
| `dark_matter/hypergraph/results/deepmind_deepthink_review.md` | 0.01 | **AUDITED** | `80cc74384ac1e167...` | md5=`rdqUEby4Frm21kFlmiG+AA==` crc32c=`X94lJw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1185.pt` | 0.0 | **AUDITED** | `2d9ba3694d23b85f...` | md5=`sxoy1Y0pTL3YxPhyX3d5bw==` crc32c=`JDCZpw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3080.pt` | 0.0 | **AUDITED** | `1bfbcf2169a5f1e5...` | md5=`vXKqu1tygwJwtjmzZQkU4g==` crc32c=`2qtEPg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2015.pt` | 0.0 | **AUDITED** | `0bd93f6290a2e448...` | md5=`6Jzp0QJTs1HXJFUklv9//g==` crc32c=`04WLcA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3130.pt` | 0.0 | **AUDITED** | `c7d534a11441edbd...` | md5=`jH+UZRHZw46phJZO3wJqQA==` crc32c=`+EoWRw==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/rules.py` | 0.0 | **AUDITED** | `861a5d52556da93f...` | md5=`JqWxNbQlGRTEWQiUe5aglw==` crc32c=`R2Pv5Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_605.pt` | 0.0 | **AUDITED** | `d7d031679f625200...` | md5=`tXkAxZEZTESSzYwDtU4q3g==` crc32c=`lPRDnw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3000.pt` | 0.0 | **AUDITED** | `2963f5ce560ca85e...` | md5=`RejxPU3TLGbmnjWTZHV6kw==` crc32c=`h0hALg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1325.pt` | 0.0 | **AUDITED** | `12a279e560cbc75b...` | md5=`4GIVA25lI1tomOQjtCscHQ==` crc32c=`qSazbQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1505.pt` | 0.0 | **AUDITED** | `fb79da90a8e20af2...` | md5=`DelsSnUgljr3j6chr50AaA==` crc32c=`8yQ0+g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1690.pt` | 0.0 | **AUDITED** | `2d8f5dfffd629e6e...` | md5=`swQuTAEw8ZOZ97XFsQ6WCQ==` crc32c=`4wGxTA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1880.pt` | 0.0 | **AUDITED** | `02a3b759a3aca422...` | md5=`L8DD53njdjcLSA0tY0PRRg==` crc32c=`tcSzNg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2060.pt` | 0.0 | **AUDITED** | `5317873c5c9a7998...` | md5=`r7VGgzQT7WLLB2ag1Xwmjw==` crc32c=`A4FR6w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_875.pt` | 0.0 | **AUDITED** | `5ee97142374b7fe2...` | md5=`DLbBSXxOHBB8xWL2XNf0zg==` crc32c=`KHTFJQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_965.pt` | 0.0 | **AUDITED** | `02ef62f84a32917a...` | md5=`zbopEEuFZaRb8qWwq4otJw==` crc32c=`+7TmnQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_95.pt` | 0.0 | **AUDITED** | `1cd7e33f3a84900d...` | md5=`T3IJIn/45/Dp4DkxvqD1dQ==` crc32c=`5Z0ffg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2575.pt` | 0.0 | **AUDITED** | `65a7cdcfcee38827...` | md5=`a7E8VndtiqrkdygiA3z1bg==` crc32c=`Az2W3g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_40.pt` | 0.0 | **AUDITED** | `67fa616cda333c9f...` | md5=`tscRSV78WRM9WUeYe6XbYA==` crc32c=`VEVziw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_300.pt` | 0.0 | **AUDITED** | `dc28cd5ae3a2ac78...` | md5=`zELJNRVIeGas64UDSH0tTA==` crc32c=`WsopRA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1180.pt` | 0.0 | **AUDITED** | `9deb9eb2ff7cc07c...` | md5=`TFjwV7Dnrw+sl8aUuCN4xA==` crc32c=`xgFgsg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1355.pt` | 0.0 | **AUDITED** | `c2917521e0a0aa21...` | md5=`7BjE30AKckN85dOO17WUig==` crc32c=`mxOQ4w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2570.pt` | 0.0 | **AUDITED** | `0489cc288573c6fb...` | md5=`n/ZbyCFlyMzzG2uSuHKOLA==` crc32c=`4Qxvyw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2865.pt` | 0.0 | **AUDITED** | `173c23dd5c5edc5a...` | md5=`EehdxV04OI/XsxlpBxFdsQ==` crc32c=`8bOMlQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_855.pt` | 0.0 | **AUDITED** | `4792499f717e26cd...` | md5=`xAsWx4zmMkAKIW2hLK3YMw==` crc32c=`PQqloA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1130.pt` | 0.0 | **AUDITED** | `7da54c9c5a69a389...` | md5=`IqawGG5D3hA75/xF4a1tFQ==` crc32c=`hybFJA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_415.pt` | 0.0 | **AUDITED** | `97f87430efabb9fe...` | md5=`Z8dPM1qR5t94iOqeYuSU9A==` crc32c=`q68ZoQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1405.pt` | 0.0 | **AUDITED** | `9346e34bcd352a62...` | md5=`wlNe+HFhDleHSeGP6UtdFA==` crc32c=`kOLDFQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1110.pt` | 0.0 | **AUDITED** | `1512e7169f1e3faf...` | md5=`84DzI38dGQR70kOlBxn7Xg==` crc32c=`kF4EIA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1100.pt` | 0.0 | **AUDITED** | `c421c0d0867f45e9...` | md5=`rvYjewkew5L6NvKzkTrtnw==` crc32c=`m+Jkog==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_205.pt` | 0.0 | **AUDITED** | `81255bdbb557cd74...` | md5=`2NOfYxgR9e9q5RqlJB591g==` crc32c=`/zyXZg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2170.pt` | 0.0 | **AUDITED** | `ed74d8f933b76cc2...` | md5=`DT/OMmvb8ITMtSWtDw75YQ==` crc32c=`a/vGhg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1420.pt` | 0.0 | **AUDITED** | `80878028a7718d02...` | md5=`PcYwzQkFN5RUiKVq0M0csw==` crc32c=`Zav7BA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_550.pt` | 0.0 | **AUDITED** | `81488289c5e46465...` | md5=`fwv5Uyl/x9ntkXoT6uHchA==` crc32c=`JKVmiQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1095.pt` | 0.0 | **AUDITED** | `f6da88cad0be7da5...` | md5=`UJxSA28JY/bzklp4QBFrzg==` crc32c=`TEoOyg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_770.pt` | 0.0 | **AUDITED** | `ef36bf6e777466de...` | md5=`Mk0CHnDGyAgHZDecLZUTfw==` crc32c=`hslXCA==` |
| `dark_matter/hypergraph/processing/hypergraph/continuum_limits/__pycache__/__init__.cpython-310.pyc` | 0.0 | **AUDITED** | `b02488248b932acc...` | md5=`OHhibziY1gHG48BuXVCJIg==` crc32c=`k/UhQA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3175.pt` | 0.0 | **AUDITED** | `ec555be747f9accb...` | md5=`nnSswkvm/Cc5tvCjgUS3DA==` crc32c=`NIptWg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1340.pt` | 0.0 | **AUDITED** | `e86ca59483e9eaf1...` | md5=`ZLBuGx1IFodzjSEZ79URJg==` crc32c=`cp4JdA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1205.pt` | 0.0 | **AUDITED** | `52ab96b56c996eaa...` | md5=`aXSqFWc9ygVXorQHlnez5A==` crc32c=`3ZiFhg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1800.pt` | 0.0 | **AUDITED** | `250c6a9d3ad49218...` | md5=`wPjckzKTkaobi2lP7WrsJg==` crc32c=`6Ce3Jg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2445.pt` | 0.0 | **AUDITED** | `8db77a31f17975be...` | md5=`mfLq55mEDuKBlXirWvIZJw==` crc32c=`fD/Atw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2935.pt` | 0.0 | **AUDITED** | `3c6dcf3957404f56...` | md5=`j7f8N8waN3ltOsRG8kftyA==` crc32c=`tziZ8A==` |
| `dark_matter/hypergraph/processing/hypergraph/__init__.py` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_465.pt` | 0.0 | **AUDITED** | `e8e7996e108109b3...` | md5=`tXCqGezFVUT6pXVgqvjO7A==` crc32c=`HGSzFA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2165.pt` | 0.0 | **AUDITED** | `32bdfd851d603196...` | md5=`B07KnCjXVPJbRTtvv09lcQ==` crc32c=`gnZfEQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2480.pt` | 0.0 | **AUDITED** | `b5192e8714f474ae...` | md5=`JjTnWTCYvgzuDMHajlIyDA==` crc32c=`7Ry/ug==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1390.pt` | 0.0 | **AUDITED** | `dd1e72cb317af359...` | md5=`nI+G+Ho5mXmRIJE00AHQyA==` crc32c=`CjDv7g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2590.pt` | 0.0 | **AUDITED** | `5442b5e11f35c8ed...` | md5=`MqXFFQfWB6W5y4HQM9lORw==` crc32c=`hWYo1w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2750.pt` | 0.0 | **AUDITED** | `0f5436d237c28d20...` | md5=`A6sX9W/dEZ2/GHmzYdyQBg==` crc32c=`MflBEQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_425.pt` | 0.0 | **AUDITED** | `295316cf87eed1d9...` | md5=`D6KZ3C+3NzTWjF7teOODyg==` crc32c=`NphyHg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_165.pt` | 0.0 | **AUDITED** | `73c77a3d8c6c6349...` | md5=`Z4nMfDPFk2nXbJwiaVKH1g==` crc32c=`LCVPbw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_905.pt` | 0.0 | **AUDITED** | `3667f0b414098070...` | md5=`57KZ+aItKfDXQJJkUlkJwg==` crc32c=`xDZHEg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_310.pt` | 0.0 | **AUDITED** | `12a2922fd76e38f2...` | md5=`nM8KEgftBfdUdJMDKfTWZw==` crc32c=`0oMifg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1105.pt` | 0.0 | **AUDITED** | `dc4faa4875b208ae...` | md5=`hnDXoFChvQ5FsII2rdpUQw==` crc32c=`edOdtw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_540.pt` | 0.0 | **AUDITED** | `a10444931eb3880e...` | md5=`UC6afgAAEZ8+ZV/YcwElsg==` crc32c=`rOxtsw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_245.pt` | 0.0 | **AUDITED** | `793a5c878df0cca1...` | md5=`8DPGQLgehVodIzRjs5oGQA==` crc32c=`1cBWbA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1580.pt` | 0.0 | **AUDITED** | `ea4230d13315f404...` | md5=`pGhE9OWzrKIcwWRQGwclgw==` crc32c=`TPbJ/w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_25.pt` | 0.0 | **AUDITED** | `56e7bda5fded1da0...` | md5=`bYvL9MSxEQiCZd5BP10Drw==` crc32c=`yMekpg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1890.pt` | 0.0 | **AUDITED** | `31fd9ceaa84ea914...` | md5=`+Spfh3cQDp3MTvj4mib2Gw==` crc32c=`vnjTtA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_730.pt` | 0.0 | **AUDITED** | `85db74d70484cb22...` | md5=`VUvWaONcMRZqXugzO1sKRA==` crc32c=`rDWWAg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3155.pt` | 0.0 | **AUDITED** | `a0348cc9ec3eee6b...` | md5=`FeqIYOrkxM66LlH/zO1D4A==` crc32c=`I/KsXg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_750.pt` | 0.0 | **AUDITED** | `09383d32a18b7c48...` | md5=`JPCks7rXvcrkHOb04I3f8Q==` crc32c=`k7c3jQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_805.pt` | 0.0 | **AUDITED** | `282916bc50a54a74...` | md5=`BuEisyx7kIqGNS9+3f+MFg==` crc32c=`n79vkA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_610.pt` | 0.0 | **AUDITED** | `3376a5b6dcd6640c...` | md5=`QiyTKPsQrqsjvc/iRNYOgQ==` crc32c=`4sLeBQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2495.pt` | 0.0 | **AUDITED** | `b8561982b1c94d37...` | md5=`672v9Gw2h44G+1wHFoTcGQ==` crc32c=`BJEmLQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_45.pt` | 0.0 | **AUDITED** | `0ad97b3f480bb067...` | md5=`HwbDEcNOZsjgm6JHrSxd8g==` crc32c=`a19Kig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_355.pt` | 0.0 | **AUDITED** | `6172c2417378b020...` | md5=`hXsUTBHujUvst8PWKGoYdQ==` crc32c=`BgB11A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_340.pt` | 0.0 | **AUDITED** | `8454dda2973d3eb0...` | md5=`GmDJqG1WjUc09XLc+ILvlQ==` crc32c=`cDboTg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2100.pt` | 0.0 | **AUDITED** | `51d4faa26c86d1d8...` | md5=`E7eyF1d7qKiOXSgFcXdOWw==` crc32c=`Wc7lCA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3160.pt` | 0.0 | **AUDITED** | `ee05fa1b3a20c92d...` | md5=`LBeNFeRTsT7IhcMnVj3ltw==` crc32c=`3Qf0zQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1630.pt` | 0.0 | **AUDITED** | `ec87aad29cabeb1f...` | md5=`G2d3BmvIrQgf6vF2Yvb7Gg==` crc32c=`qZp0WA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1930.pt` | 0.0 | **AUDITED** | `00bc4be2407333fb...` | md5=`bVIxLrM9Vahy5Ush3vlzpg==` crc32c=`lyXhTw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_55.pt` | 0.0 | **AUDITED** | `a87b0a316d96d44c...` | md5=`c8oJ4zH23nMJzTdwUlFnnQ==` crc32c=`p0C11w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1215.pt` | 0.0 | **AUDITED** | `85c6b0dc39cb3372...` | md5=`oRy21paxGw+dq3ypcfhPGQ==` crc32c=`1iTlBA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1860.pt` | 0.0 | **AUDITED** | `f065a2f2deb0fafc...` | md5=`MC6eDOLetEpxQlUHnmw+hg==` crc32c=`0a70Kg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_400.pt` | 0.0 | **AUDITED** | `98180267f161d190...` | md5=`iHsxDiRsxJEZ+zvCgryzng==` crc32c=`3ZmEOw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1670.pt` | 0.0 | **AUDITED** | `70e75bb12c3f94ff...` | md5=`5QsbMry32/WGdqIhk6qiRg==` crc32c=`h2v2UA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3165.pt` | 0.0 | **AUDITED** | `3e7682c805ecf25b...` | md5=`7yMtgevFflH89H+YFa3AYA==` crc32c=`PzYN2A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2460.pt` | 0.0 | **AUDITED** | `9994683191101c49...` | md5=`Pr9SHeVM2uz8tEdrBk6vPA==` crc32c=`iXb4pg==` |
| `dark_matter/hypergraph/results/batch_final_summary.json` | 0.0 | **AUDITED** | `14b40901f29547d2...` | md5=`aZ2d3+mGVWa7r3jFkXfLrA==` crc32c=`HKJa/A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1965.pt` | 0.0 | **AUDITED** | `6c374503976c4001...` | md5=`udserogC1CLhs/11UyAvRA==` crc32c=`UFn60A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2985.pt` | 0.0 | **AUDITED** | `7976bd28eb25b40d...` | md5=`XosrakuKHB2uyF/v54mVQQ==` crc32c=`9h88Zg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_555.pt` | 0.0 | **AUDITED** | `ffaf3b38eee2a8a4...` | md5=`fwGs54kl/U2Ozx6JmPE5mQ==` crc32c=`2trwKQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_700.pt` | 0.0 | **AUDITED** | `53b88e846b2908b3...` | md5=`iiEs1olVKkoyOAV1PdKT7Q==` crc32c=`MQL9vQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2290.pt` | 0.0 | **AUDITED** | `02f07aaa33142950...` | md5=`Bfcg+W32qSYsMAQUCarS3g==` crc32c=`q9qZqw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1395.pt` | 0.0 | **AUDITED** | `20a58acda475f651...` | md5=`i/DjOcJNYgKQoe6qZB3kwA==` crc32c=`6AEW+w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1385.pt` | 0.0 | **AUDITED** | `6d655900790a7bb2...` | md5=`Av76WBgt1A9eGgOU3/ccMw==` crc32c=`4712eQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1275.pt` | 0.0 | **AUDITED** | `1b3fd915e78f007b...` | md5=`DhYoMDXmwe6i2jra69T2JQ==` crc32c=`762mCA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_140.pt` | 0.0 | **AUDITED** | `b361cd422f7206e8...` | md5=`+kKLKcs/3OBHvKHyEK5iLw==` crc32c=`xyS5Sg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2665.pt` | 0.0 | **AUDITED** | `8724558cb2549f82...` | md5=`vw6hD7/r/5xcqLJ/WDyBGA==` crc32c=`rMrubQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2420.pt` | 0.0 | **AUDITED** | `419f9287adb8456a...` | md5=`VMFN6G7yMq1Yujpk9scgfw==` crc32c=`p4d6rg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2700.pt` | 0.0 | **AUDITED** | `b9c8c60b47873728...` | md5=`p49x0S0BqeWPrzhOJJU51Q==` crc32c=`FLSjmw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1025.pt` | 0.0 | **AUDITED** | `817c248a39ce00da...` | md5=`8JmupBoLIO2ZscIxzpw11Q==` crc32c=`DW2rXA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_175.pt` | 0.0 | **AUDITED** | `1bbcf673627404d4...` | md5=`cYqf3qwOzZzSdVWH/S68Uw==` crc32c=`pGxEVQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_565.pt` | 0.0 | **AUDITED** | `f87ca6484fee73d2...` | md5=`mDb8golozaDtQApP05MUhQ==` crc32c=`R+2blg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_290.pt` | 0.0 | **AUDITED** | `59cc3f316d7d31a8...` | md5=`YEaazbdki0XQuvK5wTT34A==` crc32c=`3POI6A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2325.pt` | 0.0 | **AUDITED** | `4698f78f14841430...` | md5=`pDr8+4c0H/5a+p/iC1axRw==` crc32c=`awoyxw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_455.pt` | 0.0 | **AUDITED** | `c871b6c676e4ffc1...` | md5=`gc0W0ILAMpFZFzFVeMbCXg==` crc32c=`gVPYqw==` |
| `dark_matter/euclid/real_euclid_worker.py` | 0.02 | **AUDITED** | `67f44eb7b9189148...` | md5=`Fc2C48U9x36+ddKOLq2YuA==` crc32c=`WSksJA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2280.pt` | 0.0 | **AUDITED** | `bd828d7ce70ca610...` | md5=`7V/3hvtxZJots6BQKFCUSg==` crc32c=`oGb5KQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2915.pt` | 0.0 | **AUDITED** | `fc62bd4af011e859...` | md5=`TZZeLTaaYBhWpj3yMHbIcg==` crc32c=`oEBY9A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_615.pt` | 0.0 | **AUDITED** | `c771c249fb883ca4...` | md5=`4KQkV1PoZZjDWNuhdoZ1Bw==` crc32c=`HL1IpQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2600.pt` | 0.0 | **AUDITED** | `f9bcdfcb3b867b0e...` | md5=`WDZ94OMduHHG0os0PTU3iQ==` crc32c=`d3JUdA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3005.pt` | 0.0 | **AUDITED** | `7a4afdc9754f03b7...` | md5=`JSMB51/UvrWUyqEUx3TMrg==` crc32c=`ZXm5Ow==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2780.pt` | 0.0 | **AUDITED** | `0b93638772b57df8...` | md5=`TlISRrvIDbWc39dZkq8CLQ==` crc32c=`SVeniw==` |
| `dark_matter/hypergraph/results/brief/MFDM_Continuum_Limit_Paper.tex` | 0.01 | **AUDITED** | `16237d18844f808a...` | md5=`BOw0PVaehsZhOIccnoTJSg==` crc32c=`MOu1TA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_800.pt` | 0.0 | **AUDITED** | `7c838c78d473fa07...` | md5=`5w5phIkYlv9yngSXbL3B+Q==` crc32c=`YcD5MA==` |
| `dark_matter/hypergraph/processing/hypergraph/__pycache__/phase0_tensor_masking.cpython-310.pyc` | 0.0 | **AUDITED** | `9032a81e0223e254...` | md5=`Lqp25wCt+6TD31kU/R6bdg==` crc32c=`q0iiag==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1475.pt` | 0.0 | **AUDITED** | `3ed680f64b5988a4...` | md5=`4OYjQCI72QN71RbJIEACDw==` crc32c=`otfgmw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2790.pt` | 0.0 | **AUDITED** | `21e7f7d9259abda3...` | md5=`2qM+NGBbyzsUogpLzxCnow==` crc32c=`QuvHCQ==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/__pycache__/__init__.cpython-310.pyc` | 0.0 | **AUDITED** | `7fea65a30d36bcae...` | md5=`/fUR4pvtm0tH7U8ymwAUJw==` crc32c=`Re80JA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2795.pt` | 0.0 | **AUDITED** | `e25822b152bd3964...` | md5=`sb3rx8jdBGARvUy3muwsKA==` crc32c=`oNo+HA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1150.pt` | 0.0 | **AUDITED** | `6c43e1b0aaa0c3f5...` | md5=`/lXak3orQszV6PKfGRYtbw==` crc32c=`vq+GKA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2755.pt` | 0.0 | **AUDITED** | `72e3e66ad2f25ce2...` | md5=`3GzViWi8fsy1BNo71t+aXg==` crc32c=`08i4BA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1815.pt` | 0.0 | **AUDITED** | `67d122672a5675a1...` | md5=`JjnbTdxVBXiLEAF6ovo33g==` crc32c=`AaousQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3095.pt` | 0.0 | **AUDITED** | `a86ba1250533a535...` | md5=`lKag2SW3p5R9O+8C1A8eQQ==` crc32c=`MybdqQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1675.pt` | 0.0 | **AUDITED** | `3fea06d34e2f6714...` | md5=`h4uplECcntJjmP0I8Lhhhg==` crc32c=`ZVoPRQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2540.pt` | 0.0 | **AUDITED** | `d74a909918f92dc4...` | md5=`86iwtJ/dYhPMOVFw2Qv6Dg==` crc32c=`/cjOTQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_690.pt` | 0.0 | **AUDITED** | `019862f623a59f5d...` | md5=`BAfHX8F6mFk064BW2+3kHg==` crc32c=`tztcEQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2990.pt` | 0.0 | **AUDITED** | `e6b7c13d960c73e1...` | md5=`nyen0g29RwDSRo0somASwg==` crc32c=`H5Kl8Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3100.pt` | 0.0 | **AUDITED** | `94d19994b736fdb0...` | md5=`/QAOUSwQTKV4gU4I6HXR4A==` crc32c=`5I63wQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3170.pt` | 0.0 | **AUDITED** | `26c5aa2f71e2edc6...` | md5=`XtnwK/hWuaLX0DXPoYeSRw==` crc32c=`1ruUTw==` |
| `dark_matter/hypergraph/results/brief/interactive_n_body_clustering.html` | 0.01 | **AUDITED** | `df1ce98066c9ec98...` | md5=`dYJMhfBwatsdI6YIHcICtQ==` crc32c=`oC4RtQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2010.pt` | 0.0 | **AUDITED** | `2c161d1b1aade878...` | md5=`pu4Z2oTm9TlGVH1UrTVJAA==` crc32c=`MbRyZQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2065.pt` | 0.0 | **AUDITED** | `011db30309ec67b5...` | md5=`VbGet7sGfGV8BKX7ReobLw==` crc32c=`4bCo/g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1295.pt` | 0.0 | **AUDITED** | `6611fc75fb4ea187...` | md5=`X0/5SOQrl/25Y1QbvZGEIw==` crc32c=`i8fhFA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1900.pt` | 0.0 | **AUDITED** | `98fb8b4a88fa3b7b...` | md5=`QLV0wYoe2houmoF9355f6w==` crc32c=`i+FAyQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_720.pt` | 0.0 | **AUDITED** | `ffc049a946af9d24...` | md5=`7v2v57B/8ILvnt+Is1x4pg==` crc32c=`JHydOA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_850.pt` | 0.0 | **AUDITED** | `5cb3614e0bbe6349...` | md5=`hYOhF5biWoSvLJ6crDt/sA==` crc32c=`w3UzAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_30.pt` | 0.0 | **AUDITED** | `23e41bb64ea726ef...` | md5=`bvlnNrGxB4ABVhssZzZuIQ==` crc32c=`O8Ji+g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2260.pt` | 0.0 | **AUDITED** | `ee12ff99fb8c1b91...` | md5=`6RRypbQDMkyzXnvAIr1DGA==` crc32c=`xAy+NQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1825.pt` | 0.0 | **AUDITED** | `1ebaa7ecd5951f8c...` | md5=`vraw1VWsV/6p4DXYaO/Rng==` crc32c=`HW6PNw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2670.pt` | 0.0 | **AUDITED** | `32a77be74a468410...` | md5=`HAUb85KfCK0hzuZsiSeJHQ==` crc32c=`RUd3+g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_960.pt` | 0.0 | **AUDITED** | `a33138d0877d7756...` | md5=`RgW/FEubWzqDpMZvhMlVVQ==` crc32c=`BctwPQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1320.pt` | 0.0 | **AUDITED** | `57253d8ed57f385e...` | md5=`zCCZVmFUxYiSwS72pnplpA==` crc32c=`SxdKeA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1115.pt` | 0.0 | **AUDITED** | `f2be1c501f106325...` | md5=`BrZcQXT1v+WrEj9x+ZzHeg==` crc32c=`cm/9NQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2660.pt` | 0.0 | **AUDITED** | `82682b6b2eb52754...` | md5=`GvzI5Pfrih9TpcP+GAi+Qg==` crc32c=`TvsXeA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1040.pt` | 0.0 | **AUDITED** | `00a1aabe50c37126...` | md5=`6vik7ci+uOh8PhOGN/nroA==` crc32c=`1tURRQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_285.pt` | 0.0 | **AUDITED** | `2367045fc47d1edf...` | md5=`J/uBDm5Tz6pM1v99JCXpEA==` crc32c=`qsUVcg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1980.pt` | 0.0 | **AUDITED** | `6fd309a40065aca0...` | md5=`2Gy/eaF9MK2VIBGBj6T37A==` crc32c=`1gJE2Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_445.pt` | 0.0 | **AUDITED** | `b8e8ebcc8f6844fd...` | md5=`kjaB7xT6P6hGDUk4y0B7Ow==` crc32c=`CRrTkQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1125.pt` | 0.0 | **AUDITED** | `891788dd8456b664...` | md5=`+1jBaedM610R/kuKjCE0pg==` crc32c=`bqtcsw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2415.pt` | 0.0 | **AUDITED** | `cd6c756b17912875...` | md5=`6bBaFADPMn69hbvZCjvqcA==` crc32c=`WXIiPQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_625.pt` | 0.0 | **AUDITED** | `8b7a9522cef2400d...` | md5=`9qmZQtOmWl72QPM3DhM1uA==` crc32c=`gYojGg==` |
| `dark_matter/hypergraph/processing/hypergraph/batch_manager.py` | 0.01 | **AUDITED** | `34cb104d3407cfe0...` | md5=`F0QuDQcjiQE0f3YK3nkJSw==` crc32c=`GJyZJw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1745.pt` | 0.0 | **AUDITED** | `305390bddf614eeb...` | md5=`EiZ+2/rjGMGlGh4KAoiXuA==` crc32c=`GlhZLA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_820.pt` | 0.0 | **AUDITED** | `cc6a580ff9fa0498...` | md5=`yz3osOv9a5C/9OJ5Lybo5w==` crc32c=`dL6ZtQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_80.pt` | 0.0 | **AUDITED** | `848fbef4611fe964...` | md5=`97GIQfSsILrCG0Kbz+xpXg==` crc32c=`FpjZIg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2630.pt` | 0.0 | **AUDITED** | `43b10de1f17c7169...` | md5=`QiHfkpzzOJAlLCgg10KPVg==` crc32c=`a7b18g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1345.pt` | 0.0 | **AUDITED** | `8254509af928f10b...` | md5=`jefuuLe2q6AItEh+JvrZAA==` crc32c=`kK/wYQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_935.pt` | 0.0 | **AUDITED** | `d70c4cb7c3becae6...` | md5=`uAu15LZAN+PGXshB8ii/Yg==` crc32c=`WQEsrQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_840.pt` | 0.0 | **AUDITED** | `7a0b5b013632df82...` | md5=`05cntAROSvxUEQ1b/ktjMQ==` crc32c=`Szw4Og==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1600.pt` | 0.0 | **AUDITED** | `15516c9dfbcdb19a...` | md5=`yjaPJpqk53yuadIiEr5Rkw==` crc32c=`tV7V3g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1290.pt` | 0.0 | **AUDITED** | `d6d91d920386bdc9...` | md5=`dvs8cntHTmgeyyY8CEVYbg==` crc32c=`afYYAQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_345.pt` | 0.0 | **AUDITED** | `409d17a50f332b74...` | md5=`tCFgmzCc3pt1hkS4tN+eTA==` crc32c=`jkl+7g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_430.pt` | 0.0 | **AUDITED** | `e286b68899750575...` | md5=`A998lG0mcGvMO/WdZaTqEg==` crc32c=`QK7vhA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1010.pt` | 0.0 | **AUDITED** | `eee563b68f0f5dfd...` | md5=`JH30bDtqT18CfKYVqOIDLw==` crc32c=`85jzzw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1575.pt` | 0.0 | **AUDITED** | `f35a1226f29ea52c...` | md5=`xu4LcSMhz40SHcK40ylx2Q==` crc32c=`wREXdA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2455.pt` | 0.0 | **AUDITED** | `eea04f78ab47ecb4...` | md5=`KL4S0F9MgXk539T6IPMSCw==` crc32c=`d4OgNQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2130.pt` | 0.0 | **AUDITED** | `7a7cfe51d133f0b9...` | md5=`MHo1Her2ualkAsQeRVLYoQ==` crc32c=`RQpEjg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3085.pt` | 0.0 | **AUDITED** | `4b00dedae0c63cef...` | md5=`OJOr6Ds7kiwN37h4vKYpsw==` crc32c=`OJq9Kw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_570.pt` | 0.0 | **AUDITED** | `d955d0f52e6be1d9...` | md5=`Uh1+3/MZPjaaslOq+X9Dcg==` crc32c=`MdsGDA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1440.pt` | 0.0 | **AUDITED** | `e3e3c508bf3d410d...` | md5=`bO0SAXsCJgmWBczpFVUu3Q==` crc32c=`XCK4CA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2360.pt` | 0.0 | **AUDITED** | `200e9569a1d5da9b...` | md5=`TxrSD7FW9NkUdzlButY/dA==` crc32c=`p8pJ2g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_225.pt` | 0.0 | **AUDITED** | `df45acf45b748dda...` | md5=`+V32XKlv6IIeRIL4KfB+0A==` crc32c=`6kL34w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1300.pt` | 0.0 | **AUDITED** | `17310076efc75f1a...` | md5=`s4MOUZwPF/vQVAUFLG93Ig==` crc32c=`XG+LfA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2920.pt` | 0.0 | **AUDITED** | `ea1b5d85b7501c29...` | md5=`CWskg8vsWpEO0JqlJfV5Kw==` crc32c=`XrUAZw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1865.pt` | 0.0 | **AUDITED** | `fff331fdce26591a...` | md5=`Dm4nltZ9WUQw0OWHOp4iCg==` crc32c=`M58NPw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1015.pt` | 0.0 | **AUDITED** | `c928ad53eda54d6d...` | md5=`32YMHhOhZ7/uTTzQzSQ1HA==` crc32c=`EakK2g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_915.pt` | 0.0 | **AUDITED** | `6c67181e9ea77e25...` | md5=`xBBajwEN7txyMbf8FlfHVg==` crc32c=`TH9MKA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1230.pt` | 0.0 | **AUDITED** | `b4e2e14fcaebc1b8...` | md5=`9Hr30bvcTLtJaf7JxhlG7g==` crc32c=`I23dFQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2465.pt` | 0.0 | **AUDITED** | `0e09b0280ac07ffb...` | md5=`r2USKdi68Ei51fJJA/MkcQ==` crc32c=`a0cBsw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_735.pt` | 0.0 | **AUDITED** | `db8a780385a895e8...` | md5=`wMDlHH9cilHWrD9b2wHeaw==` crc32c=`UkoAog==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2595.pt` | 0.0 | **AUDITED** | `58bc39fda29cf91f...` | md5=`dbaybffX9RypGOrZkT9enA==` crc32c=`Z1fRwg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2355.pt` | 0.0 | **AUDITED** | `ddc78096f3a4337d...` | md5=`6lQOAG2GD7lt9/3ShW+t+Q==` crc32c=`WT8RSQ==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/oligon_defect_sim.py` | 0.0 | **AUDITED** | `8fff1fe05c662cea...` | md5=`Q7nxgktqKsJEJtaG32mMAQ==` crc32c=`ICl6Sg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_480.pt` | 0.0 | **AUDITED** | `a28b9e8821e266f9...` | md5=`KduxY+Va8KpNs/GO9be6rQ==` crc32c=`iGAGLw==` |
| `dark_matter/hypergraph/processing/hypergraph/oligon_simulations/__pycache__/oligon_mfdm_mapper.cpython-310.pyc` | 0.0 | **AUDITED** | `cbd20acf414dcc91...` | md5=`yXKEf80tIDmqht5rfw7KlQ==` crc32c=`9pQxlA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2315.pt` | 0.0 | **AUDITED** | `733cf989b2b9db96...` | md5=`80m88xALaUzMqA1mkx7etQ==` crc32c=`d86TQQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3050.pt` | 0.0 | **AUDITED** | `d833c3acc249f47c...` | md5=`VXvIn3fuM6b2n1mC7JYKpQ==` crc32c=`ogWipA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3035.pt` | 0.0 | **AUDITED** | `78f4d4928de7b12b...` | md5=`J3kp32PHvMkhe+Hpa2G1Eg==` crc32c=`eb0YvQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_160.pt` | 0.0 | **AUDITED** | `4205d624721bcaaf...` | md5=`HsppnDdFFFf0qJ/GW+P60w==` crc32c=`0lrZzw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1700.pt` | 0.0 | **AUDITED** | `94744ab41cd68d93...` | md5=`hmTBhJAxatPFxVVJlEI3TQ==` crc32c=`1pgiMQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1160.pt` | 0.0 | **AUDITED** | `365926dc1ee3f30a...` | md5=`mwc2G1IFvIZG+IPhY1dlew==` crc32c=`omsnrg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3145.pt` | 0.0 | **AUDITED** | `abf4f94824b87574...` | md5=`t2swaImB/tBo5dN3YGGffA==` crc32c=`KE7M3A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_460.pt` | 0.0 | **AUDITED** | `9deea8b85001f66e...` | md5=`sSQxBFPHuUfr0eqSFR+3AQ==` crc32c=`4hsltA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2110.pt` | 0.0 | **AUDITED** | `733e262538da6d3d...` | md5=`Tqwonv2iq47iqp23P8lSgw==` crc32c=`UnKFig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2160.pt` | 0.0 | **AUDITED** | `4264018509a32b2b...` | md5=`4ukr+GEISIIN0Uz7+l92MQ==` crc32c=`YEemBA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1020.pt` | 0.0 | **AUDITED** | `5017908ecf5948e6...` | md5=`iX2hll/nrzAhJHR4AgAK1A==` crc32c=`71xSSQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3125.pt` | 0.0 | **AUDITED** | `d85f27d087b0e45e...` | md5=`26XZywjRoZ6/N6WFTdA5IA==` crc32c=`EceP0A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_35.pt` | 0.0 | **AUDITED** | `457d9ec8d8f865fd...` | md5=`C7J7eu1yYDqAAqslSCQuIQ==` crc32c=`BNhb+w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_275.pt` | 0.0 | **AUDITED** | `0cbcaca48dedbb48...` | md5=`e9j15XKaCvi5r7ruqNEJwA==` crc32c=`SPc90w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1990.pt` | 0.0 | **AUDITED** | `1e2534f8a1e5e7db...` | md5=`9k4Dzg3AyTukqbMm5Uhb8A==` crc32c=`3b4kWw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1875.pt` | 0.0 | **AUDITED** | `db2c20c187df7e44...` | md5=`NTEQ+vqrDjAJcBxQrvSL3A==` crc32c=`OCNtvQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_970.pt` | 0.0 | **AUDITED** | `d60498946d984fc2...` | md5=`WoiWLQEoaGOyKRIovukF9A==` crc32c=`jYJ7Bw==` |
| `dark_matter/hypergraph/results/brief/wpp_computational_essay.md` | 0.01 | **AUDITED** | `db14754ee5182c5e...` | md5=`2HthLJBxGKmGCQ9RnVocrQ==` crc32c=`HgMAgA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1065.pt` | 0.0 | **AUDITED** | `28383f6849897a1a...` | md5=`3UCOTLrQmVO1NtUEVi3y7g==` crc32c=`I5wpVA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1540.pt` | 0.0 | **AUDITED** | `c735ae5891f7c379...` | md5=`59fy+1PNUUCAWqvxsvgtxg==` crc32c=`P+RP5w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2820.pt` | 0.0 | **AUDITED** | `4038f27bf4a6c1eb...` | md5=`KvGYbZRQrqKZe4Q30uBzPQ==` crc32c=`PXP3iA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2890.pt` | 0.0 | **AUDITED** | `fac0956174d1e002...` | md5=`j9SpE9FadnLRPLzmUWg+lQ==` crc32c=`fFRSHg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2310.pt` | 0.0 | **AUDITED** | `bb1b76d9c52b9d55...` | md5=`GzRRcO4C8nsMgHni5mUcVA==` crc32c=`lf9qVA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2680.pt` | 0.0 | **AUDITED** | `38862384efb78369...` | md5=`VnoJF99aot+eSOfB8+eDdQ==` crc32c=`KpFQZA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1705.pt` | 0.0 | **AUDITED** | `5275ce1af111de64...` | md5=`zRi0bDry7w7FG3BgvQMlLQ==` crc32c=`NKnbJA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1655.pt` | 0.0 | **AUDITED** | `9c2a7c287944e13e...` | md5=`ZfVOARI7l3T4S+C/s8BxYw==` crc32c=`ciLOQQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1585.pt` | 0.0 | **AUDITED** | `4c0e067da45e2537...` | md5=`wmy6aI+1YDmz0jWQ3+/Mjg==` crc32c=`rscw6g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3015.pt` | 0.0 | **AUDITED** | `8fc0b427db8630aa...` | md5=`0sRUBGXJpfR6ip1HMRQIEA==` crc32c=`bsXZuQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1960.pt` | 0.0 | **AUDITED** | `cc41b6d197e72708...` | md5=`C1oxRD07w0LVr36d6Cz8Lw==` crc32c=`smgDxQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_230.pt` | 0.0 | **AUDITED** | `c1edc51926867ab7...` | md5=`cDqTe8kbrS9iEohWBSN1lQ==` crc32c=`nHRqeQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2685.pt` | 0.0 | **AUDITED** | `d5cbfd57e719b444...` | md5=`nFxwe/nzBNvYKLTU/oxgog==` crc32c=`yKCpcQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1190.pt` | 0.0 | **AUDITED** | `3c6972cfce690f20...` | md5=`vtbIIfLmgXxx8r5/qYD/7w==` crc32c=`zb0AMA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1080.pt` | 0.0 | **AUDITED** | `4bb6e3e1a4d9e9f8...` | md5=`uUd+ulLz+0YjopAjYaFTzA==` crc32c=`pceXXQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2500.pt` | 0.0 | **AUDITED** | `7df7cfa38710768f...` | md5=`BAOMn6Kcq+qf7EP4EhQzIw==` crc32c=`0zlMRQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2810.pt` | 0.0 | **AUDITED** | `327a20c7db282ca1...` | md5=`FL3RuJZCJqC9bqJTPohtlg==` crc32c=`IbdWDg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3060.pt` | 0.0 | **AUDITED** | `8004559e350a498b...` | md5=`hD932vmp3UKKrycGaifVXQ==` crc32c=`vsEDIg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1740.pt` | 0.0 | **AUDITED** | `fee6e7e04f486a8b...` | md5=`0HWkIwzAii6/6jSFJUrulA==` crc32c=`+GmgOQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1635.pt` | 0.0 | **AUDITED** | `821ed15dcaf3a0fb...` | md5=`Hx+cZxHvgwZV+w9IsOvXaA==` crc32c=`S6uNTQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_210.pt` | 0.0 | **AUDITED** | `689d402ec034f2e5...` | md5=`gmeywEoZ9A5oe0Yb/VqH+w==` crc32c=`iQoK/A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_520.pt` | 0.0 | **AUDITED** | `676074e0a670ca32...` | md5=`gZ6lflObg03C0bDphVp6VA==` crc32c=`k27MPA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_710.pt` | 0.0 | **AUDITED** | `81e8aa33553dd01e...` | md5=`JFKWu6mYCC4Udnv4slzZlg==` crc32c=`uUv2hw==` |
| `dark_matter/hypergraph/processing/hypergraph/__pycache__/rate_limiter.cpython-310.pyc` | 0.0 | **AUDITED** | `98471d4775839e96...` | md5=`OuTRVfKRCCaNRTUYYcLxUg==` crc32c=`pngtuA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_530.pt` | 0.0 | **AUDITED** | `51f8da3cb81bb1d4...` | md5=`11ZpjU91ufp3FzqvfEGl/Q==` crc32c=`GyfHBg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_220.pt` | 0.0 | **AUDITED** | `0649c008a7150e5e...` | md5=`1h4LMBy7yMjHzdzFlpt+OQ==` crc32c=`FD1hQw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_845.pt` | 0.0 | **AUDITED** | `06f2646424861242...` | md5=`4GZr+LQRUwyPpEjiBjSMXg==` crc32c=`tUOumg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2435.pt` | 0.0 | **AUDITED** | `a5ff4676df330399...` | md5=`VEm1r4u33HaRPuh1wJgK6A==` crc32c=`TgrjOQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1660.pt` | 0.0 | **AUDITED** | `7acbcdfd67c945e4...` | md5=`9iKoIihMajkd6sag/b3X7w==` crc32c=`jNeW0g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1305.pt` | 0.0 | **AUDITED** | `4ac66c722d1840a3...` | md5=`3Ea4nKB1Uf7WB1XPWUZAwg==` crc32c=`vl5yaQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2235.pt` | 0.0 | **AUDITED** | `d049a9bacea6284d...` | md5=`hCd7ZoJ3DP3XZVVOki+cEg==` crc32c=`A3Clqg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2645.pt` | 0.0 | **AUDITED** | `549feb7a70446a2a...` | md5=`2KhuILMgQG1PUtAOg89GVQ==` crc32c=`u7IvaQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2305.pt` | 0.0 | **AUDITED** | `13852b13854244ac...` | md5=`m/aBgBlD9T/MFCXMFsl/fA==` crc32c=`fHLzww==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_510.pt` | 0.0 | **AUDITED** | `f7232d716a48248e...` | md5=`8V7L9dgGm8VSa6GUaduwlA==` crc32c=`Dlmngw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_885.pt` | 0.0 | **AUDITED** | `bda88e9eaaebe4d8...` | md5=`eqr02YUicac3vOqCgZEyDw==` crc32c=`ykbthA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1425.pt` | 0.0 | **AUDITED** | `0c5d9b34a78d1983...` | md5=`19cR/6LVdWJWT+6j8c2+ZQ==` crc32c=`h5oCEQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2770.pt` | 0.0 | **AUDITED** | `6c23bf3faa4fab64...` | md5=`St4zGL7foO7iPOeQQGrm4Q==` crc32c=`JoGAFQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1710.pt` | 0.0 | **AUDITED** | `75796f7ea4669452...` | md5=`tyIa2JQpQQP44LI7XVL+vA==` crc32c=`3SRCsw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_645.pt` | 0.0 | **AUDITED** | `598d168d7f66b06a...` | md5=`fxt7lXVr7vn1UsBxVD1jgA==` crc32c=`vgiClQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_235.pt` | 0.0 | **AUDITED** | `3dd0801a6c08be4d...` | md5=`eVGPN8fCjf2VrWqCahFlsg==` crc32c=`Ygv82Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1250.pt` | 0.0 | **AUDITED** | `cf658947190dc49f...` | md5=`gXsQl5gqEIr/255VCJBlDg==` crc32c=`GuSeGQ==` |
| `dark_matter/hypergraph/results/MEMORY.md` | 0.0 | **AUDITED** | `299ee8ba72403c57...` | md5=`6s5AG/gbdNcKuapsCpdH3A==` crc32c=`15mu8Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1445.pt` | 0.0 | **AUDITED** | `401727ecd9ee2ad6...` | md5=`a/OEOazmFEUfMcG6comndQ==` crc32c=`vhNBHQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2960.pt` | 0.0 | **AUDITED** | `76da3c70ed868a22...` | md5=`XeCbYmGaVKWiTN4d7mSRkw==` crc32c=`cESCbw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_360.pt` | 0.0 | **AUDITED** | `d0e8654c470fecc6...` | md5=`Yld36yIL7Be31+dy9CuOiQ==` crc32c=`ZUiIyw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1835.pt` | 0.0 | **AUDITED** | `9f0129af271bcb69...` | md5=`7y4ZdCYy0QvDJln7lkaalQ==` crc32c=`FtLvtQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_335.pt` | 0.0 | **AUDITED** | `ec3ab1aab096c369...` | md5=`5dKEVy7pa7q+opFD6XkmZw==` crc32c=`OYLUWw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1995.pt` | 0.0 | **AUDITED** | `0da4ed6a3f728d20...` | md5=`9LnjfIgT8P8IDAGdMqQiJQ==` crc32c=`P4/dTg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2525.pt` | 0.0 | **AUDITED** | `2eb0df7a757b7654...` | md5=`5peXWPMLWLgmn3lZMniVgw==` crc32c=`JnB0VA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3040.pt` | 0.0 | **AUDITED** | `585774aeba228f37...` | md5=`Bte80m/QWIc/v16f1gVYqA==` crc32c=`qbnCJg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2615.pt` | 0.0 | **AUDITED** | `a7ca28a8d853e175...` | md5=`Y7aMtIlsMJbjg7Rgyxcx5Q==` crc32c=`nv/N4w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2095.pt` | 0.0 | **AUDITED** | `e71051465284584a...` | md5=`V1RJEeQf4LO/+zETZ9abxg==` crc32c=`jmaPYA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1500.pt` | 0.0 | **AUDITED** | `a34625ee8e42228d...` | md5=`btUvs0nKJLqUxMO4w8xWVg==` crc32c=`ERXN7w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2620.pt` | 0.0 | **AUDITED** | `b9ed38d2af9c5717...` | md5=`+rbWnTSTPwNVMNGyjBn4Jg==` crc32c=`YAqVcA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_920.pt` | 0.0 | **AUDITED** | `650236d992d25027...` | md5=`DEs0mIiR6EN4kO80JOMkjg==` crc32c=`LzexNw==` |
| `dark_matter/hypergraph/processing/hypergraph/__pycache__/cost_monitoring.cpython-310.pyc` | 0.0 | **AUDITED** | `737348bdc6aa0d73...` | md5=`I6mJGT2fpHkZ54JtlABhhw==` crc32c=`I2AYbw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2555.pt` | 0.0 | **AUDITED** | `61a11be3ce9a0c8d...` | md5=`UYolepTVz0KMKoAP3D2K7A==` crc32c=`FEVX2g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1610.pt` | 0.0 | **AUDITED** | `42a7ce89393c313c...` | md5=`lc/Asy2O5VCRgoKjdTs1Ww==` crc32c=`vuK1XA==` |
| `dark_matter/hypergraph/processing/hypergraph/__pycache__/__init__.cpython-310.pyc` | 0.0 | **AUDITED** | `51d575c75c93338f...` | md5=`V7b8VRb5jtrCA3DuAjf0RA==` crc32c=`gmm5ig==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1840.pt` | 0.0 | **AUDITED** | `a67953637cd270f4...` | md5=`yExjYtSU0vZ6iTfPtrKiMw==` crc32c=`xtY1Lg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_410.pt` | 0.0 | **AUDITED** | `ed06d2ebce15f612...` | md5=`F/VGxwHfPILSJkSC41Cr/A==` crc32c=`VdCPAQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_125.pt` | 0.0 | **AUDITED** | `d507c85ed0722e1e...` | md5=`1CMtHLAA3K2VFzFZaCLqHA==` crc32c=`BtmOZQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_475.pt` | 0.0 | **AUDITED** | `87d9c5ca739ba4ba...` | md5=`aDhoPzVbhSH9l3j4TaMh7w==` crc32c=`lC24Lg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_470.pt` | 0.0 | **AUDITED** | `fcbad0d2e770940e...` | md5=`mxbdrcVwn9mLHoVNosAE9Q==` crc32c=`alIujg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1460.pt` | 0.0 | **AUDITED** | `b131b31dd8a36b8a...` | md5=`K4kDyXVhIFXX3DuWqsfC7Q==` crc32c=`S1p5DA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2240.pt` | 0.0 | **AUDITED** | `69c509bf681ea64d...` | md5=`yLQj1jMwYwt7PyGGFTQtHw==` crc32c=`03R/MQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_745.pt` | 0.0 | **AUDITED** | `e7a0dc233f9f02dc...` | md5=`h3ZphbVhAFcQWAN/HnBqUw==` crc32c=`5YGqFw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_780.pt` | 0.0 | **AUDITED** | `37b60c2d983b44aa...` | md5=`74ny+lGl6fsZiqJuHXnxfw==` crc32c=`ZPt/qQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_190.pt` | 0.0 | **AUDITED** | `b10b5777589f117c...` | md5=`hPyYvvwo3GRb04f2Hv0xtA==` crc32c=`MGjxbg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_195.pt` | 0.0 | **AUDITED** | `a2efa10af867ce67...` | md5=`RydyKcH8trizv/jNWNI+8w==` crc32c=`zhdnzg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1555.pt` | 0.0 | **AUDITED** | `f9b57016f4976aa4...` | md5=`afzLMpMVbotB0fERGDn7fg==` crc32c=`1mnWcA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2255.pt` | 0.0 | **AUDITED** | `b766f63ff067d096...` | md5=`HuynJy+uB40xe4fIfl3eEw==` crc32c=`Ovnmpg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2335.pt` | 0.0 | **AUDITED** | `46bba5f0e850ea4d...` | md5=`t655QsXc3g/AkoibWNS+NA==` crc32c=`YLZSRQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1760.pt` | 0.0 | **AUDITED** | `46221b518a30098b...` | md5=`FBvMyY9cVWvjmTYXKbiqjw==` crc32c=`7xFhPQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2115.pt` | 0.0 | **AUDITED** | `75101ed46047ad2d...` | md5=`qpOzVccIVqF7rY394WCgiA==` crc32c=`sEN8nw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_760.pt` | 0.0 | **AUDITED** | `f37b77b6f11320a3...` | md5=`n6E2KxNby9Kmt7K2CAYhMw==` crc32c=`DoBcMg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2725.pt` | 0.0 | **AUDITED** | `66cc7236d3930fab...` | md5=`OEzrDGimUiA320xw7K5gYw==` crc32c=`4f2big==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1790.pt` | 0.0 | **AUDITED** | `188ee36af8b77012...` | md5=`gzRajkU/mRMWCDo/UtIKgg==` crc32c=`gMdGow==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_330.pt` | 0.0 | **AUDITED** | `8551c8cc3abf6042...` | md5=`ttMD128Ny6TmKoQzlh39yg==` crc32c=`x/1C+w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_795.pt` | 0.0 | **AUDITED** | `5c570bba0cebc239...` | md5=`tTYhwNyAkqEo83ZL/42NrQ==` crc32c=`Es3iMw==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/__init__.py` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1935.pt` | 0.0 | **AUDITED** | `7a82e8965baddac6...` | md5=`Dh1UU3a4NK/KSUMlDnBW+g==` crc32c=`dRQYWg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3140.pt` | 0.0 | **AUDITED** | `6db7abd229b2ad70...` | md5=`B+8skRvpoV9yr3o7rNEFgA==` crc32c=`yn81yQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2695.pt` | 0.0 | **AUDITED** | `1c8c717ecbdd5ca1...` | md5=`pxYZCMgMKKqQrBHwraeLrQ==` crc32c=`wxzJ8w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2300.pt` | 0.0 | **AUDITED** | `5ba00f546414250e...` | md5=`PotMsPVWlnNVRBi4EDNXhw==` crc32c=`nkMK1g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_660.pt` | 0.0 | **AUDITED** | `440bfaaf6f72a22e...` | md5=`+OaLjiJg5bQM7A5xaYBlwQ==` crc32c=`VQl0sA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1950.pt` | 0.0 | **AUDITED** | `997206cef128e3cf...` | md5=`FOcgOTrb9P2+524Wamk0qA==` crc32c=`rqyiQw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_590.pt` | 0.0 | **AUDITED** | `5bd8b9b31f74e3bf...` | md5=`xQWjAkfwSo53QUkyhqArMQ==` crc32c=`W6Allw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2805.pt` | 0.0 | **AUDITED** | `a147c3ca62ef9bf6...` | md5=`CYfuhL0pKKggP/zyfBkg2g==` crc32c=`yDrPmQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1375.pt` | 0.0 | **AUDITED** | `ba6fccf96c9bf9b5...` | md5=`5jm1G1ciFJIOivBcPjE7Kg==` crc32c=`jGtR5w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1525.pt` | 0.0 | **AUDITED** | `1fb8f402b3a6502d...` | md5=`cgl3OHoRvmAQXHHdHcPsGg==` crc32c=`5Fz1/g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_895.pt` | 0.0 | **AUDITED** | `22e5dd3aa5c8224f...` | md5=`M4Xls/mtxX0XUVDVhHniZQ==` crc32c=`Qg/mvg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1240.pt` | 0.0 | **AUDITED** | `64bd5d2f716ddf45...` | md5=`xyZFP7prXwBVsU3ldttFGw==` crc32c=`EVj+mw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2370.pt` | 0.0 | **AUDITED** | `40073b210217301c...` | md5=`nwolaktOVeGChSTRcbHWig==` crc32c=`rHYpWA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1400.pt` | 0.0 | **AUDITED** | `1510f7a47378762b...` | md5=`3NEj1Cn6o7RIIChAdEVotQ==` crc32c=`ctM6AA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1155.pt` | 0.0 | **AUDITED** | `2fb7b4e1626998cc...` | md5=`bB69VzSmUHBCzCFSqWjnQQ==` crc32c=`XJ5/PQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_185.pt` | 0.0 | **AUDITED** | `c2c2d8e166aee3e9...` | md5=`SVuktuh7SF6tEanIo7E/Rg==` crc32c=`Rl5s9A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2155.pt` | 0.0 | **AUDITED** | `95ac41913193cac4...` | md5=`zanpccsL4EfgCAuIrMMR/g==` crc32c=`nrL+lw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1615.pt` | 0.0 | **AUDITED** | `9616d2464f40f0ef...` | md5=`5wgPbKpZtC8cPdNXl524Zw==` crc32c=`XNNMSQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2650.pt` | 0.0 | **AUDITED** | `e2cf6cff27327a4d...` | md5=`5GcQaSRwX27ldzF/c8qVvA==` crc32c=`Uj+2/g==` |
| `dark_matter/hypergraph/processing/hypergraph/__pycache__/gpu_accelerated_engine.cpython-310.pyc` | 0.0 | **AUDITED** | `a311f3379001d608...` | md5=`LMhvTKRk79H/3ingJzb1sg==` crc32c=`MfcWIw==` |
| `dark_matter/hypergraph/processing/hypergraph/gpu_accelerated_engine.py` | 0.0 | **AUDITED** | `035c78814a3e56a1...` | md5=`duCr05MQ+RyTwZnigJ3MZQ==` crc32c=`ot2Akw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2400.pt` | 0.0 | **AUDITED** | `831d6495ecca5aba...` | md5=`AnMzNQ3o43Hzlh+KGruH7A==` crc32c=`sP+7qg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3105.pt` | 0.0 | **AUDITED** | `43edcf274cae8e7d...` | md5=`D2QUVvQac9Pg5nkzkOe9Ww==` crc32c=`Br9O1A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2295.pt` | 0.0 | **AUDITED** | `ba0d4bf1d21d5ce6...` | md5=`H3KIa1PBJ2oNdQ12SQd91w==` crc32c=`Setgvg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1510.pt` | 0.0 | **AUDITED** | `46079b53f68b7d78...` | md5=`rWFxVRVp8GMherPP9TUhAg==` crc32c=`GqmtbQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2950.pt` | 0.0 | **AUDITED** | `8b7b5c5569491bb0...` | md5=`EmvX35ORdcv34n8ZfP7RMg==` crc32c=`bIAj6Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1455.pt` | 0.0 | **AUDITED** | `4e05adbc8441295e...` | md5=`+fF4y7U3bYi8hjF/yfE3Zg==` crc32c=`ta8hnw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_260.pt` | 0.0 | **AUDITED** | `3751161467a8e48e...` | md5=`60U/c6+Is08yn3pLU0mT0w==` crc32c=`PsGgSQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_350.pt` | 0.0 | **AUDITED** | `463a2ca7e4701d17...` | md5=`ckLtfWRXje+qFiYqsJeP+A==` crc32c=`+H/jdA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1910.pt` | 0.0 | **AUDITED** | `fe1c9a0f7bc5e761...` | md5=`fbsq6LcDhX1FshEpCmEyXw==` crc32c=`gF0gSw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2175.pt` | 0.0 | **AUDITED** | `00431c9bca9d916b...` | md5=`+W5cXG3snw8ONfgLB9oIpQ==` crc32c=`ico/kw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3070.pt` | 0.0 | **AUDITED** | `65d34fbe3a7f4cd0...` | md5=`6y6yUCrydUqlH8LnbIYO4g==` crc32c=`tX1joA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2860.pt` | 0.0 | **AUDITED** | `4308a3e434dfa0e0...` | md5=`0WWBustHSJkyLUPE4ECBOg==` crc32c=`E4J1gA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3090.pt` | 0.0 | **AUDITED** | `06f301f52d11a53d...` | md5=`B2M0JqfbIA9/+61loHkUfw==` crc32c=`0RckvA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2450.pt` | 0.0 | **AUDITED** | `f5239bb51227424a...` | md5=`t22nkv6aQ3nKG1U+cNN1ww==` crc32c=`lbJZIA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2605.pt` | 0.0 | **AUDITED** | `f72bacb7372b8931...` | md5=`FrMV9jW1fdDBVp88dvi8wg==` crc32c=`lUOtYQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2250.pt` | 0.0 | **AUDITED** | `ccd8ee16b3ccbd6f...` | md5=`wrurXNCUflLXKA8a92R2rg==` crc32c=`2Mgfsw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_200.pt` | 0.0 | **AUDITED** | `ba5069e31ee8a703...` | md5=`T68vRAalqBFLz0q9yaMqvw==` crc32c=`AUMBxg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2550.pt` | 0.0 | **AUDITED** | `f2fb267872f11078...` | md5=`IWTqiLEjvLJmdinH8dRfIQ==` crc32c=`9nSuzw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_685.pt` | 0.0 | **AUDITED** | `68ff595d590e9870...` | md5=`V1jKpX4wsmD2jnyRyXvtTQ==` crc32c=`wQ3Biw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_250.pt` | 0.0 | **AUDITED** | `babab46bf57185e5...` | md5=`Qrz5vm/GxCvbFxvAf57WxA==` crc32c=`o/bL9g==` |
| `dark_matter/hypergraph/results/brief/wpp_computational_essay.wl` | 0.01 | **AUDITED** | `228456060155d275...` | md5=`/loIDgBdoDVLxN9ksW5fRg==` crc32c=`4ieW7Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_630.pt` | 0.0 | **AUDITED** | `bf512ab14d5fe17b...` | md5=`xfmFRNDb79+0kLZsW1Z0BQ==` crc32c=`97y+gA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1120.pt` | 0.0 | **AUDITED** | `300db85a68961fed...` | md5=`TLkGZSif6+x004euzXDA0A==` crc32c=`jJqlpg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2975.pt` | 0.0 | **AUDITED** | `e1d428384d2a3166...` | md5=`FA9G76XXtgJP8m70UnzdUQ==` crc32c=`mckb+A==` |
| `dark_matter/euclid/euclid_validation_run.py` | 0.0 | **AUDITED** | `448dc2bb704b1574...` | md5=`6Jh7hnmcNScfspcrr6pg3w==` crc32c=`lR6/1w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1085.pt` | 0.0 | **AUDITED** | `1776faef453c1456...` | md5=`2qkDHqWLtPdoqWYwd7hzfw==` crc32c=`R/ZuSA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1595.pt` | 0.0 | **AUDITED** | `00fd2a844f31b6d3...` | md5=`Nte1a8PhdEq5fQLsI9Fvlw==` crc32c=`pXtQaA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1645.pt` | 0.0 | **AUDITED** | `f95cfa8345bcfa7e...` | md5=`16PtiZ0IPBFdfhq1/jKV+A==` crc32c=`eZ6uww==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_490.pt` | 0.0 | **AUDITED** | `29768cc7e3967a95...` | md5=`WEsng4quZVziTerzGXKc8w==` crc32c=`ACkNFQ==` |
| `dark_matter/hypergraph/processing/hypergraph/continuum_limits/vacuum_energy_calculator.py` | 0.0 | **AUDITED** | `c9aaf56a61b14121...` | md5=`O+N/I3F7KHxAdFfDzemASA==` crc32c=`+AsJiQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1030.pt` | 0.0 | **AUDITED** | `9b8ea801fea15d63...` | md5=`unT060UlQH0JpoE0kp3QGg==` crc32c=`5OAyyw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2905.pt` | 0.0 | **AUDITED** | `153c64149a802a2e...` | md5=`LhD+dtlx1KpYA9Ekc6xjIg==` crc32c=`q/w4dg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_3135.pt` | 0.0 | **AUDITED** | `5630d764cbce5f46...` | md5=`XOf7kbo15od3rLdhGt20bw==` crc32c=`GnvvUg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_925.pt` | 0.0 | **AUDITED** | `1e3be082e55579f6...` | md5=`AEq0QtlXOSie7EnUgYvgJg==` crc32c=`0Ugnlw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2850.pt` | 0.0 | **AUDITED** | `dc2eb8aa1ce05d51...` | md5=`1ekaLOumKyibNXMc6Pberg==` crc32c=`D0bUBg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1520.pt` | 0.0 | **AUDITED** | `f63cd01b70e74be7...` | md5=`V4qU3MsfXXQHHtKee9qB6w==` crc32c=`Bm0M6w==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_215.pt` | 0.0 | **AUDITED** | `461018a1e6d3ffb4...` | md5=`9Itq8Q+WtNI/bDWoieeVlg==` crc32c=`d3WcXA==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/__pycache__/rules.cpython-310.pyc` | 0.0 | **AUDITED** | `d33f30ed0e3b9459...` | md5=`SEKNF8pkmeU3fAC+voBOZg==` crc32c=`T0iKSA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2145.pt` | 0.0 | **AUDITED** | `ae70c095ed232db1...` | md5=`dPTXCBf0Rzaf4DLoLU24kQ==` crc32c=`lQ6eFQ==` |
| `dark_matter/hypergraph/processing/oligon_mfdm_mapper.py` | 0.01 | **AUDITED** | `8b0710b474fe95ec...` | md5=`0cCn3balr4BoEHHNghGgEg==` crc32c=`hksFYg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_85.pt` | 0.0 | **AUDITED** | `1cb25bb25e91fe62...` | md5=`E6cqTSIKiv4Qr5iwcx9IvQ==` crc32c=`KYLgIw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_60.pt` | 0.0 | **AUDITED** | `d3bcc1d71d05c215...` | md5=`b6lQ0D+rB/lqYByG9XhxvA==` crc32c=`yZb7wA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1310.pt` | 0.0 | **AUDITED** | `0d18766f50ab9b0d...` | md5=`wEijyTtCmYlcAOMg20+3Xg==` crc32c=`V9Pr/g==` |
| `dark_matter/hypergraph/results/brief/deepmind_scientific_audit_brief.md` | 0.01 | **AUDITED** | `606028f1962506b4...` | md5=`0GU5SFIU7t7iCZ2+G/drRA==` crc32c=`YiNMSA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2900.pt` | 0.0 | **AUDITED** | `09e0e7972fa7c2a0...` | md5=`21Es0zAEVXk+Dzy6w22A7Q==` crc32c=`Sc3BYw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2785.pt` | 0.0 | **AUDITED** | `52cc018eedda6ff9...` | md5=`pvoN5cl8iaCfg9aUc0pEnA==` crc32c=`q2Zeng==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1225.pt` | 0.0 | **AUDITED** | `2466ea80be4279a4...` | md5=`PAg7HkFOyCLHbcypPnYASA==` crc32c=`yuBEgg==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/__pycache__/multiway_rules.cpython-310.pyc` | 0.0 | **AUDITED** | `728cb0d649210f86...` | md5=`l7tPTVok4xavGvJsYb3GQA==` crc32c=`UvmUxA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2150.pt` | 0.0 | **AUDITED** | `86e053cf414abac9...` | md5=`TAJFt2gE6EoG1A3r4iu1sw==` crc32c=`fIMHgg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2910.pt` | 0.0 | **AUDITED** | `3f3e35c797be0e44...` | md5=`hrt3GJqi0cISaOobd4FVxw==` crc32c=`QnGh4Q==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_315.pt` | 0.0 | **AUDITED** | `aa1338167857f9b3...` | md5=`o0sHVOpDLo42N2g+3QIW+Q==` crc32c=`LPy03g==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2140.pt` | 0.0 | **AUDITED** | `a7afdec9707371f5...` | md5=`Zj0rkA7QxHZlBYrets6ucQ==` crc32c=`dz9nAA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2875.pt` | 0.0 | **AUDITED** | `ab84e9c5cf9618e2...` | md5=`atpbAP9cpKbvBlEA+r3QPg==` crc32c=`+g/sFw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_440.pt` | 0.0 | **AUDITED** | `e699086b61372f25...` | md5=`/aTw522AUoxJrva9jkSVjw==` crc32c=`92VFMQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_930.pt` | 0.0 | **AUDITED** | `76472accd820b1f3...` | md5=`W1p/byWdZz+CpRVFHwdHYA==` crc32c=`p366DQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_680.pt` | 0.0 | **AUDITED** | `ec1e08eb94f52537...` | md5=`8WxU7HkcFl9MLvYorrjUGQ==` crc32c=`P3JXKw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_535.pt` | 0.0 | **AUDITED** | `527f5de116cb860d...` | md5=`etJI3oFpmIpk0Ui9tEtctw==` crc32c=`5VhRpg==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_940.pt` | 0.0 | **AUDITED** | `e3d60d4b4b246517...` | md5=`f1Y3OXjF53Q6R53bjc8I/A==` crc32c=`ELUQuA==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1000.pt` | 0.0 | **AUDITED** | `a87e74efe03f2751...` | md5=`5nfpq8wipreIZEKoJBhlIw==` crc32c=`+CSTTQ==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1435.pt` | 0.0 | **AUDITED** | `69c031daa6dfd27e...` | md5=`QHktMeTGDk3IyYC1NAuhDg==` crc32c=`jCZikw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_1855.pt` | 0.0 | **AUDITED** | `c653f2ee690de37f...` | md5=`1rOIZGas5NkiIUXLHjBfnw==` crc32c=`L1usuQ==` |
| `dark_matter/hypergraph/processing/hypergraph/rewrite_rules/__pycache__/__init__.cpython-310.pyc` | 0.0 | **AUDITED** | `905d99e8279a9103...` | md5=`ebiKcg044YhF/dInOc/QNw==` crc32c=`aV2daw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_2210.pt` | 0.0 | **AUDITED** | `eb8298fdce0a164d...` | md5=`MSh7qn4pi0LO9d2RycGrOg==` crc32c=`9jmduw==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_385.pt` | 0.0 | **AUDITED** | `ecb96ce26dde7b4d...` | md5=`JfJwD/8Q9+l0IJXDfEd7+A==` crc32c=`8Uw98A==` |
| `dark_matter/hypergraph/checkpoints/checkpoint_step_995.pt` | 0.0 | **AUDITED** | `28b90f1573f26c86...` | md5=`4jB2EwKNPRPRMwVrzOF1Uw==` crc32c=`GYbOPA==` |

### des_y3/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `des_y3/` | N/A | **ABSENT** |  | Retracted from 2026-07-31 table; not in bucket |

### euclid_q1/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `euclid_q1/tile_102042288/EUC_MER_FINAL-CAT_TILE102042288-9EC67D_20241023T090937.150749Z_00.00.fits` | 103.58 | **PRESENT** |  |  |
| `euclid_q1/tile_102042289/EUC_MER_FINAL-CAT_TILE102042289-CFC681_20241021T014045.907769Z_00.00.fits` | 9.96 | **AUDITED** | `492f3331c0284987...` | md5=`t2R3s8WTEiABmF3FSos7Ug==` crc32c=`sbf7Eg==` |
| `euclid_q1/s8_joint_covariance.txt` | 0.0 | **AUDITED** | `5c8092dcf5184e74...` | md5=`kvforUX9QPWyBh4bXGjFnQ==` crc32c=`WOwgJQ==` |
| `euclid_q1/tile_102157301/EUC_MER_FINAL-CAT_TILE102157301-20BBA8_20241025T022824.601698Z_00.00.fits` | 31.99 | **AUDITED** | `c5053957612459b3...` | md5=`1MroKUDuitLQpMmvMYGRxQ==` crc32c=`bKNUXA==` |
| `euclid_q1/tile_102157301/EUC_MER_FINAL-MORPH-CAT_TILE102157301-216EF8_20241025T022823.960513Z_00.00.fits` | 7.13 | **AUDITED** | `97306d5896f9a260...` | md5=`PuZiKbuMmmoVS0PP904aWA==` crc32c=`z6sN0A==` |
| `euclid_q1/tile_102042288/EUC_MER_FINAL-MORPH-CAT_TILE102042288-AF209C_20241023T090936.673861Z_00.00.fits` | 23.09 | **AUDITED** | `33b943d85eb8bb2a...` | md5=`ZYgy5k+jlaDcpEzgoeSJ7w==` crc32c=`uwinSw==` |
| `euclid_q1/tile_102042288/EUC_MER_FINAL-CUTOUTS-CAT_TILE102042288-F1AEFD_20241021T090407.239664Z_00.00.fits` | 10.72 | **AUDITED** | `23065d808b031627...` | md5=`A3EKo1qxuKRv+SSxO1pIQQ==` crc32c=`5o/M/A==` |
| `euclid_q1/s8_joint_means.txt` | 0.0 | **AUDITED** | `b1e0aafd515bc1a2...` | md5=`FNCu8wh2eEri2IKcr/beCQ==` crc32c=`2ZFA5A==` |
| `euclid_q1/tile_102042289/EUC_MER_FINAL-CUTOUTS-CAT_TILE102042289-973122_20241021T002843.080044Z_00.00.fits` | 1.03 | **AUDITED** | `4a584a4120510f64...` | md5=`ycMv38BaL59ttfEVJjj3QA==` crc32c=`KhJ1Qw==` |
| `euclid_q1/tile_102042289/EUC_MER_FINAL-MORPH-CAT_TILE102042289-FFA8A6_20241021T014044.896244Z_00.00.fits` | 2.22 | **AUDITED** | `c1bdc6adc70519ba...` | md5=`ty2L8q2Dr7gMIEuuul7UtQ==` crc32c=`wPn1pw==` |
| `euclid_q1/README.md` | 0.0 | **AUDITED** | `a88016cc7f9df792...` | md5=`t1neEd9uPLtrgSEM4wbrsw==` crc32c=`p8p9/g==` |
| `euclid_q1/tile_102157301/EUC_MER_FINAL-CUTOUTS-CAT_TILE102157301-33897_20241025T005223.092706Z_00.00.fits` | 3.31 | **AUDITED** | `8ae5e9e6e160d319...` | md5=`COOE2FlS85PheSrRl4pTKA==` crc32c=`/qsl5Q==` |

### formal_verification/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `formal_verification/lean_oracle_v5.tar.gz` | 32.38 | **QUARANTINED** |  | Source audit pending WP-B; binary unverifiable |

### ipta_dr2/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `ipta_dr2/` | N/A | **ABSENT** |  | Retracted and DEFERRED per T0 decision DL-2 |

### mcmc_chains/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `mcmc_chains/chains/cooper_s10_g75_3_iter04_chain01.npz` | 0.03 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter04_chain03.npz` | 0.03 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter02_chain00.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter02_chain02.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter03_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter02_chain00.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter01_chain00.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g120_39_iter01_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter01_chain01.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter04_chain02.npz` | 0.03 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g120_39_iter01_chain00.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter01_chain02.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter03_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter01_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter02_chain00.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter03_chain02.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g120_39_iter01_chain02.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter03_chain02.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter02_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter03_chain00.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter04_chain00.npz` | 0.03 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter03_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter01_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter02_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter01_chain01.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter03_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter03_chain00.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter01_chain02.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter02_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_3_iter02_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter02_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter02_chain01.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter02_chain02.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter02_chain02.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter01_chain03.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g120_39_iter01_chain03.npz` | 0.02 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g75_29_iter01_chain00.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter01_chain00.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter01_chain02.npz` | 0.01 | **PRESENT** |  |  |
| `mcmc_chains/chains/cooper_s10_g63_32_iter01_chain01.npz` | 0.01 | **PRESENT** |  |  |

### mcmc_posteriors/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `mcmc_posteriors/posterior_cooper_s10_g120_39.json` | 0.0 | **AUDITED** | `52c95e66e5e01945...` | md5=`V7geWYyDsX6rTPXd64ubaw==` crc32c=`CNoW4Q==` |
| `mcmc_posteriors/bayesian_model_comparison.json` | 0.0 | **AUDITED** | `011a33d359dbe45d...` | md5=`I1huj2A58M+qDcCVpGnagg==` crc32c=`R4nGpA==` |

### nanograv_15yr/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `nanograv_15yr/output.json` | 0.0 | **AUDITED** | `ebef3c61c9f9b0a4...` | md5=`gwW9vA3KCEoqx5zQIGw+4g==` crc32c=`fQG9bw==` |
| `nanograv_15yr/input.json` | 0.0 | **AUDITED** | `14061379a118b64e...` | md5=`9vVS6D+6IakaCoBtRUPTAg==` crc32c=`rCPXPw==` |
| `nanograv_15yr/15yr_emp_distr.json` | 26.0 | **AUDITED** | `5d5e5a8377741843...` | md5=`1VrOZoq+3hQOaWDwJfBdnA==` crc32c=`SPsdlg==` |

### planck_2018/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/check_param` | 0.06 | **AUDITED** | `6f1a480375631e06...` | md5=`Z9yQRvkko+3zR4dUuEoyVg==` crc32c=`wEsv1w==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lmax` | 0.01 | **AUDITED** | `a56f3cb632cdd3b0...` | md5=`bqwJn+r5D8g9d2R0cV20jA==` crc32c=`+sZSZA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/_mdb` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/cl_cmb_plik_v22.dat` | 0.04 | **AUDITED** | `dac0d9d493213e77...` | md5=`aQtrcIVyvwBIbbMlDqmI2A==` crc32c=`sKQUKg==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/_mdb` | 0.0 | **AUDITED** | `e3b0c44298fc1c14...` | md5=`1B2M2Y8AsgTpgAmY7PhCfg==` crc32c=`AAAAAA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/blmin.dat` | 0.02 | **AUDITED** | `325b351cbf8f6945...` | md5=`dRvvHg5Wq8Ei2AfoDDyIBg==` crc32c=`eT1LgQ==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/bweight.dat` | 0.18 | **AUDITED** | `8afcbd8bad769e2d...` | md5=`xxYSkjzj8Cc5RAM0RcnFGQ==` crc32c=`M1naww==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_mdb` | 0.0 | **AUDITED** | `04198fe177773534...` | md5=`nHzQlaHy+3VoEMFKOWOyDw==` crc32c=`WS0D9Q==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lmax` | 0.01 | **AUDITED** | `f9c99156a4c02968...` | md5=`Xhw9J3pwpHYesbKPsQcKQA==` crc32c=`vpdPow==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/c_matrix_plik_v22.dat` | 2.87 | **AUDITED** | `ad90378c50bd6784...` | md5=`gfMYHsnIXXEUs6PPZdUR4g==` crc32c=`u8tIOA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/_mdb` | 0.0 | **AUDITED** | `1809ef0dd82f6c47...` | md5=`iV2q9D7KUv8b2Qx7osWw5w==` crc32c=`onaT0A==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/c_matrix_plik_v22.dat` | 2.87 | **AUDITED** | `ad90378c50bd6784...` | md5=`gfMYHsnIXXEUs6PPZdUR4g==` crc32c=`u8tIOA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/blmax.dat` | 0.02 | **AUDITED** | `c28ade0fa5270c7e...` | md5=`MOgoT7fs+P1lZNYLEK7arg==` crc32c=`vpFWKA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/bweight.dat` | 0.18 | **AUDITED** | `8afcbd8bad769e2d...` | md5=`xxYSkjzj8Cc5RAM0RcnFGQ==` crc32c=`M1naww==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/has_cl` | 0.01 | **AUDITED** | `264d74648124b54c...` | md5=`a7L2nI23+RtyFVL0FdcmhQ==` crc32c=`RSo0XA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/bf_lite_plikTTTEEE_v22b_lowl_simall.minimum.theory_cl` | 0.2 | **AUDITED** | `a6758abb574bba94...` | md5=`0iECRCJ0szD6BwVgc7lfhg==` crc32c=`Clo2UQ==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/has_cl` | 0.01 | **AUDITED** | `c89b88124927721d...` | md5=`109oUlDIg2cSz/G1ixyXkA==` crc32c=`oa90jg==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_external/cl_cmb_plik_v22.dat` | 0.04 | **AUDITED** | `dac0d9d493213e77...` | md5=`aQtrcIVyvwBIbbMlDqmI2A==` crc32c=`sKQUKg==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/blmax.dat` | 0.02 | **AUDITED** | `c28ade0fa5270c7e...` | md5=`MOgoT7fs+P1lZNYLEK7arg==` crc32c=`vpFWKA==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/check_param` | 0.02 | **AUDITED** | `ae44c62d0d1b5df1...` | md5=`qmYeqij8iGLM6u6Vpsk2RA==` crc32c=`7nE07A==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/bf_lite_plikTTTEEE_v22b_lowl_simall.minimum.theory_cl` | 0.2 | **AUDITED** | `a6758abb574bba94...` | md5=`0iECRCJ0szD6BwVgc7lfhg==` crc32c=`Clo2UQ==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/lkl_0/_mdb` | 0.0 | **AUDITED** | `04198fe177773534...` | md5=`nHzQlaHy+3VoEMFKOWOyDw==` crc32c=`WS0D9Q==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TT.clik/clik/_mdb` | 0.0 | **AUDITED** | `287cbb84f317c933...` | md5=`hF4buUbw4NrpD5TMiDSHNQ==` crc32c=`juNraQ==` |
| `planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/blmin.dat` | 0.02 | **AUDITED** | `325b351cbf8f6945...` | md5=`dRvvHg5Wq8Ei2AfoDDyIBg==` crc32c=`eT1LgQ==` |
| `planck_2018/` | N/A | **ABSENT** |  | Retracted from 2026-07-31 table; pending P1 acquisition |

### proofs/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `proofs/GeneratedK3.lean` | N/A | **ABSENT** |  | Retracted from 2026-07-31 table; file does not exist |

### publications/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `publications/paper_figures/budget_projection.pdf` | 0.03 | **AUDITED** | `4cba89039b093595...` | md5=`RenXYcddZdjvsZdZmkOnjA==` crc32c=`BL5g0A==` |
| `publications/paper_figures/chi2_convergence.pdf` | 0.03 | **AUDITED** | `0b38b4b238a78930...` | md5=`0uXenld9IDa/zRhCNyvtQg==` crc32c=`4OyMOg==` |
| `publications/paper_figures/parameter_evolution.pdf` | 0.03 | **AUDITED** | `ac15d552d090c71e...` | md5=`p+Dx5ySvKaEm7ueLtLwbhA==` crc32c=`Pq96Yg==` |
| `publications/paper_figures/dual_track_corner.png` | 0.15 | **AUDITED** | `a4d6e1e2b0c151c4...` | md5=`vCSPW5Gu95KWa2p3HCk4QQ==` crc32c=`1/BwOQ==` |
| `publications/paper_figures/dual_track_corner.pdf` | 0.55 | **AUDITED** | `8d1181c00c417417...` | md5=`onuuC7YTCepQtGsNwkdpwQ==` crc32c=`nFWbYA==` |
| `publications/paper_figures/chi2_convergence.png` | 0.22 | **AUDITED** | `0aeaca51dcd0c08b...` | md5=`bVHkDO5YekfoRdDhxggf+Q==` crc32c=`B1iquQ==` |
| `publications/SocrateAI_K3_T2_Discovery_Final.pdf` | 0.77 | **QUARANTINED** |  | F5b claim status pending audit WP-A |
| `publications/paper_figures/budget_projection.png` | 0.18 | **AUDITED** | `544f2f1a3471e568...` | md5=`2aKe/LIVS88dqXZTJWBLcg==` crc32c=`rGMOXw==` |
| `publications/paper_figures/spectral_sieve.png` | 0.22 | **AUDITED** | `b6f474c84ff5adde...` | md5=`iiv4jfSRmKNsTQBSUpfr3Q==` crc32c=`2993ng==` |
| `publications/paper_figures/hodge_diamond.png` | 0.15 | **AUDITED** | `862f237789fcefb6...` | md5=`+FXTYsVy8ZljEJoJmo5FIg==` crc32c=`GkjVgg==` |
| `publications/paper_figures/parameter_evolution.png` | 0.32 | **AUDITED** | `5a99ec9c807e656f...` | md5=`IU0qRvgJ3EE4gpm/XjA54w==` crc32c=`tevzcA==` |
| `publications/paper_figures/spectral_sieve.pdf` | 0.03 | **AUDITED** | `a53d0d77fed12bf4...` | md5=`GoBqrMc3Tsq40Msa+8h+6Q==` crc32c=`tQc8lg==` |
| `publications/paper_figures/hodge_diamond.pdf` | 0.02 | **AUDITED** | `53beaa00184752f0...` | md5=`9DpDsy5sijuszYTe40SH5g==` crc32c=`I/VfCA==` |
| `publications/paper_artifacts_v5.tar.gz` | 3.3 | **AUDITED** | `d85513821dfe552a...` | md5=`DpNas3lG9QsFLyEaQyxD6Q==` crc32c=`0idI9g==` |

### stream2_cy4_ml/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `stream2_cy4_ml/Data/Transverse_WS_8B.txt.zip` | 21.13 | **AUDITED** | `7c63db87aa326281...` | md5=`c4qGnD9jqUOs+lwAxYRoZw==` crc32c=`grCAIg==` |
| `stream2_cy4_ml/Data/Partition/PartitionDataB.zip` | 11.78 | **AUDITED** | `1d268144561c6fb2...` | md5=`FGmy5bn8e4ypk7zyAB1DZQ==` crc32c=`/4ESNg==` |
| `stream2_cy4_ml/README.md` | 0.0 | **AUDITED** | `48c52cb1bf6cbb75...` | md5=`9m1iq5+a4V44vX9yGC9AXw==` crc32c=`2QZ6EA==` |
| `stream2_cy4_ml/Data/Transverse_WS_8A.txt.zip` | 13.3 | **AUDITED** | `1ef7b4499ee4c03a...` | md5=`T58lOZOKY2HyGVVEobObsw==` crc32c=`WMS6+w==` |
| `stream2_cy4_ml/Data/Transverse_WS_7.txt.zip` | 4.87 | **AUDITED** | `9eaa5a631db5a8fb...` | md5=`rNSTuW5FqMsQ0kipVDSkCQ==` crc32c=`SS5oMA==` |
| `stream2_cy4_ml/Definitions.py` | 0.02 | **AUDITED** | `ddfe4d13288ffc22...` | md5=`Y527suidENjxuy+CBvPXrg==` crc32c=`28MlqQ==` |
| `stream2_cy4_ml/SR.py` | 0.0 | **AUDITED** | `f055997b4922174a...` | md5=`NkgmnPSRgdVW26CiXuSYjA==` crc32c=`I3oCfA==` |
| `stream2_cy4_ml/PCA.py` | 0.01 | **AUDITED** | `731a53e4e90538f5...` | md5=`HX0LcV7IC+VFQHDAAtYKMg==` crc32c=`neRLaw==` |
| `stream2_cy4_ml/Machine_Learning_Fourfolds.py` | 0.01 | **AUDITED** | `5388803b2442d7e3...` | md5=`KQRKWHbShhZ2vc4IgdzhVQ==` crc32c=`2Wv0gg==` |
| `stream2_cy4_ml/Example_Notebook.ipynb` | 0.01 | **AUDITED** | `cb3517b6f5274fa3...` | md5=`IXZFwIOPtwON5GnwD02EtA==` crc32c=`b2KZRQ==` |
| `stream2_cy4_ml/Data/Partition/PartitionDataA.zip` | 13.52 | **AUDITED** | `2cb0305335e81d92...` | md5=`cVp/1teQONey1qq5NdSUrg==` crc32c=`O5+Ulw==` |
| `stream2_cy4_ml/WeightClassification.py` | 0.01 | **AUDITED** | `5d2733c558dd9c92...` | md5=`c1H+/0A6oIGMJS4v3yYivw==` crc32c=`kjAhFw==` |
| `stream2_cy4_ml/Data_Analysis_Fourfolds.py` | 0.01 | **AUDITED** | `9a684a1cadbd51c9...` | md5=`nRkycGA1MZ2gpT9/oJ25qQ==` crc32c=`tEt1oQ==` |
| `stream2_cy4_ml/Data/5dTransWH.all.gz` | 22.62 | **AUDITED** | `093691618989ef57...` | md5=`cBtwl1bnALytzlKUMQtfzQ==` crc32c=`aCjlgQ==` |

### stream3_desi_dr1/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `stream3_desi_dr1/desi_2024_gaussian_bao_ALL_GCcomb_cov.txt` | 0.0 | **AUDITED** | `bbafa9074b51cf1a...` | md5=`Dx0Q4uprsX8PdK1+n99heg==` crc32c=`limZzQ==` |
| `stream3_desi_dr1/sdss_DR16_LYxQSO_BAO_DMDHgrid.txt` | 0.18 | **AUDITED** | `653e2cea43a742d1...` | md5=`zWnYIsXA+Pu1fH1q7D1F+A==` crc32c=`MWA3hA==` |
| `stream3_desi_dr1/sdss_DR12Consensus_bao.dat` | 0.0 | **AUDITED** | `fc43f1cd9c815bb5...` | md5=`6oXRFjy1rntAwksOn0ILAQ==` crc32c=`sOMzaQ==` |
| `stream3_desi_dr1/sdss_DR16_ELG_FSBAO_DMDHfs8gridlikelihood.txt` | 57.54 | **AUDITED** | `399439b0be94678e...` | md5=`6JKMiFNWLdCFzqWrSg3rLQ==` crc32c=`xCEpcg==` |
| `stream3_desi_dr1/sdss_DR16_LRG_BAO_DMDH.dat` | 0.0 | **AUDITED** | `b3317e7590799fad...` | md5=`x1zZ+5dSC+ou3569FxsNlw==` crc32c=`ykzc5Q==` |
| `stream3_desi_dr1/desi_2024_eboss_gaussian_bao_Lya_GCcomb_cov.txt` | 0.0 | **AUDITED** | `afb75cc336706698...` | md5=`I95H1gSBEAWv2zSl/5XCUw==` crc32c=`YL2Ivw==` |
| `stream3_desi_dr1/sdss_DR16_ELG_BAO_DVtable.txt` | 0.02 | **AUDITED** | `ebbd6b7a2946cf19...` | md5=`X2D28FLJ6gSG887/ODMClg==` crc32c=`byFMKA==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG_GCcomb_z0.4-0.6_mean.txt` | 0.0 | **AUDITED** | `ea7ce09ebd710d06...` | md5=`K78JVlPUO8ducq0MALOACg==` crc32c=`9YjRDw==` |
| `stream3_desi_dr1/sdss_DR12_LRG_BAO_DMDH.dat` | 0.0 | **AUDITED** | `ccdbe5ad44016ea0...` | md5=`eZ1SbqkvMAgR6SA0pye8Og==` crc32c=`dKAVew==` |
| `stream3_desi_dr1/BAO_consensus_covtot_dM_Hz.txt` | 0.0 | **AUDITED** | `05c04829c8edc117...` | md5=`Fnzy7UIcM3ol/vhc73c+Uw==` crc32c=`+B69zg==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_ELG_LOPnotqso_GCcomb_z1.1-1.6_mean.txt` | 0.0 | **AUDITED** | `cb8e5aecec6e4b58...` | md5=`ubY9xOHRF1KlXQL66N8Yrw==` crc32c=`eGUTZw==` |
| `stream3_desi_dr1/sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8.dat` | 0.0 | **AUDITED** | `cddd6cbbca7dadc9...` | md5=`acZLvl9yI9hwRmXDfr709Q==` crc32c=`OjwmbQ==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG+ELG_LOPnotqso_GCcomb_z0.8-1.1_mean.txt` | 0.0 | **AUDITED** | `96219da1f1877c71...` | md5=`v9MFkMFFRXbFDvwDwA0LQw==` crc32c=`lwMkDQ==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG_GCcomb_z0.6-0.8_mean.txt` | 0.0 | **AUDITED** | `6ce4744f4772f84a...` | md5=`Uy+0jiKsVIz1n1gTfzWsbw==` crc32c=`cP37BQ==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG_GCcomb_z0.4-0.6_cov.txt` | 0.0 | **AUDITED** | `1fc0b21fd34a0e19...` | md5=`nzUtHaOYo79tmkxp8+ej0Q==` crc32c=`aWhqug==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG+ELG_LOPnotqso_GCcomb_cov.txt` | 0.0 | **AUDITED** | `8c8f5270dc3db24c...` | md5=`hI50YSmDkbT9CcvFxqC26Q==` crc32c=`RTnoAw==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt` | 0.0 | **AUDITED** | `252a143274c8a07c...` | md5=`xY2+Sy0MvSsmHmTIXNIRpw==` crc32c=`2uugGQ==` |
| `stream3_desi_dr1/sdss_DR12_LRG_BAO_DMDH_covtot.txt` | 0.0 | **AUDITED** | `fd2a67856f0ffa72...` | md5=`mPU4eODAC4HHRyhD2F+YWA==` crc32c=`oOR+qw==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt` | 0.0 | **AUDITED** | `9ac154ab583ce759...` | md5=`nC0sAp581YViy1ub8qv1/w==` crc32c=`fVnO6A==` |
| `stream3_desi_dr1/README.md` | 0.0 | **AUDITED** | `87444c7e5303c4fb...` | md5=`2qml5i//oaylNQgxERoeVg==` crc32c=`4GiuHw==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG+ELG_LOPnotqso_GCcomb_z0.8-1.1_cov.txt` | 0.0 | **AUDITED** | `6ab34a65089f798b...` | md5=`73uBFRBBoC6c9DWBhpXB0A==` crc32c=`jQ9I6A==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG_GCcomb_z0.6-0.8_mean.txt` | 0.0 | **AUDITED** | `6d2f38d0727b2aef...` | md5=`sjv2YlWmiavgce2aGHw6/g==` crc32c=`UNqpyw==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_QSO_GCcomb_mean.txt` | 0.0 | **AUDITED** | `9bffdd0bf27615ab...` | md5=`Gb7AAPu3usIW80hI6VvEWA==` crc32c=`FhdrEw==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG_GCcomb_z0.6-0.8_cov.txt` | 0.0 | **AUDITED** | `cf17b81f8e62c9a9...` | md5=`0ROYzlQXReo+4ShOhJ+dvQ==` crc32c=`bxLv9Q==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_Lya_GCcomb_mean.txt` | 0.0 | **AUDITED** | `b6894a6662ebe83a...` | md5=`wudRYNU9jwHdSIEvkxpRVA==` crc32c=`POp4YA==` |
| `stream3_desi_dr1/sdss_DR16_LYAUTO_BAO_DMDHgrid.txt` | 0.18 | **AUDITED** | `40cee3a1c9dc5861...` | md5=`up/5EGnTcx0xKXPRkYOHdA==` crc32c=`r9MW8g==` |
| `stream3_desi_dr1/test_bao_mixed_observables_mean.txt` | 0.0 | **AUDITED** | `2e0bf112234fd8a2...` | md5=`cJmR9hGmDIf0vLJmb7hykQ==` crc32c=`Vk0B9A==` |
| `stream3_desi_dr1/sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8_covtot.txt` | 0.0 | **AUDITED** | `88f844447fb54679...` | md5=`XnU6ejWHf1jnAIV05e9cRg==` crc32c=`IiLg7Q==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_Lya_GCcomb_cov.txt` | 0.0 | **AUDITED** | `f93a5d57e0039f1f...` | md5=`y7I6vyLGIMGPwuIGbAfSNA==` crc32c=`2LvmoA==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_QSO_GCcomb_cov.txt` | 0.0 | **AUDITED** | `7445c6bca01e2732...` | md5=`3IKhi9bSTLK1WW9EluEvnA==` crc32c=`Z+2mKg==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_LRG_GCcomb_z0.4-0.6_cov.txt` | 0.0 | **AUDITED** | `c2f304ae57904488...` | md5=`l7x54D4AcceA4K2cX+cBJA==` crc32c=`4gUAZg==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_BGS_BRIGHT-21.35_GCcomb_mean.txt` | 0.0 | **AUDITED** | `06fc72ca4f4b4a03...` | md5=`s5fxiVMug+q3/zUa/zPgqQ==` crc32c=`tP7jiQ==` |
| `stream3_desi_dr1/sdss_DR16_QSO_BAO_DMDH_covtot.txt` | 0.0 | **AUDITED** | `c0d8bab471320451...` | md5=`NqozRkYKuOYUJ4KCUM0U5Q==` crc32c=`LprRBA==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG_GCcomb_z0.6-0.8_cov.txt` | 0.0 | **AUDITED** | `16fa8c323f54139e...` | md5=`YkrBh54CcLdRKgNdb6mgZw==` crc32c=`cma9zA==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_ELG_LOPnotqso_GCcomb_z1.1-1.6_cov.txt` | 0.0 | **AUDITED** | `8d1afedca817a80f...` | md5=`S+e1nLtSYlryP9Ad13wwdA==` crc32c=`T1/QGg==` |
| `stream3_desi_dr1/sdss_DR12Consensus_final.dat` | 0.0 | **AUDITED** | `eae45d2629dc1214...` | md5=`6dSIDAgKUGPS5D+M2JBy7Q==` crc32c=`pw6urg==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_ELG_LOPnotqso_GCcomb_z1.1-1.6_cov.txt` | 0.0 | **AUDITED** | `6ade793349c090ab...` | md5=`XhXXLkCpYqup1tTYdSntnQ==` crc32c=`m5PPvQ==` |
| `stream3_desi_dr1/sdss_MGS_prob.txt` | 0.01 | **AUDITED** | `c252e18fefc69b76...` | md5=`gO1/MtIyqACagD8KFUPHGw==` crc32c=`iuYnhg==` |
| `stream3_desi_dr1/sdss_DR12Consensus_FS.dat` | 0.0 | **AUDITED** | `16c28eb4cee0c0a8...` | md5=`4TqPhCEDib/7NutRrq5JZQ==` crc32c=`k6BOeQ==` |
| `stream3_desi_dr1/sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8.dat` | 0.0 | **AUDITED** | `a098ea4df320ac1c...` | md5=`H+IGvApF2mW8ZCCiPe+Gwg==` crc32c=`TdCiJw==` |
| `stream3_desi_dr1/final_consensus_covtot_dM_Hz_fsig.txt` | 0.0 | **AUDITED** | `dea6d8d4893d2b84...` | md5=`YHmhaZJa/E+wQkQnps3Hxw==` crc32c=`jzh8hg==` |
| `stream3_desi_dr1/desi_2024_eboss_gaussian_bao_Lya_GCcomb_mean.txt` | 0.0 | **AUDITED** | `e6b09123521f91c2...` | md5=`CaLIAjHi1dEO5XuTCKzNRw==` crc32c=`QyHGTw==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_QSO_GCcomb_z0.8-2.1_mean.txt` | 0.0 | **AUDITED** | `12bf41993f73c7ce...` | md5=`jn211RoDXH99faxWvDIsiw==` crc32c=`K5iT4g==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_Lya_GCcomb_mean.txt` | 0.0 | **AUDITED** | `9b4ab92080d038d0...` | md5=`dK7IjDA7og/1s9y1CYkNVw==` crc32c=`+MDtBw==` |
| `stream3_desi_dr1/sdss_DR16_LRG_BAO_DMDH_covtot.txt` | 0.0 | **AUDITED** | `1a45e106f8e2bbf8...` | md5=`3kjKU00KZa16ewNkTAHrHA==` crc32c=`LO3XXA==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_ALL_GCcomb_mean.txt` | 0.0 | **AUDITED** | `dd2873a0b88459a4...` | md5=`bSrNsF64WiEW7nBUaAgYww==` crc32c=`SfHJgA==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_Lya_GCcomb_cov.txt` | 0.0 | **AUDITED** | `02a049dbf3a1cd39...` | md5=`2vNs9vCylbC1omm35IHsfQ==` crc32c=`kB/rvQ==` |
| `stream3_desi_dr1/FS_consensus_covtot_dM_Hz_fsig.txt` | 0.0 | **AUDITED** | `a7e5d4a757b39591...` | md5=`BkHZsYrhq/5m18H607RI3A==` crc32c=`aH/Z/w==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_ELG_LOPnotqso_GCcomb_z1.1-1.6_mean.txt` | 0.0 | **AUDITED** | `75d2dd246d2f1714...` | md5=`oV6yjsAQiC6U6FvuovFN/Q==` crc32c=`f4ZYcg==` |
| `stream3_desi_dr1/sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8_covtot.txt` | 0.0 | **AUDITED** | `409cabbf4ccf6993...` | md5=`7VKAYLdrYhFH9OE8hchw0Q==` crc32c=`9Ahlvw==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_BGS_BRIGHT-21.5_GCcomb_z0.1-0.4_mean.txt` | 0.0 | **AUDITED** | `b47109f842b2b79c...` | md5=`Y79jAc3pkNo3vyT6drkSFw==` crc32c=`qSdccA==` |
| `stream3_desi_dr1/sdss_DR16_QSO_BAO_DMDH.txt` | 0.0 | **AUDITED** | `9d3a43515d009d5c...` | md5=`WFFfbHYmoJiEp1w1Qr6l2A==` crc32c=`IdppXg==` |
| `stream3_desi_dr1/test_bao_mixed_observables_cov.txt` | 0.0 | **AUDITED** | `c280474d8d2b8e2a...` | md5=`9gE0JY7vmnH70voC3JfVww==` crc32c=`fduWHQ==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG_GCcomb_z0.4-0.6_mean.txt` | 0.0 | **AUDITED** | `86336445497058ee...` | md5=`SK4xQN986lZYuqHxkhTNLA==` crc32c=`SRBtHA==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_QSO_GCcomb_z0.8-2.1_cov.txt` | 0.0 | **AUDITED** | `ccd4322915db7666...` | md5=`NjqkAf4y70gzE34oEv5dvQ==` crc32c=`YqNE3g==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_LRG+ELG_LOPnotqso_GCcomb_mean.txt` | 0.0 | **AUDITED** | `c34585b9afdb683e...` | md5=`OYaiXyAZYPJuBe05Zo0kug==` crc32c=`bSxjXw==` |
| `stream3_desi_dr1/desi_bao_dr2/desi_gaussian_bao_BGS_BRIGHT-21.35_GCcomb_cov.txt` | 0.0 | **AUDITED** | `06d7260009fa0030...` | md5=`IUHnopOG2Iy8HEzCoF6nYQ==` crc32c=`zSm/AA==` |
| `stream3_desi_dr1/desi_2024_gaussian_bao_BGS_BRIGHT-21.5_GCcomb_z0.1-0.4_cov.txt` | 0.0 | **AUDITED** | `71235724a2d79f85...` | md5=`PelvL7yXWzKedhHNZvH2ng==` crc32c=`utT3dQ==` |

### stream3_euclid_q2/

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `stream3_euclid_q2/kids1000_K1K_BandPowers.data` | 0.01 | **AUDITED** | `e412b9ce71af4e21...` | md5=`uXy6eJazpgHt21uzZaULrQ==` crc32c=`mcx3+Q==` |
| `stream3_euclid_q2/kids1000_bandpowers_EE.npy` | 0.0 | **AUDITED** | `693f14ce40eda137...` | md5=`ZCXeqIpH1HKa+Kf8CuHrQw==` crc32c=`R4VDNQ==` |
| `stream3_euclid_q2/BandPowers_Benchmark.param` | 0.0 | **AUDITED** | `b7b1bf5fccbc456b...` | md5=`RRIoashJ6Pv1TMwMe/L+BA==` crc32c=`CM1fOQ==` |
| `stream3_euclid_q2/kids1000_bandpowers_EE.json` | 0.0 | **AUDITED** | `e0c940ba5741aa65...` | md5=`bUxvDBuKfoHXywySLCm4wA==` crc32c=`gRDUyA==` |
| `stream3_euclid_q2/s8_joint_covariance.txt` | 0.0 | **AUDITED** | `2500573e53476aa9...` | md5=`95HYs3CfH7z+cs1kPpLyFQ==` crc32c=`L9wf1w==` |
| `stream3_euclid_q2/euclid_q2_proxy_bridge.dataset` | 0.0 | **AUDITED** | `816b14835737ba35...` | md5=`nO91+Z45OjabWcsV2SMpxA==` crc32c=`h3o9Ww==` |
| `stream3_euclid_q2/kids1000_K1K_BandPowers.data.benchmark` | 0.01 | **AUDITED** | `3f9624711d3bf172...` | md5=`mQuO/7gPXSh8xoNAv8jfxw==` crc32c=`0/3FjA==` |
| `stream3_euclid_q2/BandPowers_Benchmark_HMcode.param` | 0.0 | **AUDITED** | `3e02bc09a56be5a0...` | md5=`cgrR1qVpvJy74wgquEpDPQ==` crc32c=`XST94A==` |
| `stream3_euclid_q2/s8_wl_measurements.json` | 0.0 | **AUDITED** | `95a25b4f06d9c9fa...` | md5=`ualMFJAkWqy1jsO7sKodYg==` crc32c=`/Otahw==` |
| `stream3_euclid_q2/mpirun_with_multinest.sh` | 0.0 | **AUDITED** | `25b480571fc5c693...` | md5=`cgKFEHrWMLly+vEEjnSTSQ==` crc32c=`N9zjyw==` |
| `stream3_euclid_q2/kids1000_README.md` | 0.0 | **AUDITED** | `3ebf9cd310bd1085...` | md5=`Qrq9SxiMDZCuVH14Z9gCrg==` crc32c=`RfHUnQ==` |
| `stream3_euclid_q2/mpirun_with_polychord.sh` | 0.0 | **AUDITED** | `aa527c9c726fbd97...` | md5=`w20ljKRrrr2jzb/Co82erw==` crc32c=`puIOsA==` |
| `stream3_euclid_q2/euclid_q2_proxy_bridge.dat` | 0.0 | **AUDITED** | `8d5628d709da106e...` | md5=`P2QOkbeqq6z8BMQmmdSWUA==` crc32c=`hPjswg==` |
| `stream3_euclid_q2/kids1000_K1K_BandPowers.data.benchmark_hmcode` | 0.01 | **AUDITED** | `cc50bc8374e082ef...` | md5=`b/9C6WIPH60hmNT2LtRd9Q==` crc32c=`2qgtWA==` |
| `stream3_euclid_q2/s8_joint_means.txt` | 0.0 | **AUDITED** | `900c0bcb74979d66...` | md5=`M7GNj/QdSYae0dXX3y819w==` crc32c=`n4nSmw==` |
| `stream3_euclid_q2/euclid_q2_proxy_bridge.covmat` | 0.0 | **AUDITED** | `b027e2d912b63a95...` | md5=`Edyj1LCfljg9XYKGpk/bxw==` crc32c=`MsZcjg==` |
| `stream3_euclid_q2/theory_bandpowers.param` | 0.0 | **AUDITED** | `fd224e4d21c74269...` | md5=`amsdDP/ll5Zw9PN5aTK1iA==` crc32c=`z0+XIA==` |
| `stream3_euclid_q2/kids1000___init__.py` | 0.03 | **AUDITED** | `f4d86d4e356648a6...` | md5=`dvi95vFJdOaFPaXaWhBLBQ==` crc32c=`ZqBAMQ==` |
| `stream3_euclid_q2/README.md` | 0.0 | **AUDITED** | `81a2d25467e96bd3...` | md5=`OzHD6iI/UG+dwRdKoC9TRQ==` crc32c=`ZK7amA==` |

### stream4_bridge/

**🔬 EXPLORATORY SANDBOX** — no claim from Stream 4 may be cited as evidence in Streams 1–3 (T0 decision DL-3).

| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |
|-----|-----------|--------|---------|--------------------------|
| `stream4_bridge/spectral_bridge_verification.json` | 0.0 | **AUDITED** | `721ecd9c3a841aa8...` | md5=`8C1T3lzAkBn9nDd7QWMSoQ==` crc32c=`l9/5UA==` |
| `stream4_bridge/deterministic_k3_candidate_cooper_s10.json` | 0.0 | **AUDITED** | `82c1c5ac0bb63383...` | md5=`zKghlrBY6bDN7uUNBwXvzQ==` crc32c=`RXNiiA==` |
| `stream4_bridge/convergence_report.json` | 0.0 | **AUDITED** | `b2a73d1794a01132...` | md5=`yGnSGoQc5I4P3YoYD3GwWA==` crc32c=`G3bshw==` |
