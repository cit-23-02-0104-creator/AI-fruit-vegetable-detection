import os
import ssl
import json
import base64
import uvicorn
import socket
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from roboflow import Roboflow

import os

# Bypass Vercel's missing HOME variable issue
if not os.environ.get("HOME"):
    os.environ["HOME"] = "/tmp"

# Now import roboflow safely
from roboflow import Roboflow

# ... the rest of your serverless function code ...

# ── Config ──────────────────────────────────────────────────────────────
API_KEY = "aNQojwGzi6K6FI8x9Mpl"
PROJECT_NAME = "fruits-and-vegetables-yz9mm"
MODEL_VERSION = 1
CONFIDENCE = 40
OVERLAP = 30
HOST = "0.0.0.0"
PORT = 8443

# ── Init Roboflow ───────────────────────────────────────────────────────
_fruit_model = None

def get_fruit_model():
    global _fruit_model
    if _fruit_model is None:
        print("[*] Loading Roboflow models...")
        rf = Roboflow(api_key=API_KEY)
        print("  -> Loading Fruit Model...")
        fruit_project = rf.workspace().project(PROJECT_NAME)
        _fruit_model = fruit_project.version(MODEL_VERSION).model
        print("[OK] Models loaded successfully!")
    return _fruit_model

# ── FastAPI App ─────────────────────────────────────────────────────────
app = FastAPI(title="Fruit & Vegetable Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_dir = Path(__file__).parent / "static"
# Removed static_dir.mkdir(exist_ok=True) as Vercel filesystem is read-only
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = static_dir / "index.html"
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))


@app.post("/api/detect")
async def detect_objects(file: UploadFile = File(...)):
    """Receive an image, run detection, return predictions as JSON."""
    contents = await file.read()
    if not contents:
        return JSONResponse({"error": "Empty image"}, status_code=400)

    # Save temp file for Roboflow API
    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "_temp_upload.jpg")
    with open(temp_path, "wb") as f:
        f.write(contents)

    try:
        active_model = get_fruit_model()
        prediction = active_model.predict(
            temp_path,
            confidence=CONFIDENCE,
            overlap=OVERLAP,
        ).json()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # Build clean response
    detections = []
    for pred in prediction.get("predictions", []):
        x = pred["x"]
        y = pred["y"]
        w = pred["width"]
        h = pred["height"]
        detections.append({
            "class": pred["class"],
            "confidence": round(pred["confidence"], 3),
            "x1": int(x - w / 2),
            "y1": int(y - h / 2),
            "x2": int(x + w / 2),
            "y2": int(y + h / 2),
            "width": int(w),
            "height": int(h),
        })

    return {
        "image_width": prediction.get("image", {}).get("width", 0),
        "image_height": prediction.get("image", {}).get("height", 0),
        "detections": detections,
        "count": len(detections),
    }


@app.post("/api/detect-frame")
async def detect_frame(file: UploadFile = File(...)):
    """Same as detect but optimised for camera frames (smaller response)."""
    return await detect_objects(file=file)


# ── Helpers ─────────────────────────────────────────────────────────────
def get_local_ip():
    """Get the local network IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_self_signed_cert():
    """Generate a self-signed SSL certificate for HTTPS."""
    cert_dir = Path(__file__).parent / "certs"
    cert_dir.mkdir(exist_ok=True)
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"

    if cert_file.exists() and key_file.exists():
        return str(cert_file), str(key_file)

    local_ip = get_local_ip()

    # Try using the 'cryptography' library first (pure Python, no openssl binary needed)
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime, ipaddress

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
        ])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.IPAddress(ipaddress.IPv4Address(local_ip)),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                ]),
                critical=False,
            )
            .sign(key, hashes.SHA256())
        )

        key_file.write_bytes(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
        cert_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        print("[OK] SSL certificate generated (cryptography lib)")
        return str(cert_file), str(key_file)

    except ImportError:
        pass

    # Fallback: use openssl binary with empty config
    from subprocess import run as sp_run
    empty_cnf = cert_dir / "openssl.cnf"
    empty_cnf.write_text("[req]\ndistinguished_name=dn\n[dn]\n", encoding="utf-8")
    env = os.environ.copy()
    env["OPENSSL_CONF"] = str(empty_cnf)
    sp_run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", str(key_file),
        "-out", str(cert_file),
        "-days", "365",
        "-nodes",
        "-subj", f"/CN={local_ip}",
        "-addext", f"subjectAltName=IP:{local_ip},IP:127.0.0.1",
    ], check=True, env=env)
    print("[OK] SSL certificate generated (openssl)")
    return str(cert_file), str(key_file)


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    local_ip = get_local_ip()

    try:
        cert_file, key_file = generate_self_signed_cert()
        print(f"\n{'='*60}")
        print(f"  Fruit & Vegetable Detector")
        print(f"{'='*60}")
        print(f"  Local:   https://localhost:{PORT}")
        print(f"  Phone:   https://{local_ip}:{PORT}")
        print(f"{'='*60}")
        print(f"  NOTE: On your phone, accept the self-signed certificate warning")
        print(f"{'='*60}\n")

        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            ssl_certfile=cert_file,
            ssl_keyfile=key_file,
            log_level="info",
        )
    except FileNotFoundError:
        # OpenSSL not found, fall back to HTTP
        print(f"\n{'='*60}")
        print(f"  Fruit & Vegetable Detector (HTTP mode)")
        print(f"{'='*60}")
        print(f"  WARNING: OpenSSL not found - running in HTTP mode")
        print(f"  WARNING: Camera may not work on phone (requires HTTPS)")
        print(f"  Local:   http://localhost:{PORT}")
        print(f"  Phone:   http://{local_ip}:{PORT}")
        print(f"{'='*60}\n")

        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            log_level="info",
        )
