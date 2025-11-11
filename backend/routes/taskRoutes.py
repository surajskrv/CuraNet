from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from backend.utils import role_required, get_current_user
import io

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/export-history', methods=['POST'])
@jwt_required()
@role_required('patient')
def trigger_csv_export(user):
    """Trigger CSV export of patient history"""
    from backend.app import celery
    
    if not celery:
        return jsonify({'message': 'Background jobs are not available. Please ensure Redis is running.'}), 503
    
    patient_id = user.id
    
    # Trigger async task using the registered task
    task = celery.export_patient_history_csv.delay(patient_id)
    
    return jsonify({
        'message': 'CSV export started',
        'task_id': task.id,
        'status': 'processing'
    }), 202

@task_bp.route('/export-history/<task_id>', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_csv_export_status(user, task_id):
    """Get status of CSV export task and download if ready"""
    from backend.app import celery
    
    if not celery:
        return jsonify({'message': 'Background jobs are not available.'}), 503
    
    task = celery.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Waiting to be processed...'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', 'Processing...')
        }
    elif task.state == 'SUCCESS':
        csv_content = task.result
        
        if csv_content:
            # Return CSV file
            csv_bytes = io.BytesIO(csv_content.encode('utf-8'))
            
            return send_file(
                csv_bytes,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'patient_history_{user.id}_{task_id[:8]}.csv'
            )
        else:
            return jsonify({
                'state': task.state,
                'status': 'Export completed but no data found'
            }), 200
    else:
        response = {
            'state': task.state,
            'status': 'Export failed',
            'error': str(task.info) if task.info else 'Unknown error'
        }
    
    return jsonify(response), 200 if task.state != 'FAILURE' else 500

