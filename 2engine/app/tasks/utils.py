from .documents import TaskDocument
from elasticsearch_dsl.query import MultiMatch

def q_search(query):

    q = MultiMatch(query=query,  fields=['description', 'name'], fuzziness=2)

    result = TaskDocument.search().query(q)
    total = result.count()
    tasks = result[0:total]

    return tasks.to_queryset()  