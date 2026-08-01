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
        
    # Field: COMPUTER_SCIENCE (CSN exists, maybe we map to CSN or just use SWE? Let's use SWE for now or assume Field is known)
    # The report says Field: COMPUTER_SCIENCE. Actually we'll just use CSN (Computing Systems and Networks) or SWE (Software Engineering) 
    # Let's assume CSN for Discrete Math.
    
    # 1. New Subject: MATHEMATICAL_FOUNDATIONS (under CSN)
    new_subject = ["MATHEMATICAL_FOUNDATIONS\tMathematical Foundations\tCore mathematical principles underlying computing.\tCSN\t40\tmath, discrete\t\t\n"]
    lines = insert_before_marker(lines, "Bảng 3:", new_subject)
    
    # 2. New Category: DISCRETE_STRUCTURES (under MATHEMATICAL_FOUNDATIONS)
    new_category = ["DISCRETE_STRUCTURES\tDiscrete Structures\tStudy of mathematical structures that are fundamentally discrete rather than continuous.\tMATHEMATICAL_FOUNDATIONS\t10\tlogic, sets, graphs\t\t\n"]
    lines = insert_before_marker(lines, "Bảng 4:", new_category)
    
    # 3. New Topics
    new_topics = [
        "MATHEMATICAL_LOGIC\tMathematical Logic\tFormal logic and reasoning.\tDISCRETE_STRUCTURES\t10\tlogic, propositions\t\t\n",
        "SET_AND_RELATION_THEORY\tSet and Relation Theory\tSets, relations, and functions.\tDISCRETE_STRUCTURES\t20\tsets, relations\t\t\n",
        "DISCRETE_COMBINATORICS\tDiscrete Combinatorics\tCounting and combinatorics.\tDISCRETE_STRUCTURES\t30\tcounting, permutations\t\t\n",
        "GRAPH_AND_TREE_STRUCTURES\tGraph and Tree Structures\tGraphs and trees theory.\tDISCRETE_STRUCTURES\t40\tgraphs, trees\t\t\n"
    ]
    lines = insert_before_marker(lines, "Bảng 5:", new_topics)
    
    # 4. New Concepts
    new_concepts = [
        "PROPOSITIONAL_LOGIC\tPropositional Logic\tLogic and boolean operators.\tMATHEMATICAL_LOGIC\t10\tlogic, boolean\t\t\n",
        "SET_THEORY\tSet Theory\tSets, subsets, operations.\tSET_AND_RELATION_THEORY\t10\tsets, unions\t\t\n",
        "COMBINATORICS\tCombinatorics\tPermutations, combinations, counting.\tDISCRETE_COMBINATORICS\t10\tcounting\t\t\n",
        "GRAPH_THEORY\tGraph Theory\tVertices, edges, traversal.\tGRAPH_AND_TREE_STRUCTURES\t10\tgraphs, trees\t\t\n"
    ]
    lines = lines + new_concepts
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    # Also append to ULO bank
    ulo_path = ".agents/skills/learning-objective-generator/resources/master_learning_objectives.tsv"
    if os.path.exists(ulo_path):
        with open(ulo_path, "a", encoding="utf-8") as f:
            f.write("ULO-PROPOSITIONAL_LOGIC-01\tEvaluate Boolean Expression\tNgười học có khả năng đánh giá tính đúng đắn của một hệ thống các quy tắc điều kiện dựa trên bảng chân trị.\tUNIVERSAL\t\tPROPOSITIONAL_LOGIC\tEVALUATE\tPROCEDURAL\n")
            f.write("CIO-EVALUATE-BOOLEAN-EXPRESSION\tEvaluate Boolean Expression\tNgười học có khả năng phân giải và tính toán kết quả của một biểu thức logic phức hợp.\tSPECIFIC_IMPL\tULO-PROPOSITIONAL_LOGIC-01\tPROPOSITIONAL_LOGIC\tAPPLY\tPROCEDURAL\n")
            f.write("CIO-SIMPLIFY-LOGIC-CIRCUIT\tSimplify Logic Circuit\tNgười học có khả năng rút gọn một chuỗi các biểu thức điều kiện bằng định lý De Morgan.\tSPECIFIC_IMPL\tULO-PROPOSITIONAL_LOGIC-01\tPROPOSITIONAL_LOGIC\tANALYZE\tPROCEDURAL\n")
            
            f.write("ULO-GRAPH_THEORY-01\tAnalyze Graph Connections\tNgười học có khả năng phân tích và thiết kế các mô hình mạng lưới dựa trên đặc tính kết nối của đồ thị.\tUNIVERSAL\t\tGRAPH_THEORY\tANALYZE\tPROCEDURAL\n")
            f.write("CIO-TRAVERSE-CONNECTED-NODES\tTraverse Connected Nodes\tNgười học có khả năng triển khai thuật toán duyệt qua tất cả các đỉnh liên thông trong một mạng lưới.\tSPECIFIC_IMPL\tULO-GRAPH_THEORY-01\tGRAPH_THEORY\tAPPLY\tPROCEDURAL\n")
            f.write("CIO-FIND-SHORTEST-PATH\tFind Shortest Path\tNgười học có khả năng tính toán đường đi tối ưu nhất giữa hai điểm trong một hệ thống có trọng số.\tSPECIFIC_IMPL\tULO-GRAPH_THEORY-01\tGRAPH_THEORY\tAPPLY\tPROCEDURAL\n")

if __name__ == "__main__":
    main()
