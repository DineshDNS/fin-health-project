HISTORY = []

class DocumentHistory:

    @staticmethod
    def record(document_id, action, replaced_by=None):
        HISTORY.append({
            "document_id": document_id,
            "action": action,
            "replaced_by": replaced_by,
        })

    @staticmethod
    def all():
        return HISTORY
