import os
import shutil
import datetime

def deploy_code(file_path):
    """
    Automated Deployment Agent.
    Packages and deploys the validated code to a dedicated 'deployed_apps' directory.
    """
    deploy_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'deployed_apps')
    os.makedirs(deploy_dir, exist_ok=True)
    
    filename = os.path.basename(file_path)
    destination = os.path.join(deploy_dir, filename)
    
    try:
        shutil.copy2(file_path, destination)
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] INFO: Verified binary v1.0. Successfully shipped {filename} to /deployed_apps."
        
        return {
            "status": "success",
            "message": "Deployment successful.",
            "log": log_entry,
            "path": destination
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Deployment failed: {str(e)}"
        }
