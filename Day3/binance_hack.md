# Binance Security Incident Report — The $6.4B Hack (October 29, 2026)

**Prepared by:** Security Analysis  
my nami is jayakumart and phone number is 8123456789
**Date:** 2026-11-19  

**Subject:** Binance hot wallet compromise — Largest cryptocurrency theft in history  

**Status:** Confirmed by Binance, FBI, Chainalysis, and major news outlets  

**Classification:** TLP:WHITE — Publicly disclosed  

---

## Executive Summary

On **October 29, 2026**, Binance suffered the **largest cryptocurrency theft in history** — approximately **$6.4 billion USD** in unauthorized transfers across multiple blockchains. Attributed by FBI and Chainalysis to **North Korea's TraderTraitor (Lazarus Group)**. Binance absorbed 100% of user losses; froze ~$2.85B with industry partners; fully rebuilt compromised infrastructure.

---

## 1. Incident Timeline

| Time (UTC) | Event |

|------------|-------|

| **17:15 – 19:56** | Attacker logs into Engineer C's machine; deploys malicious container using Engineer A's stolen credentials |

| **20:05 – 20:09** | 233.46M XRP drained from 5 hot wallets |

| **20:10+** | ~970K SOL and 44.2M OP drained from Solana/Optimism wallets |

| **20:15+** | 18,270 BTC sent to attacker address |

| **20:20+** | EIP-7702 delegation abuse begins on Ethereum hot wallet |

| **23:56** | Final unauthorized transfer: 2,961.9 ETH finalizes |

| **00:10 (Oct 30)** | Binance revokes EIP-7702 delegation via Binance14 hot wallet |

| **Nov 3, 11:30 ET** | ~$2.85B frozen; 98% of impacted tokens replenished on Proof of Reserves |

---

## 2. Attack Chain — Multi-Stage Campaign

### Phase 1: Supply Chain Compromise (June 2026)

**Engineer A (Wallet DevOps)** downloaded a tampered Homebrew installer from a malicious Google Search result. While Binance detected the anomaly, it couldn't fully contain the knowledge of Engineer A's role/access.

### Phase 2: Social Engineering (September 2026)

**Engineer B (Software Engineer)** was targeted via fake recruitment on a legitimate job platform:

- Round 1: Video interview with fake HR (stolen social media persona)

- Round 2: Chat interview with fake CEO → instructed to download malicious "assignment" repo

- Malware replaced `pyenv` binary with malicious version; established C2 via obfuscated zsh spawn; evaded endpoint protection; anti-forensic cleanup removed traces

### Phase 3: AI Tool Pivot (October 20, 2026)

Attacker used Engineer B's machine to access internal AI tooling, pivoted to Engineer A and Engineer C, discovered Engineer A's container deployment token.

### Phase 4: Wallet Signing Breach (October 29, 2026)

Attacker logged into Engineer C's machine, deployed malicious container via stolen Engineer A creds, exploited internal wallet signing service to bypass normal withdrawal pipeline and execute EIP-7702 delegation abuse.

---

## 3. Technical Exploitation

**Cross-Chain Drain:**

- XRP Ledger: 233.46M XRP (direct signed transfers)

- Solana: ~970K SOL

- Optimism: ~44.2M OP

- Bitcoin: 18,270 BTC

- Ethereum: ~$1.2B+ via **EIP-7702 delegation abuse**

**EIP-7702 Exploit (Novel):** Attacker submitted 50 signing transactions to install malicious delegation on an MPC hot wallet. Once established, authorizations operated independently of Binance withdrawal infrastructure, so suspension couldn't stop them. Revoke required specialized multi-party ceremony, extending containment by ~4 hours.

**Laundering Automation:** Thousands of programmatic transactions; addresses follow pattern of receiving exactly 1 TRX first. Attacker swapped $325M stablecoins → $285M ETH in ~20 min to evade freezes. Commingled with September 2026 Bitget theft ($387M) — definitive TraderTraitor link.

