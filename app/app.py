from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging, time, random, os
from pythonjsonlogger import jsonlogger

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagate import set_global_textmap

# Logging (JSON)
logger = logging.getLogger("obs_app")
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Prometheus metrics
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency seconds')

# Tracing setup
service_name = os.getenv("OTEL_SERVICE_NAME", "observability-demo")
trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": service_name})))
jaeger_exporter = JaegerExporter(
    collector_endpoint=os.getenv("OTEL_EXPORTER_JAEGER_ENDPOINT", "http://jaeger:14268/api/traces"),
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))
set_global_textmap(B3MultiFormat())
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.before_request
def before():
    request.start_time = time.time()

@app.after_request
def after(response):
    duration = time.time() - getattr(request, "start_time", time.time())
    REQUEST_COUNTER.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    REQUEST_LATENCY.observe(duration)
    logger.info("request_complete", extra={
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_ms": int(duration*1000),
        "request_id": request.headers.get("X-Request-Id", "")
    })
    return response

@app.route("/")
def index():
    with tracer.start_as_current_span("index-handler"):
        time.sleep(random.uniform(0.01, 0.15))
        return jsonify({"msg": "hello from observability demo"})

@app.route("/error")
def error():
    with tracer.start_as_current_span("error-handler"):
        logger.error("simulated_error", extra={"path": "/error"})
        return jsonify({"msg": "error"}), 500

@app.route("/external")
def external():
    with tracer.start_as_current_span("external-call"):
        try:
            r = requests.get("https://api.github.com", timeout=2)
            return jsonify({"status": r.status_code}), 200
        except Exception as e:
            logger.error("external_failed", extra={"error": str(e)})
            return jsonify({"error": str(e)}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
