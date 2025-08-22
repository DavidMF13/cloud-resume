import logging
import azure.functions as func
import os
import json
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError

# --- 1. Configuration and Client Initialization ---
# It's a best practice to get sensitive information from environment variables
# rather than hardcoding it in the script. You must set these values
# in your local environment or in the Azure Portal before deployment.

# The URL and key for your Cosmos DB account.
# Replace the placeholder values with your actual environment variable names.
# Use os.environ.get() to avoid a KeyError if the variable is not set.
COSMOS_DB_URL = os.environ.get("COSMOS_DB_URL")
COSMOS_DB_KEY = os.environ.get("COSMOS_DB_KEY")

# The names of your database and container.
DATABASE_NAME = "cloudresume"
CONTAINER_NAME = "visitors"

# Initialize variables to None to prevent NameError if connection fails
client = None
database = None
container = None

# Create a CosmosClient instance. This should be done once outside of the
# main function to reuse the connection across multiple function invocations,
# which improves performance.
try:
    client = CosmosClient(COSMOS_DB_URL, credential=COSMOS_DB_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    logging.info("Successfully connected to Cosmos DB.")
except Exception as e:
    logging.error(f"Error initializing Cosmos DB client: {e}")
    # Consider how to handle this error based on your application's needs.
    # For a simple function, it might be okay to let the invocation fail.

# --- 2. Main Azure Function ---
# This is the V2 programming model entry point. All functions are defined
# as methods on this `app` instance.
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="incrementCounter", methods=["get", "post"])
def incrementCounter(req: func.HttpRequest) -> func.HttpResponse:
    """
    This Azure Function handles an HTTP request to increment a visitor counter
    stored in a Cosmos DB document.

    Steps:
    1. Reads the document with the counter.
    2. Increments the 'count' value.
    3. Replaces the document in the container with the new value.
    4. Returns the updated count in a JSON response.
    """
    logging.info('HTTP trigger function processed a request.')
    
    # We must ensure our Cosmos DB client was initialized correctly.
    if not container:
        logging.error("Cosmos DB container client is not available.")
        return func.HttpResponse(
            "Cosmos DB client not initialized. Check application settings.",
            status_code=500
        )

    try:
        # Define the ID for the document you want to update.
        document_id = "resume-visitor-counter"
        # Since 'id' is often the partition key, we provide it here for a
        # more efficient point-read operation.
        partition_key = document_id

        # Read the current document from the container.
        document = container.read_item(item=document_id, partition_key=partition_key)

        # Get the current count and increment it.
        current_count = document.get("count", 0)
        document["count"] = current_count + 1

        # Replace the item in the container with the new, updated document.
        updated_document = container.replace_item(item=document, body=document)

        # Log the success and the new count.
        logging.info(f"Counter incremented successfully. New count: {updated_document['count']}")
        
        # Create a JSON response with the new count.
        response_data = {
            "id": updated_document.get("id"),
            "count": updated_document.get("count")
        }

        # Return a successful HTTP response.
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )

    except CosmosResourceNotFoundError:
        # If the document does not exist, return a 404 Not Found error.
        logging.error(f"Document with ID '{document_id}' not found.")
        return func.HttpResponse(
            f"The document '{document_id}' was not found in the database.",
            status_code=404
        )
    except Exception as e:
        # Catch any other unexpected errors and return a 500 Internal Server Error.
        logging.error(f"An unexpected error occurred: {e}")
        return func.HttpResponse(
            "An internal server error occurred.",
            status_code=500
        )
