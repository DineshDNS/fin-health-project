import uuid

DOCUMENTS = []

class DocumentStore:

    @staticmethod
    def save(data):
        doc = {"document_id": f"doc_{uuid.uuid4().hex[:6]}", **data}
        DOCUMENTS.append(doc)
        return doc

    @staticmethod
    def delete(document_id):
        global DOCUMENTS
        DOCUMENTS = [d for d in DOCUMENTS if d["document_id"] != document_id]

    @staticmethod
    def all():
        return DOCUMENTS
