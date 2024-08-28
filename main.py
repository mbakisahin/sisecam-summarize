import uvicorn
from fastapi import FastAPI, HTTPException
import config
from processors.pipeline import PipelineCoordinator
from utils.system_messages import SYSTEM_MESSAGE_FINAL, SYSTEM_MESSAGE_SUMMARIZATION

# app = FastAPI()
#
# @app.on_event("startup")
# async def startup_event():
#     """
#     Initializes any components or configurations on startup.
#     """
#     config.app_logger.info("FastAPI app startup initiated.")
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     """
#     Cleanup operations on shutdown.
#     """
#     config.app_logger.info("FastAPI app shutdown initiated.")
#
# @app.get("/")
# async def read_root():
#     return {"message": "FastAPI application is running."}
#
# @app.post("/run-pipeline")
# async def run_pipeline():
#     """
#     Endpoint to trigger the pipeline process.
#     """
#     try:
#         config.app_logger.info("Pipeline process started via API.")
#
#         pipeline_coordinator = PipelineCoordinator()
#         pipeline_coordinator.run(SYSTEM_MESSAGE_SUMMARIZATION, SYSTEM_MESSAGE_FINAL)
#
#         config.app_logger.info("Pipeline process completed successfully.")
#         return {"status": "Pipeline completed successfully."}
#
#     except Exception as e:
#         config.app_logger.error(f"Error during pipeline execution: {str(e)}")
#         raise HTTPException(status_code=500, detail="An error occurred while running the pipeline.")
#
def main():
    try:
        config.app_logger.info("Pipeline process started via API.")

        pipeline_coordinator = PipelineCoordinator()
        pipeline_coordinator.run(SYSTEM_MESSAGE_SUMMARIZATION, SYSTEM_MESSAGE_FINAL)

        config.app_logger.info("Pipeline process completed successfully.")
        return {"status": "Pipeline completed successfully."}

    except Exception as e:
        config.app_logger.error(f"Error during pipeline execution: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while running the pipeline.")

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    main()
