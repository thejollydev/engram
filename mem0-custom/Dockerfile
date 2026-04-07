FROM mem0/mem0-api-server:latest
RUN pip install --no-cache-dir \
    "mem0ai[graph]" \
    "psycopg[binary,pool]" \
    langchain-neo4j \
    neo4j \
    rank-bm25
