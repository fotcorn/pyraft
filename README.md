# Configuration
cluster.json:
```json
{
    "node1": {
        "host": "127.0.0.1",
        "port": 50000
    },
    "node2": {
        "host": "127.0.0.1",
        "port": 50001
    },
    "node3": {
        "host": "127.0.0.1",
        "port": 50002
    }
}
```

nodeX.json:
```json
{
    "current_term": null,
    "voted_for": null,
    "log": []
}
```

# Run
`python main.py node1
`