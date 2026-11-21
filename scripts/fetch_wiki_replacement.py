
import json
import time
from pathlib import Path

import requests
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "constants"
    / "wiki_llm_training_resume_project.jsonl"
)

TOPICS = [
    # Languages and runtimes
    "Python (programming language)", "C++", "Java (programming language)",
    "JavaScript", "TypeScript", "Go (programming language)", "Rust (programming language)",
    "SQL", "Bash (Unix shell)", "Node.js", "Java Virtual Machine", "Kotlin",
    "Swift (programming language)", "C#", "Ruby (programming language)",
    "Scala (programming language)", "Solidity", "Dart (programming language)",

    # Classical ML
    "Random forest", "Gradient boosting", "XGBoost", "Decision tree learning",
    "Support vector machine", "K-nearest neighbors algorithm", "Naive Bayes classifier",
    "Linear regression", "Logistic regression", "Principal component analysis",
    "K-means clustering", "DBSCAN", "Ensemble learning", "Dimensionality reduction",
    "Time series analysis", "Bayesian statistics", "Causal inference",

    # Deep learning and AI
    "Neural network", "Convolutional neural network", "Recurrent neural network",
    "Transformer (machine learning)", "Attention (machine learning)", "Backpropagation",
    "Large language model", "Generative pre-trained transformer", "BERT (language model)",
    "Fine-tuning (machine learning)", "Transfer learning", "Embedding",
    "Generative adversarial network", "Diffusion model", "Reinforcement learning",
    "Computer vision", "Natural language processing", "Explainable AI",

    # Data structures
    "Array (data structure)", "Linked list", "Hash table", "Binary search tree",
    "Red–black tree", "AVL tree", "B-tree", "Heap (data structure)", "Trie",
    "Graph (abstract data type)", "Stack (abstract data type)",
    "Queue (abstract data type)", "Bloom filter", "Disjoint-set data structure",

    # Algorithms
    "Sorting algorithm", "Quicksort", "Merge sort", "Binary search algorithm",
    "Dynamic programming", "Dijkstra's algorithm", "A* search algorithm",
    "Depth-first search", "Breadth-first search", "Greedy algorithm",
    "Pathfinding", "Simultaneous localization and mapping",

    # System design
    "Microservices", "Monolithic application", "Load balancing (computing)",
    "Database sharding", "Caching (computing)", "Content delivery network",
    "CAP theorem", "ACID", "Consistent hashing", "Replication (computing)",
    "Leader election", "Distributed system", "Event-driven architecture",
    "REST", "GraphQL", "gRPC", "WebSocket", "Serverless computing",
    "Service mesh", "API gateway", "OAuth", "JWT",

    # MLOps and deployment
    "CI/CD", "DevOps", "MLOps", "Containerization (computing)", "Kubernetes",
    "Docker (software)", "Infrastructure as code", "Terraform (software)",
    "Model serving", "Feature store", "Data lineage", "A/B testing",
    "Model monitoring", "Experiment tracking", "Data version control",

    # Tools and frameworks
    "Librosa", "Streamlit", "Flask (web framework)", "Django (web framework)",
    "FastAPI", "Spring Boot", "React (software)", "Angular (web framework)",
    "Apache Kafka", "RabbitMQ", "Redis", "PostgreSQL", "MongoDB",
    "Elasticsearch", "Apache Spark", "Hadoop", "Pandas (software)",
    "NumPy", "Scikit-learn",

    # Generative AI and LLM stack
    "Retrieval-augmented generation", "LangChain", "LlamaIndex",
    "Vector database", "Pinecone (database)", "Weaviate", "Prompt engineering",
    "Parameter-efficient fine-tuning", "Low-rank adaptation",
    "Hugging Face Transformers", "Stable Diffusion", "Synthetic data",
    "Hallucination (artificial intelligence)", "Model alignment",

    # Data engineering and analytics
    "Data warehouse", "Data lake", "Data mesh", "Snowflake (software)",
    "Google BigQuery", "Amazon Redshift", "Databricks", "Apache Airflow",
    "dbt (software)", "ETL", "ELT", "Apache Flink", "Star schema",
    "Slowly changing dimension", "Data governance",

    # Cloud and observability
    "Amazon Web Services", "Microsoft Azure", "Google Cloud Platform",
    "Helm (software)", "Argo CD", "Prometheus (software)", "Grafana",
    "OpenTelemetry", "Istio", "Chaos engineering",
    "Site reliability engineering", "Infrastructure as Service",
    "Platform as a Service", "GitOps",

    # Frontend and mobile
    "Vue.js", "Next.js", "Tailwind CSS", "Redux (JavaScript library)",
    "Webpack", "React Native", "Flutter (software)", "SwiftUI",
    "Jetpack Compose", "Android Studio", "Xcode",
    "Progressive web app", "Single-page application", "WebAssembly",

    # Game development and graphics
    "Unity (game engine)", "Unreal Engine", "OpenGL", "Vulkan (API)",
    "DirectX", "Shader", "Ray tracing (graphics)", "3D computer graphics",
    "Physics engine", "Augmented reality", "Virtual reality", "WebGL",

    # Security and blockchain
    "Cybersecurity", "Penetration test", "Identity management",
    "Zero trust security model", "OWASP", "Smart contract", "Ethereum",
    "Decentralized application", "Web3", "Cryptography",
    "Public-key cryptography", "Consensus algorithm",

    # Embedded and hardware
    "Embedded system", "Real-time operating system", "Microcontroller",
    "Firmware", "Internet of things", "Field-programmable gate array",
    "System on a chip", "Communication protocol", "I2C", "SPI", "UART"
]


def fetch_wiki_content(title):
    url = "https://en.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "CareerKnowledgeGraphBot/1.0 (educational_project@example.com)"
    }
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1
    }

    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=10
        )
        if response.status_code != 200:
            print(f"HTTP Error {response.status_code} for {title}")
            return None

        pages = response.json().get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id == "-1":
                print(f"Page not found: {title}")
                return None
            if "extract" in page_data:
                return page_data["extract"]

    except Exception as exc:
        print(f"Error fetching {title}: {exc}")

    return None


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"Topics: {len(TOPICS)}")
    print(f"Output: {OUTPUT_FILE}")

    success_count = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for topic in tqdm(TOPICS, desc="Fetching Wikipedia articles"):
            content = fetch_wiki_content(topic)

            if content:
                entry = {
                    "title": topic,
                    "text": content,
                    "source": "wikipedia_core_concepts",
                    "keyword": "Computer Science Fundamentals"
                }
                file.write(json.dumps(entry, ensure_ascii=False) + "\n")
                success_count += 1
                time.sleep(0.5)

    print(f"\nSUCCESSFULLY FETCHED: {success_count} / {len(TOPICS)} Articles")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
