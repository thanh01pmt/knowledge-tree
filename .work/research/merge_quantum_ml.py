import os

def insert_before_marker(lines, marker, new_lines):
    for i, line in enumerate(lines):
        if line.startswith(marker):
            return lines[:i] + new_lines + lines[i:]
    return lines + new_lines

def main():
    file_path = ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # 1. New Subject: QUANTUM_SYSTEMS (under CSN)
    new_subject = ["QUANTUM_SYSTEMS\tQuantum Systems\tStudy of quantum computing hardware and algorithms.\tCSN\tquantum, superposition, entanglement\t\t\n"]
    lines = insert_before_marker(lines, "Bảng 3:", new_subject)
    
    # 2. New Category: QUANTUM_MACHINE_LEARNING (under QUANTUM_SYSTEMS)
    new_category = ["QUANTUM_MACHINE_LEARNING\tQuantum Machine Learning\tIntersection of quantum computing and artificial intelligence.\tQUANTUM_SYSTEMS\tqml, quantum algorithms, variational\t\t\n"]
    lines = insert_before_marker(lines, "Bảng 4:", new_category)
    
    # 3. New Topics (under QUANTUM_MACHINE_LEARNING)
    new_topics = [
        "QUANTUM_MECHANICS_BASICS\tQuantum Mechanics Basics\tCore physics principles underlying quantum computing.\tQUANTUM_MACHINE_LEARNING\tqubits, superposition, entanglement\t\t\n",
        "QUANTUM_CIRCUITS_AND_GATES\tQuantum Circuits and Gates\tLogic gates and circuits for quantum state manipulation.\tQUANTUM_MACHINE_LEARNING\tquantum gates, unitary, cirq, qiskit\t\t\n",
        "HYBRID_QUANTUM_CLASSICAL_AI\tHybrid Quantum-Classical AI\tAI systems combining classical and quantum processing.\tQUANTUM_MACHINE_LEARNING\tqnn, parameterized circuits, vqe\t\t\n"
    ]
    lines = insert_before_marker(lines, "Bảng 5:", new_topics)
    
    # 4. New Concepts
    new_concepts = [
        "QUANTUM_STATES_SUPERPOSITION\tQuantum States and Superposition\tQubits, Dirac Notation, Superposition, Measurement.\tQUANTUM_MECHANICS_BASICS\tqubits, superposition\t\t\n",
        "QUANTUM_ENTANGLEMENT\tQuantum Entanglement\tBell States, Spooky Action, Quantum Correlation.\tQUANTUM_MECHANICS_BASICS\tentanglement\t\t\n",
        "QUANTUM_LOGIC_GATES\tQuantum Logic Gates\tPauli-X/Y/Z, Hadamard, CNOT, Quantum Circuits.\tQUANTUM_CIRCUITS_AND_GATES\tgates, hadamard, cnot\t\t\n",
        "PARAMETERIZED_QUANTUM_CIRCUITS\tParameterized Quantum Circuits\tQuantum Neural Networks, VQE, Ansatz, Hybrid Training.\tHYBRID_QUANTUM_CLASSICAL_AI\tpqc, qnn, vqe\t\t\n"
    ]
    lines = lines + new_concepts
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    # Also append to ULO bank (create file if it doesn't exist, though it's simulated as we are just tracking it)
    ulo_path = ".agents/skills/learning-objective-generator/resources/master_learning_objectives.tsv"
    os.makedirs(os.path.dirname(ulo_path), exist_ok=True)
    with open(ulo_path, "a", encoding="utf-8") as f:
        f.write("ULO-PARAMETERIZED_QUANTUM_CIRCUITS-01\tCreate Quantum Neural Network\tNgười học có khả năng thiết kế một kiến trúc mạng nơ-ron lượng tử bằng cách điều chỉnh các tham số quay của cổng lượng tử.\tUNIVERSAL\t\tPARAMETERIZED_QUANTUM_CIRCUITS\tCREATE\tPROCEDURAL\n")
        f.write("CIO-BUILD-VARIATIONAL-CIRCUIT\tBuild Variational Circuit\tNgười học có khả năng khởi tạo và cấu hình một mạch lượng tử lai cho bài toán tối ưu hóa.\tSPECIFIC_IMPL\tULO-PARAMETERIZED_QUANTUM_CIRCUITS-01\tPARAMETERIZED_QUANTUM_CIRCUITS\tAPPLY\tPROCEDURAL\n")
        f.write("CIO-OPTIMIZE-QUANTUM-GRADIENTS\tOptimize Quantum Gradients\tNgười học có khả năng triển khai vòng lặp gradient descent để cập nhật tham số lượng tử (Parameter Shift Rule).\tSPECIFIC_IMPL\tULO-PARAMETERIZED_QUANTUM_CIRCUITS-01\tPARAMETERIZED_QUANTUM_CIRCUITS\tAPPLY\tPROCEDURAL\n")

if __name__ == "__main__":
    main()
