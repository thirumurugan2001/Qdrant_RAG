from rag_utils.ragController import rag

# Controller function to handle the RAG process based on the provided question
def ragController(Question):
    try:
        # Check if the provided question is not empty before proceeding with the RAG process
        if Question != "":
            return rag(Question)
        else:
            return {
                "message":"Invaild data !",
                "statusCode":400,
                "Status":False
            }
    except Exception as e:
        print(f"Error in ragController controller.py file: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }