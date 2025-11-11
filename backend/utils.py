from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from backend.models import User
from backend.extensions import cache
import json
from jinja2 import Template

def format_report(html_template, data):
    with open(html_template) as file:
        template = Template(file.read())
        return template.render(data = data)

def safe_cache_get(key, default=None):
    """Safely get from cache, return default if Redis unavailable"""
    try:
        return cache.get(key) or default
    except Exception:
        return default

def safe_cache_set(key, value, timeout=300):
    """Safely set cache, silently fail if Redis unavailable"""
    try:
        cache.set(key, value, timeout=timeout)
    except Exception:
        pass  # Cache is optional, continue without it

def safe_cache_delete(key):
    """Safely delete from cache"""
    try:
        cache.delete(key)
    except Exception:
        pass

def role_required(required_role):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or user.role != required_role:
                return jsonify({'message': 'Access denied. Insufficient permissions.'}), 403
            
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current logged in user"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None

def cache_key_prefix(*args, **kwargs):
    """Generate cache key prefix"""
    key = f"{request.path}:{json.dumps(request.args, sort_keys=True)}"
    return key

def clear_cache_pattern(pattern):
    """Clear cache entries matching a pattern"""
    try:
        # Check if Redis client is available (for pattern matching)
        if hasattr(cache.cache, '_client') and cache.cache._client:
            keys = cache.cache._client.keys(pattern)
            if keys:
                cache.cache._client.delete(*keys)
                print(f"Cleared cache keys matching pattern: {pattern}")
        else:
            # For SimpleCache, we can't do pattern matching easily
            # Just log that pattern clearing is not available
            print(f"Pattern cache clearing not available (SimpleCache). Pattern: {pattern}")
    except Exception as e:
        print(f"Error clearing cache pattern {pattern}: {e}")
        pass  # Cache is optional
