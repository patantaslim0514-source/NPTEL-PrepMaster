"""
sample_data.py - Preloaded high-yield NPTEL course modules for instant 1-click demo 
and offline fallback.
"""

SAMPLE_COURSES = {
    "cloud_computing": {
        "id": "cloud_computing",
        "title": "NPTEL: Cloud Computing & Virtualization",
        "instructor": "Prof. Soumya Kanti Ghosh (IIT Kharagpur)",
        "week": "Week 3: Virtualization, Hypervisors & Service Level Agreements (SLA)",
        "total_pages": 12,
        "total_words": 3450,
        "estimated_read_time_mins": 17,
        "overview": "Comprehensive NPTEL lecture module covering Type-1 and Type-2 Hypervisors, Full vs Paravirtualization, SLA metrics, Cloud elasticity vs scalability, and NIST cloud characteristics.",
        "key_points": [
            {
                "category": "Core Concept",
                "title": "NIST Essential Characteristics of Cloud",
                "content": "On-demand self-service, Broad network access, Resource pooling (multi-tenancy), Rapid elasticity (scale in/out dynamically), and Measured service (pay-per-use billing)."
            },
            {
                "category": "Virtualization",
                "title": "Type-1 (Bare-Metal) vs Type-2 (Hosted) Hypervisors",
                "content": "Type-1 runs directly on hardware (e.g., VMware ESXi, Xen, KVM) offering superior performance and low overhead. Type-2 runs on a host operating system (e.g., Oracle VirtualBox, VMware Workstation), easier to test but adds OS overhead."
            },
            {
                "category": "Architecture",
                "title": "Full Virtualization vs Paravirtualization",
                "content": "Full virtualization requires no modification to the guest OS (uses binary translation or hardware assist like Intel VT-x/AMD-V). Paravirtualization modifies the guest OS kernel with hypercalls for enhanced I/O throughput."
            },
            {
                "category": "SLA & Reliability",
                "title": "Service Level Agreement (SLA) & High Availability Formula",
                "content": "Availability formula: $A = \\frac{\\text{MTTF}}{\\text{MTTF} + \\text{MTTR}} \\times 100\\%$. 'Five Nines' ($99.999\\%$) permits only ~5.26 minutes of downtime per year."
            },
            {
                "category": "Exam Pitfall",
                "title": "Scalability vs Elasticity (NPTEL Favorite)",
                "content": "Scalability is the structural ability to handle growing workload by adding resources (static/planned). Elasticity is the automatic, autonomous adaptation of capacity to match fluctuating demand in real-time."
            }
        ],
        "conceptual_explanations": [
            {
                "topic": "1. Hypervisor Architecture and Classification",
                "analogy": "Think of hardware as a piece of land. A Type-1 Hypervisor is like building an apartment complex directly on the foundation. A Type-2 Hypervisor is like building a tent inside an existing house—it depends on the room's floor and roof (Host OS).",
                "deep_dive": "Virtual Machine Monitors (VMM) abstract the physical compute, memory, and I/O. In Type-1 hypervisors, privileged Ring 0 instructions are intercepted directly by the hypervisor microkernel. In Type-2, the hypervisor operates in User Space (Ring 3) or Kernel space through the Host OS kernel, incurring context-switch latency between Guest OS -> Host OS -> Hardware.",
                "key_takeaway": "NPTEL frequently asks whether KVM is Type-1 or Type-2: KVM turns the Linux kernel itself into a Type-1 bare-metal hypervisor via loadable kernel modules (kvm.ko)."
            },
            {
                "topic": "2. Virtualization Techniques: Binary Translation vs Hypercalls",
                "analogy": "Binary Translation is like a live simultaneous interpreter translating sensitive phrases on the fly without changing the original speaker's script. Paravirtualization is like teaching the speaker a specific diplomatic dialect beforehand so no interpreter is needed.",
                "deep_dive": "x86 architecture historically had the 'virtualization hole' where 17 sensitive instructions (like POPF, PUSHF, CLI) were unprivileged and did not trap when executed in Ring 1. VMware solved this through Dynamic Binary Translation. Xen pioneered Paravirtualization by replacing sensitive instructions with explicit hypercalls.",
                "key_takeaway": "Hardware-assisted virtualization (Intel VT-x / AMD-V) introduced root and non-root execution rings, eliminating the need for complex binary translation."
            },
            {
                "topic": "3. Service Level Agreements (SLA) and Cloud Metrics",
                "analogy": "An SLA is like a contract with an electricity company: if the power cuts out for more than 5 minutes a month, they pay you a penalty rebate.",
                "deep_dive": "Key SLA contractual parameters include: RTO (Recovery Time Objective - target time to resume business after failure), RPO (Recovery Point Objective - maximum acceptable data loss in time), MTTF (Mean Time To Failure), and MTTR (Mean Time To Repair). SLA violations trigger service credit penalties.",
                "key_takeaway": "Remember: High Availability is multiplicative in series ($A_{total} = A_1 \\times A_2$) and redundant in parallel ($A_{total} = 1 - (1 - A_1)(1 - A_2)$)."
            }
        ],
        "mcqs": [
            {
                "id": "cc_q1",
                "question": "Which of the following hypervisors runs directly on bare-metal host hardware without requiring an underlying host operating system?",
                "options": [
                    "A) Oracle VirtualBox",
                    "B) VMware ESXi",
                    "C) VMware Workstation",
                    "D) QEMU (in pure emulation mode)"
                ],
                "correct_answers": [1],
                "type": "single",
                "difficulty": "Easy",
                "explanation": "VMware ESXi is a Type-1 (bare-metal) hypervisor running directly on physical hardware. VirtualBox and VMware Workstation are Type-2 hosted hypervisors.",
                "hint": "Look for enterprise data-center grade hypervisors.",
                "topic_tag": "Hypervisors"
            },
            {
                "id": "cc_q2",
                "question": "Which of the following are essential characteristics of cloud computing according to the NIST definition? (Select all that apply)",
                "options": [
                    "A) On-demand self-service",
                    "B) Broad network access",
                    "C) Resource pooling",
                    "D) Rapid elasticity",
                    "E) Fixed physical server dedication"
                ],
                "correct_answers": [0, 1, 2, 3],
                "type": "multiple",
                "difficulty": "Medium",
                "explanation": "NIST defines five essential characteristics: On-demand self-service, Broad network access, Resource pooling, Rapid elasticity, and Measured service. Dedicated fixed physical servers violate multi-tenant resource pooling.",
                "hint": "There are 5 NIST characteristics. Dedicated physical allocation is contrary to cloud.",
                "topic_tag": "NIST Characteristics"
            },
            {
                "id": "cc_q3",
                "question": "In a cloud service system, if the Mean Time To Failure (MTTF) is 990 hours and the Mean Time To Repair (MTTR) is 10 hours, what is the system availability?",
                "options": [
                    "A) 90.0%",
                    "B) 95.0%",
                    "C) 99.0%",
                    "D) 99.9%"
                ],
                "correct_answers": [2],
                "type": "single",
                "difficulty": "Medium",
                "explanation": "Availability $A = \\frac{\\text{MTTF}}{\\text{MTTF} + \\text{MTTR}} = \\frac{990}{990 + 10} = \\frac{990}{1000} = 0.99 = 99.0\\%$.",
                "hint": "Apply the standard formula: MTTF / (MTTF + MTTR).",
                "topic_tag": "SLA Metrics"
            },
            {
                "id": "cc_q4",
                "question": "What is the primary difference between full virtualization and paravirtualization?",
                "options": [
                    "A) Paravirtualization does not use any hypervisor at all",
                    "B) Full virtualization requires modifications to the guest operating system kernel",
                    "C) Paravirtualization modifies the guest OS to use hypercalls for interacting with the hypervisor",
                    "D) Paravirtualization can only run Windows guest operating systems"
                ],
                "correct_answers": [2],
                "type": "single",
                "difficulty": "Hard",
                "explanation": "In paravirtualization, the guest operating system's kernel is modified to execute explicit hypercalls instead of sensitive unvirtualizable instructions, yielding high I/O efficiency.",
                "hint": "Think about what is modified in the guest kernel.",
                "topic_tag": "Virtualization Techniques"
            },
            {
                "id": "cc_q5",
                "question": "Which of the following statements correctly differentiates between Cloud Scalability and Cloud Elasticity?",
                "options": [
                    "A) Elasticity is manual, whereas Scalability is automatic",
                    "B) Scalability is the ability to handle growth over time; Elasticity is the ability to adapt to variable workloads dynamically in real-time",
                    "C) Scalability applies only to storage, Elasticity applies only to CPU",
                    "D) There is no technical difference between the two terms"
                ],
                "correct_answers": [1],
                "type": "single",
                "difficulty": "Hard",
                "explanation": "Scalability refers to the planned capacity of a system to grow (scale up/out). Elasticity is the instantaneous autonomic scaling in and out based on fluctuating traffic.",
                "hint": "Elastic bands stretch and contract quickly to match load.",
                "topic_tag": "Cloud Concepts"
            }
        ],
        "flashcards": [
            {
                "front": "What are the 5 NIST Cloud Characteristics?",
                "back": "1. On-demand self-service\n2. Broad network access\n3. Resource pooling\n4. Rapid elasticity\n5. Measured service",
                "tag": "NIST Definition"
            },
            {
                "front": "Type-1 Hypervisor vs Type-2 Hypervisor",
                "back": "Type-1: Runs directly on bare metal (ESXi, KVM, Xen).\nType-2: Runs on top of a Host OS (VirtualBox, VMware Workstation).",
                "tag": "Virtualization"
            },
            {
                "front": "System Availability Formula",
                "back": "Availability (%) = [MTTF / (MTTF + MTTR)] * 100",
                "tag": "SLA Formula"
            },
            {
                "front": "What is a 'Hypercall'?",
                "back": "A software trap to the hypervisor, analogous to a system call (syscall) from user space to the OS kernel.",
                "tag": "Paravirtualization"
            },
            {
                "front": "Difference between RTO and RPO",
                "back": "RTO (Recovery Time Objective): Maximum acceptable downtime duration.\nRPO (Recovery Point Objective): Maximum acceptable age of data lost in time.",
                "tag": "Disaster Recovery"
            }
        ],
        "sample_doubts": [
            "Why is KVM classified as a Type-1 hypervisor when Linux is already running?",
            "How do we calculate availability for two independent cloud servers in parallel?",
            "What is the difference between Live Migration and Cold Migration of VMs?"
        ]
    },
    "dsa_algorithms": {
        "id": "dsa_algorithms",
        "title": "NPTEL: Data Structures & Algorithms",
        "instructor": "Prof. Madhavan Mukund (CMI / NPTEL)",
        "week": "Week 4: Graph Traversal, Shortest Paths & Minimum Spanning Trees",
        "total_pages": 14,
        "total_words": 4100,
        "estimated_read_time_mins": 20,
        "overview": "NPTEL core algorithm module covering BFS, DFS, Dijkstra's Single Source Shortest Path, Bellman-Ford algorithm for negative edge weights, Prim's and Kruskal's MST algorithms.",
        "key_points": [
            {
                "category": "Graph Traversal",
                "title": "BFS vs DFS Complexity & Applications",
                "content": "Both BFS and DFS run in $O(V + E)$ time using Adjacency Lists. BFS uses a Queue (finds shortest path in unweighted graphs). DFS uses a Stack/recursion (detects cycles, topological sort, strongly connected components)."
            },
            {
                "category": "Shortest Path",
                "title": "Dijkstra's Algorithm Limitations",
                "content": "Greedy approach. Time complexity $O((V + E) \\log V)$ using Min-Heap / Priority Queue. Cannot handle negative edge weights or negative weight cycles."
            },
            {
                "category": "Dynamic Programming",
                "title": "Bellman-Ford Algorithm",
                "content": "Handles negative edge weights. Relaxes all $|V|-1$ edges $|V|-1$ times. Running time $O(V \\cdot E)$. A $|V|$-th relaxation pass detects negative weight cycles reachable from the source."
            },
            {
                "category": "Greedy MST",
                "title": "Kruskal's vs Prim's MST",
                "content": "Kruskal's sorts edges and uses Disjoint Set Union (Union-Find) with path compression: $O(E \\log E)$. Prim's grows a tree using Min-Heap: $O(E \\log V)$. Prim's is preferred for dense graphs, Kruskal's for sparse graphs."
            },
            {
                "category": "Exam Pitfall",
                "title": "Cut Property and Cycle Property",
                "content": "The lightest edge crossing any cut $(S, V \\setminus S)$ is always in some MST (Cut Property). The heaviest edge in any cycle can never be part of a unique MST (Cycle Property)."
            }
        ],
        "conceptual_explanations": [
            {
                "topic": "1. Dijkstra's Algorithm and the Greedy Choice Property",
                "analogy": "Imagine water rippling outward from a dropped pebble. The water naturally reaches the closest obstacles first before proceeding further.",
                "deep_dive": "Dijkstra maintains a set of visited vertices whose shortest distances are permanently finalized. Once a vertex $u$ with minimum tentative distance is extracted from the priority queue, we know no shorter path to $u$ can be found—provided all edge weights are non-negative ($w(e) \\ge 0$).",
                "key_takeaway": "If negative edges exist, the greedy invariant breaks because an edge traversed later could retroactively decrease an already finalized distance."
            },
            {
                "topic": "2. Bellman-Ford: Why |V| - 1 iterations suffice",
                "analogy": "Like news traveling along a chain of friends: if there are $N$ people in line, a rumor takes at most $N-1$ handoffs to travel from the first person to the last.",
                "deep_dive": "Any simple shortest path in a graph with $|V|$ vertices can contain at most $|V|-1$ edges. In iteration $k$, Bellman-Ford guarantees finding the true shortest path for all vertices reachable via at most $k$ edges. Therefore, after $|V|-1$ passes, all shortest paths are computed.",
                "key_takeaway": "If distances can still be relaxed in the $|V|$-th iteration, a negative cycle exists!"
            },
            {
                "topic": "3. Minimum Spanning Tree: Prim vs Kruskal",
                "analogy": "Prim is like a mold growing outward continuously from a single spore. Kruskal is like multiple small islands building bridges until all islands merge into one continent.",
                "deep_dive": "An MST connects all vertices with $|V|-1$ edges minimizing the total edge weight without introducing cycles. Kruskal's relies on the cycle property; Prim's relies on the cut property.",
                "key_takeaway": "The total weight of an MST is unique, but the tree itself is only unique if all edge weights are distinct."
            }
        ],
        "mcqs": [
            {
                "id": "dsa_q1",
                "question": "What is the time complexity of Dijkstra's algorithm implemented using an adjacency list and a binary min-heap for a graph $G = (V, E)$?",
                "options": [
                    "A) $O(V^2)$",
                    "B) $O((V + E) \\log V)$",
                    "C) $O(V \\cdot E)$",
                    "D) $O(E \\log E + V^2)$"
                ],
                "correct_answers": [1],
                "type": "single",
                "difficulty": "Medium",
                "explanation": "With an adjacency list and binary min-heap, extracting min takes $O(V \\log V)$ and decreasing keys takes $O(E \\log V)$, totaling $O((V + E) \\log V)$.",
                "hint": "Heap operations take logarithmic time in terms of vertices.",
                "topic_tag": "Shortest Path"
            },
            {
                "id": "dsa_q2",
                "question": "Which of the following algorithms can detect the presence of a negative weight cycle in a directed graph? (Select all that apply)",
                "options": [
                    "A) Dijkstra's Algorithm",
                    "B) Bellman-Ford Algorithm",
                    "C) Floyd-Warshall Algorithm",
                    "D) Standard Breadth First Search (BFS)"
                ],
                "correct_answers": [1, 2],
                "type": "multiple",
                "difficulty": "Hard",
                "explanation": "Both Bellman-Ford (via a $|V|$-th relaxation pass) and Floyd-Warshall (if diagonal $d[i][i] < 0$) detect negative weight cycles. Dijkstra and BFS fail with negative weights.",
                "hint": "Dijkstra assumes non-negative weights. Look for dynamic programming approaches.",
                "topic_tag": "Negative Cycles"
            },
            {
                "id": "dsa_q3",
                "question": "In a graph with $V$ vertices and $E$ edges, if all edge weights are distinct, how many distinct Minimum Spanning Trees can exist?",
                "options": [
                    "A) Exactly 1 unique MST",
                    "B) $V - 1$",
                    "C) $2^{V}$",
                    "D) Cannot be determined without edge values"
                ],
                "correct_answers": [0],
                "type": "single",
                "difficulty": "Easy",
                "explanation": "Theorem: If all edge weights in a connected weighted graph are strictly distinct, the graph has exactly ONE unique Minimum Spanning Tree.",
                "hint": "Think about the cut and cycle properties when ties do not exist.",
                "topic_tag": "Minimum Spanning Tree"
            },
            {
                "id": "dsa_q4",
                "question": "Suppose an undirected connected graph $G$ has 10 vertices and 15 edges. What is the exact number of edges in any Spanning Tree of $G$?",
                "options": [
                    "A) 15",
                    "B) 10",
                    "C) 9",
                    "D) 8"
                ],
                "correct_answers": [2],
                "type": "single",
                "difficulty": "Easy",
                "explanation": "A spanning tree of any connected graph with $V$ vertices always contains exactly $V - 1$ edges. Here $10 - 1 = 9$ edges.",
                "hint": "Formula for tree edges with V vertices is V - 1.",
                "topic_tag": "Spanning Trees"
            },
            {
                "id": "dsa_q5",
                "question": "What happens if we run Bellman-Ford on a graph containing a negative weight cycle reachable from the source vertex?",
                "options": [
                    "A) It terminates normally with the correct shortest path values",
                    "B) It enters an infinite loop and crashes",
                    "C) The $|V|$-th relaxation check will still find a shorter distance, signaling the cycle",
                    "D) It converts negative edge weights to positive values automatically"
                ],
                "correct_answers": [2],
                "type": "single",
                "difficulty": "Medium",
                "explanation": "Bellman-Ford runs for $|V|-1$ passes. If after that, any edge $(u,v)$ still satisfies $d[u] + w(u,v) < d[v]$, it proves a negative cycle is reachable.",
                "hint": "The algorithm terminates after its fixed loop iterations and detects the anomaly.",
                "topic_tag": "Bellman-Ford"
            }
        ],
        "flashcards": [
            {
                "front": "Time Complexity of Bellman-Ford Algorithm",
                "back": "O(V * E) time, O(V) space. Relaxes all edges |V|-1 times.",
                "tag": "Shortest Path"
            },
            {
                "front": "Cut Property of Minimum Spanning Trees",
                "back": "For any cut in the graph, the minimum weight edge crossing the cut must belong to the MST.",
                "tag": "MST Theorems"
            },
            {
                "front": "Why can't Dijkstra handle negative edge weights?",
                "back": "Because its greedy invariant assumes once a vertex is marked visited/extracted, its distance is final and cannot be improved.",
                "tag": "Algorithm Invariants"
            },
            {
                "front": "What data structure optimizes Kruskal's Algorithm?",
                "back": "Disjoint Set Union (Union-Find) with Union by Rank and Path Compression (nearly linear time O(α(V))).",
                "tag": "Data Structures"
            }
        ],
        "sample_doubts": [
            "Why do we relax edges |V| - 1 times in Bellman-Ford?",
            "Can a graph have multiple shortest paths but only one MST?",
            "How does Floyd-Warshall solve all-pairs shortest paths in O(V^3)?"
        ]
    },
    "deep_learning": {
        "id": "deep_learning",
        "title": "NPTEL: Deep Learning & Neural Networks",
        "instructor": "Prof. Mitesh Khapra (IIT Madras)",
        "week": "Week 6: Convolutional Neural Networks (CNN) & Backpropagation",
        "total_pages": 16,
        "total_words": 4600,
        "estimated_read_time_mins": 23,
        "overview": "NPTEL Deep Learning core module detailing Convolution operations, kernel stride & padding formulas, Receptive Field, Max Pooling vs Average Pooling, vanishing gradient problem, and batch normalization.",
        "key_points": [
            {
                "category": "Convolution Formula",
                "title": "Output Feature Map Dimension Formula",
                "content": "For input size $W$, filter size $F$, padding $P$, and stride $S$: $$W_{out} = \\left\\lfloor \\frac{W - F + 2P}{S} \\right\\rfloor + 1$$"
            },
            {
                "category": "Core Principle",
                "title": "Parameter Sharing & Sparse Connectivity",
                "content": "Unlike Fully Connected layers where every input connects to every output, CNNs use shared kernel weights across all spatial locations, drastically reducing parameter count and achieving translation equivariance."
            },
            {
                "category": "Activation & Gradients",
                "title": "Vanishing Gradient Problem in Deep Networks",
                "content": "Sigmoid $\\sigma'(z) \\le 0.25$ causes exponential gradient decay during backprop across deep layers. ReLU ($f(x) = \\max(0, x)$) solves this with derivative $1$ for $x > 0$, though it can suffer from 'Dying ReLU'."
            },
            {
                "category": "Regularization",
                "title": "Batch Normalization & Dropout",
                "content": "Batch Normalization normalizes activations across mini-batches, smoothing loss landscape and accelerating convergence. Dropout randomly zeroes activations with probability $p$ during training to prevent co-adaptation."
            },
            {
                "category": "Exam Pitfall",
                "title": "Total Parameters in a Conv Layer (NPTEL Calculation)",
                "content": "Formula: $\\text{Params} = (K_w \\times K_h \\times C_{in} + 1) \\times C_{out}$, where $+1$ accounts for the bias per filter."
            }
        ],
        "conceptual_explanations": [
            {
                "topic": "1. Convolution Operation vs Cross-Correlation",
                "analogy": "A convolutional filter is like a flashlight sliding across a dark painting, highlighting specific patterns (edges, corners, textures) wherever its template matches.",
                "deep_dive": "Strict mathematical convolution flips the kernel by 180 degrees before dot product. Deep learning frameworks (PyTorch, TensorFlow) actually implement cross-correlation without flipping, but we still refer to it as convolution since learned weights adapt symmetrically.",
                "key_takeaway": "Output channels $C_{out}$ equal the number of distinct filters applied to the input."
            },
            {
                "topic": "2. Pooling Layers and Downsampling",
                "analogy": "Max pooling is like looking at a group of students and only recording the tallest height—it preserves the dominant feature while reducing detailed spatial noise.",
                "deep_dive": "Max Pooling provides local translation invariance and halves spatial resolution (e.g. $2 \\times 2$ pool with stride 2). Crucially, pooling layers have ZERO learnable parameters, making them computationally lightweight.",
                "key_takeaway": "Modern architectures (like ResNet) often replace pooling with strided convolutions."
            },
            {
                "topic": "3. Receptive Field Expansion",
                "analogy": "Looking through a narrow straw you see a tiny spot, but as layers stack, the visual field widens like zooming out on Google Maps.",
                "deep_dive": "Stacking two $3 \\times 3$ convolutions yields an effective receptive field of $5 \\times 5$, but uses only $2 \\times (3^2) = 18$ parameters instead of $1 \\times (5^2) = 25$ parameters, plus inserts an additional non-linear activation in between.",
                "key_takeaway": "This is why VGG networks exclusively used small $3 \\times 3$ filters."
            }
        ],
        "mcqs": [
            {
                "id": "dl_q1",
                "question": "Given an input image of size $32 \\times 32 \\times 3$, we apply 10 convolutional filters of size $5 \\times 5$ with stride $S = 1$ and padding $P = 0$. What is the spatial size of the resulting feature map?",
                "options": [
                    "A) $28 \\times 28 \\times 10$",
                    "B) $30 \\times 30 \\times 10$",
                    "C) $32 \\times 32 \\times 3$",
                    "D) $27 \\times 27 \\times 10$"
                ],
                "correct_answers": [0],
                "type": "single",
                "difficulty": "Medium",
                "explanation": "Formula: $W_{out} = \\frac{W - F + 2P}{S} + 1 = \\frac{32 - 5 + 0}{1} + 1 = 27 + 1 = 28$. With 10 filters, output shape is $28 \\times 28 \\times 10$.",
                "hint": "Compute: (32 - 5) / 1 + 1.",
                "topic_tag": "CNN Dimensions"
            },
            {
                "id": "dl_q2",
                "question": "How many total learnable parameters (weights and biases) are in a convolutional layer with 16 filters of size $3 \\times 3$, acting on an input with 4 channels?",
                "options": [
                    "A) 192",
                    "B) 576",
                    "C) 592",
                    "D) 768"
                ],
                "correct_answers": [2],
                "type": "single",
                "difficulty": "Hard",
                "explanation": "Parameters per filter = $(3 \\times 3 \\times 4) + 1 \\text{ (bias)} = 36 + 1 = 37$. For 16 filters: $37 \\times 16 = 592$.",
                "hint": "Remember to include one bias term per filter!",
                "topic_tag": "Parameter Counting"
            },
            {
                "id": "dl_q3",
                "question": "Why does the ReLU activation function mitigate the vanishing gradient problem compared to Sigmoid?",
                "options": [
                    "A) ReLU's derivative is always 0",
                    "B) For positive inputs ($x > 0$), ReLU's derivative is a constant 1, preventing exponential shrinkage",
                    "C) ReLU bounds all activations between -1 and +1",
                    "D) ReLU computes faster by using exponential functions"
                ],
                "correct_answers": [1],
                "type": "single",
                "difficulty": "Easy",
                "explanation": "For $x > 0$, $\\frac{d}{dx}\\text{ReLU}(x) = 1$. Gradients pass through unchanged without being multiplied by numbers $< 0.25$ like in Sigmoid.",
                "hint": "Consider the derivative of max(0, x) for x > 0.",
                "topic_tag": "Activation Functions"
            },
            {
                "id": "dl_q4",
                "question": "Which of the following are properties of a standard Max Pooling layer? (Select all that apply)",
                "options": [
                    "A) It introduces learnable weight parameters",
                    "B) It provides translation invariance to minor shifts",
                    "C) It reduces the spatial dimensions (height and width) of the feature map",
                    "D) It changes the number of channels (depth) of the input"
                ],
                "correct_answers": [1, 2],
                "type": "multiple",
                "difficulty": "Medium",
                "explanation": "Max pooling has NO learnable parameters and operates independently on each channel (preserving channel depth), while shrinking spatial dimensions and giving local translation invariance.",
                "hint": "Does pooling have weights to train?",
                "topic_tag": "Pooling Layers"
            },
            {
                "id": "dl_q5",
                "question": "Stacking two successive $3 \\times 3$ convolutional layers (with stride 1) gives an effective receptive field equivalent to one layer with filter size:",
                "options": [
                    "A) $3 \\times 3$",
                    "B) $5 \\times 5$",
                    "C) $6 \\times 6$",
                    "D) $7 \\times 7$"
                ],
                "correct_answers": [1],
                "type": "single",
                "difficulty": "Medium",
                "explanation": "Layer 1 receptive field is $3 \\times 3$. In Layer 2, each cell looks at a $3 \\times 3$ neighborhood of Layer 1, expanding the field by $3 - 1 = 2$, yielding $3 + 2 = 5 \\times 5$.",
                "hint": "Effective receptive field grows as (F - 1) per subsequent layer.",
                "topic_tag": "Receptive Field"
            }
        ],
        "flashcards": [
            {
                "front": "Formula for Conv2D Output Size",
                "back": "W_out = floor((W - F + 2P)/S) + 1",
                "tag": "CNN Formula"
            },
            {
                "front": "Does Pooling Have Learnable Parameters?",
                "back": "NO! Max Pooling and Average Pooling compute fixed functions and have 0 learnable parameters.",
                "tag": "Architecture"
            },
            {
                "front": "Why is 2 x (3x3) conv preferred over 1 x (5x5) conv?",
                "back": "1. Same 5x5 receptive field\n2. Fewer parameters (18 vs 25)\n3. Two non-linearities instead of one for richer representation",
                "tag": "Design Principles"
            },
            {
                "front": "What causes 'Dying ReLU'?",
                "back": "When a large gradient updates weights such that the neuron never activates (input < 0) for any data point, derivative becomes permanently 0.",
                "tag": "Optimization"
            }
        ],
        "sample_doubts": [
            "How does Backpropagation calculate gradients through a Max Pooling layer?",
            "What is the mathematical difference between Batch Normalization and Layer Normalization?",
            "Why is 1x1 convolution called 'Network in Network'?"
        ]
    }
}
