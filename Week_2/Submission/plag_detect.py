import heapq
import re
import PyPDF2

class AStarNode:
    def __init__(self, position, parent=None, g_cost=0, h_cost=0):
        self.position = position
        self.parent = parent
        self.g = g_cost
        self.h = h_cost
        self.f = g_cost + h_cost

    def __lt__(self, other):
        return self.f < other.f


def expand_node(node, seq1, seq2):
    neighbors = []
    i, j = node.position

    if i < len(seq1) and j < len(seq2):
        neighbors.append(AStarNode((i + 1, j + 1), node))
    if i < len(seq1):
        neighbors.append(AStarNode((i + 1, j), node))
    if j < len(seq2):
        neighbors.append(AStarNode((i, j + 1), node))

    return neighbors


def clean_text(sentence):
    return re.sub(r'[^\w\s]', '', sentence.lower())


def heuristic(pos, seq1, seq2):
    i, j = pos
    return (len(seq1) - i) + (len(seq2) - j)


def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for x in range(m + 1):
        for y in range(n + 1):
            if x == 0 or y == 0:
                table[x][y] = 0
            elif s1[x - 1] == s2[y - 1]:
                table[x][y] = table[x - 1][y - 1]
            else:
                table[x][y] = 1 + min(table[x - 1][y], table[x][y - 1], table[x - 1][y - 1])
    return table[m][n]


def a_star_alignment(seq1, seq2):
    start_pos = (0, 0)
    goal_pos = (len(seq1), len(seq2))
    start_node = AStarNode(start_pos)
    open_heap = []
    heapq.heappush(open_heap, (start_node.f, start_node))
    visited = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current.position in visited:
            continue
        visited.add(current.position)

        if current.position == goal_pos:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        for neighbor in expand_node(current, seq1, seq2):
            ni, nj = neighbor.position
            if ni < len(seq1) and nj < len(seq2):
                neighbor.g = current.g + levenshtein_distance(seq1[ni], seq2[nj])
            else:
                neighbor.g = current.g + 1
            neighbor.h = heuristic(neighbor.position, seq1, seq2)
            neighbor.f = neighbor.g + neighbor.h
            heapq.heappush(open_heap, (neighbor.f, neighbor))

    return None


def detect_plagiarism(document1, document2):
    doc1_clean = [clean_text(s) for s in document1]
    doc2_clean = [clean_text(s) for s in document2]

    aligned_positions = a_star_alignment(doc1_clean, doc2_clean)
    matches = []

    for i, j in aligned_positions:
        if i < len(doc1_clean) and j < len(doc2_clean):
            s1, s2 = doc1_clean[i], doc2_clean[j]
            max_len = max(len(s1), len(s2))
            if max_len > 0:
                similarity = 1 - (levenshtein_distance(s1, s2) / max_len)
                if similarity >= 0.5:
                    matches.append((document1[i], document2[j], similarity))
    return matches


def extract_pdf_sentences(pdf_path):
    sentences = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                for sentence in re.split(r'(?<=[.!?]) +', text):
                    if sentence.strip():
                        sentences.append(sentence.strip())
    return sentences


if __name__ == "__main__":
    pdf1_path = "sample1.pdf"
    pdf2_path = "sample2.pdf"

    doc1_sentences = extract_pdf_sentences(pdf1_path)
    doc2_sentences = extract_pdf_sentences(pdf2_path)

    results = detect_plagiarism(doc1_sentences, doc2_sentences)

    if results:
        print("Potential plagiarism detected:")
        for d1, d2, sim in results:
            print(f"Doc1: {d1}\nDoc2: {d2}\nSimilarity: {sim*100:.2f}%\n")
    else:
        print("No plagiarism detected.")