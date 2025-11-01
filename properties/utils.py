from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    
    properties = cache.get('all_properties')
    
    if not properties:
        properties = list(Property.objects.all().values(
            "property_id", "title", "description", "price", "location", "created_at"
        ))
        cache.set('all_properties', properties, 3600)
    
    return properties

def get_redis_cache_metrics():
    
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")
        
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0.0
        
        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }
        
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error fetching Redis cache metrics: {e}")
        return {
            "keyspace_hits": None,
            "keyspace_misses": None,
            "hit_ratio": None,
        }