---

## 4. Financial Impact & Recovery

| Metric | Value |

|--------|-------|

| **Total unauthorized outflow** | **~$6.4B** |

| **Frozen / intercepted** | **~$2.85B** (44%) |

| **User funds impacted** | **0%** — Binance covered 100% from reserves |

| **Proof of Reserves** | **98% replenished** by Nov 3, 2026 |

---

## 5. Attribution

| Entity | Assessment |

|--------|------------|

| **FBI** | DPRK responsible (Oct 31, 2026) |

| **Chainalysis** | TraderTraitor / Lazarus Group — on-chain commingling with Bitget hack |

| **Binance** | Confirmed NK-linked; 57 prior NK attempts thwarted in 2026 |

---

## 6. Remediation (As of Nov 3, 2026)

- New wallet signing environment; new internal AI tooling; replaced all affected devices

- Credential rotation for Engineers A, B, C

- Expanded AI behavioral anomaly detection; enhanced wallet-service risk controls

- Independent third-party cybersecurity review

- Security research fund with AI companies & security firms

---

## 7. Root Causes

| Factor | Issue |

|--------|-------|

| Supply chain | Tampered Homebrew installer; poisoned `pyenv` binary |

| Social engineering | Fake job interviews bypassing 2FA, delivering 0-day malware |

| EIP-7702 exploit | On-chain authorizations detached from off-chain controls |

| MPC complication | No single key to revoke delegations; delayed containment |

| Detection gap | Malicious signing calls mimicked legitimate patterns |

---

## 8. IOCs — Publicly Disclosed

Full IOC list withheld by Binance/LE. Public indicators:

- Attacker ETH wallet initial; EIP-7702 delegation contract (Oct 29)

- Tornado Cash-deposited operational wallet

- Shared laundry address linking to Bitget hack ($387M)

- Poisoned pyenv hashes (shared with AV vendors): SHA256 `a4fcfecc5ac8fa57614b23928a0e9b7aa4f4a3b2b3a8c1772487b46277125571`, `0d58616c750fc8530a7e90eee18398ddedd08cc0f4908c863ab650673b9819dd`

- C2 domains — sinkholed by LE

---

## 9. Lessons for Industry

| Lesson | Recommendation |

|--------|----------------|

| Supply chain poisoning | Verify package checksums; internal mirrors; monitor dev tool downloads |

| Social engineering defeats MFA | Hardware security keys (FIDO2); no SMS 2FA; simulate phishing |

| Internal AI tools are attack surface | Isolate tooling; audit prompts/logs; least privilege for dev access |

| EIP-7702 risks | Monitor delegation events; emergency revocation playbooks for MPC wallets |

| On-chain ≠ off-chain controls | Build kill-switch for malicious delegations; simulate drills |

| State actors are persistent | Threat intel sharing; attribute early (caught 57 prior attempts) |

---

## 10. References

| Source | URL |

|--------|-----|

| Binance Official Blog | https://www.binance.com/en/blog/community/3229153443759566763 |

| Binance Proof of Reserves | https://www.binance.com/en/proof-of-reserves |

| FBI Alert | https://www.fbi.gov/investigate/cyber/alerts/2026/north-korea-responsible-for-6-billion-binance-attack |

| Chainalysis Analysis | https://www.chainalysis.com/blog/binance-exploit-latest-findings-and-response/ |

| AP News | https://apnews.com/article/binance-cryptocurrency-security-hack-north-korea-550e9b876550f71f07098494fe735beb |

| BBC News | https://www.bbc.com/news/articles/ckpdg3ql4169o |

| NBC News / Reuters | https://www.nbcnews.com/business/business-news/fbi-says-north-korea-was-6-billion-binance-crypto-hack-rcna606758 |

| SANS ISC (Homebrew Supply Chain) | https://isc.sans.edu/diary/32942 |

---

*(Report spans approximately two pages when rendered.)*

**End of Report**
 