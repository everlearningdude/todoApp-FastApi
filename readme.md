```mermaid
flowchart TD
    A[User Initiates Transaction] --> B[Funds are Tokenized]
    B --> C[Smart Contract Validates Transaction]
    C --> D{Sufficient Balance?}
    D -- Yes --> E[Multi-Signature Authorization]
    E --> F[Transaction Recorded on Blockchain]
    F --> G[Funds Transferred to Recipient's Wallet]
    G --> H[Recipient Converts Tokens to Local Currency]
    H --> I[Transaction Complete]

    D -- No --> J[Transaction Rejected]
    J --> K[User Notified of Rejection]

    style J fill:#f96,stroke:#333,stroke-width:2px
    style K fill:#f96,stroke:#333,stroke-width:2px