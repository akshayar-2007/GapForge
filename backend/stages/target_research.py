import json
from typing import Optional

# Curated benchmarks: what each company tests in interviews
COMPANY_BENCHMARKS = {
    "Goldman Sachs": {
        "depth_areas": [
            {"area": "System Design", "weight": 0.25, "keywords": ["distributed systems", "scalability", "databases", "microservices"]},
            {"area": "Trading Systems", "weight": 0.20, "keywords": ["low-latency", "real-time", "event-driven", "stream processing"]},
            {"area": "Data Engineering", "weight": 0.20, "keywords": ["ETL", "data pipelines", "Kafka", "spark", "hadoop"]},
            {"area": "Backend APIs", "weight": 0.15, "keywords": ["REST", "gRPC", "GraphQL", "microservices"]},
            {"area": "Algorithm Optimization", "weight": 0.10, "keywords": ["performance", "optimization", "complexity", "caching"]},
            {"area": "Testing & Reliability", "weight": 0.10, "keywords": ["unit tests", "integration tests", "monitoring", "logging"]},
        ]
    },
    "Meta": {
        "depth_areas": [
            {"area": "System Design", "weight": 0.25, "keywords": ["distributed systems", "scale", "consistency"]},
            {"area": "Large-Scale Data Processing", "weight": 0.20, "keywords": ["data pipelines", "big data", "streaming"]},
            {"area": "ML Infrastructure", "weight": 0.15, "keywords": ["ML models", "TensorFlow", "PyTorch", "inference"]},
            {"area": "Backend APIs", "weight": 0.15, "keywords": ["API design", "microservices"]},
            {"area": "Performance Optimization", "weight": 0.15, "keywords": ["optimization", "profiling", "caching"]},
            {"area": "Testing", "weight": 0.10, "keywords": ["testing", "QA", "reliability"]},
        ]
    },
    "Jane Street": {
        "depth_areas": [
            {"area": "Algorithmic Trading", "weight": 0.30, "keywords": ["trading", "markets", "algorithms"]},
            {"area": "Low-Latency Systems", "weight": 0.25, "keywords": ["low-latency", "performance", "C++", "optimization"]},
            {"area": "Systems Programming", "weight": 0.20, "keywords": ["C++", "systems", "memory management"]},
            {"area": "Data Engineering", "weight": 0.15, "keywords": ["data pipelines", "analytics"]},
            {"area": "Performance Tuning", "weight": 0.10, "keywords": ["profiling", "optimization"]},
        ]
    },
    "default": {
        "depth_areas": [
            {"area": "System Design", "weight": 0.20, "keywords": ["scalability", "distributed systems"]},
            {"area": "Backend Development", "weight": 0.20, "keywords": ["APIs", "databases", "backend"]},
            {"area": "Data Structures & Algorithms", "weight": 0.15, "keywords": ["algorithms", "data structures", "optimization"]},
            {"area": "Frontend / Full-Stack", "weight": 0.15, "keywords": ["React", "frontend", "UI"]},
            {"area": "Database Design", "weight": 0.15, "keywords": ["database", "SQL", "NoSQL"]},
            {"area": "Testing & DevOps", "weight": 0.15, "keywords": ["testing", "DevOps", "CI/CD"]},
        ]
    }
}

def get_company_benchmark(company_name: Optional[str] = None) -> dict:
    """Fetch depth-area benchmark for target company."""
    if not company_name or company_name not in COMPANY_BENCHMARKS:
        return COMPANY_BENCHMARKS["default"]
    return COMPANY_BENCHMARKS[company_name]