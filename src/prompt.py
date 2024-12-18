# Prompt
router_instructions ="""
You are an expert at routing user questions to a vectorstore or web search.

The vectorstore contains information from the "Mieux Vivre 2024" guide, produced by the INSPQ (https://www.inspq.qc.ca/mieux-vivre). The "Mieux Vivre 2024" guide provides comprehensive information on pregnancy, childbirth, newborn care, child development, breastfeeding, nutrition, safety, and the well-being of children and parents. It is a trusted resource for parents and families seeking guidance from conception through early childhood.

Use the vectorstore for questions on these topics. For all else, and especially for current events, use web-search.
Return JSON with single key, datasource, that is 'websearch' or 'vectorstore' depending on the question.
"""


# Doc grader instructions
doc_grader_instructions = """
You are a grader assessing relevance of a retrieved document to a user question.
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
"""

# Grader prompt
doc_grader_prompt = """
Here is the retrieved document: 
<document>
{document} 
</document>

Here is the user question: 
<question>
{question}
</question>

Carefully and objectively assess whether the document contains some information that can answer the question.
Return JSON with single key, binary_score, that is 'yes' or 'no' score to indicate whether the document contains at least some information that is relevant to the question.
The document and the question are in french.
"""


# Prompt
rag_prompt = """
You are an assistant for question-answering tasks. 
Here is the context to use to answer the question:
{context} 
Think carefully about the above context. 
Now, review the user question:
{question}
Provide an answer to this questions using only the above context. 
Use three sentences maximum and keep the answer concise.
Answer:"""


# Hallucination grader instructions
hallucination_grader_instructions = """
You are a teacher grading a quiz. 
You will be given FACTS and a STUDENT ANSWER. 
Here is the grade criteria to follow:
(1) Ensure the STUDENT ANSWER is grounded in the FACTS. 
(2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.
Score:
A score of yes means that the student's answer meets all of the criteria. This is the highest (best) score. 
A score of no means that the student's answer does not meet all of the criteria. This is the lowest possible score you can give.
Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 
Avoid simply stating the correct answer at the outset.
"""
