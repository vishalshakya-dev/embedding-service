from fastembed import TextEmbedding
from flask import Flask, request, jsonify
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize model
try:
    logger.info("Loading FastEmbed model...")
    embedding_model = TextEmbedding()
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    exit(1)

def log_timing(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
            processing_time = time.time() - start_time
            logger.info(f"Request completed in {processing_time:.3f}s")
            return result
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Request failed after {processing_time:.3f}s: {str(e)}")
            raise
    return decorated_function

@app.route('/embed', methods=['POST'])
@log_timing
def embed_text():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    try:
        embeddings = list(embedding_model.embed([text]))
        embedding = embeddings[0].tolist()
        
        return jsonify({
            'embedding': embedding,
            'dimensions': len(embedding),
            'model': 'fastembed'
        })
    except Exception as e:
        logger.error(f"Embedding failed: {str(e)}")
        return jsonify({'error': 'Failed to generate embedding'}), 500

@app.route('/embed/batch', methods=['POST'])
@log_timing
def embed_batch():
    data = request.get_json()
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({'error': 'Texts array is required'}), 400
    
    try:
        embeddings = list(embedding_model.embed(texts))
        
        return jsonify({
            'embeddings': [emb.tolist() for emb in embeddings],
            'model': 'fastembed',
            'count': len(embeddings)
        })
    except Exception as e:
        logger.error(f"Batch embedding failed: {str(e)}")
        return jsonify({'error': 'Failed to generate batch embeddings'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model': 'fastembed',
        'ready': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)