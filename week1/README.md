# Week 1

#### Goals:
- Find vedctor DB to store `userID, text` data table
    - Consider a few options
    - Look for the best vector DB, consdier weaviate vector DB
    - specs: 
        - needs to support up to 80M embeddings
        - needs to have semi fast lookup
        - needs to not be stupidly expensive
    - create python script to call the DB from
- Find embedding model
    - consider a few options
    - look at HF for best embedding model for recommendation systems/search
    - use langchain for setup
    - specs:
        - must support >60 tokens (~40 words)
        - 1500+ dimensions
        - ideal for search

----
# Research Findings:

### Vector Database Solutions

#### Managed SaaS Options

| Database | Strengths | Limitations | Cost (80M vectors) |
|----------|-----------|-------------|-------------------|
| **Pinecone** | • Fully managed<br>• Minimal operational overhead<br>• Strong horizontal scaling | • Stores only vectors (needs separate doc storage)<br>• Potential vendor lock-in | Not specifically detailed |
| **Databricks Vector Search** | • Clear pricing model<br>• Integrated with Databricks ecosystem | • Higher cost option | ~$8,000-10,000/month |

#### Open Source Options

| Database | Strengths | Limitations | Cost |
|----------|-----------|-------------|------|
| **Milvus** | • Mature open-source solution<br>• Comprehensive features<br>• Scales to billions of vectors | • Steeper learning curve<br>• More complex operations | Infrastructure & operational only |
| **Weaviate** | • GraphQL-based API<br>• Schema-based approach<br>• Hybrid search capabilities | Not specified | Infrastructure & operational only |
| **Qdrant** | • High-performance<br>• Real-time updates<br>• Filter-before-search<br>• Rust-based for efficiency | Not specified | Infrastructure & operational only |
| **Faiss** | • Exceptional performance<br>• Memory efficiency | • Not a complete database solution<br>• Lacks built-in persistence | Infrastructure & operational only |

#### Hybrid Solutions

| Database | Strengths | Limitations | Cost |
|----------|-----------|-------------|------|
| **MongoDB Atlas Vector Search** | • Integrated with document DB<br>• Single source of truth<br>• Supports nested documents | • Unclear if available on-premises | Not specified |

### Embedding Models

#### OpenAI Models

| Model | Dimensions | Token Limit | Performance (MIRACL score) | Cost |
|-------|------------|-------------|----------------------------|------|
| **text-embedding-ada-002** | 1536 | 8191 | 31.4 | $0.10 per million tokens |
| **text-embedding-3-large** | 3072 | 8191 | 54.9 | $0.13 per million tokens |
| **text-embedding-3-small** | 1536 | 8191 | 44.0 | $0.02 per million tokens |

#### Hugging Face Models
- Various embedding models available
- Selection guidance:
  - Consult MTEB leaderboard for high performers
  - Consider domain-specific models
  - Evaluate based on specific retrieval tasks

### Cost Considerations for 80M Embeddings

#### Vector Database Monthly Costs
- **Managed solutions**: ~$8,000-10,000/month (based on Databricks pricing)
- **Open-source**: Infrastructure and operational costs vary

#### One-time Embedding Generation Costs 
(assuming 50 tokens/record × 80M records = 4B tokens)

| Model | Cost for 4B tokens |
|-------|-------------------|
| **text-embedding-3-large** | $520,000 |
| **text-embedding-ada-002** | $400,000 |
| **text-embedding-3-small** | $80,000 |

### Implementation Recommendations

#### Vector Database Selection
- **For operational simplicity**: Pinecone
- **For control/vendor independence**: Milvus
- **For MongoDB users**: MongoDB Atlas Vector Search

#### Embedding Model Selection
- **Best value**: text-embedding-3-small (excellent performance at lower cost)
- **Highest performance**: text-embedding-3-large (superior performance at premium cost)

----

## Original Discussion:

![Week 1 Trudy Image](./trudy_week1.png)

