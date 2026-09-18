import os
import time
import uuid
import yaml
import pdfplumber
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MANIFEST_PATH = "pkc_manifest.yml"
WATCH_DIR = "zotero_attachments"

class ZoteroAttachmentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".pdf"):
            print(f"[INGESTION] New PDF detected: {event.src_path}")
            self.process_pdf(event.src_path)

    def process_pdf(self, filepath):
        try:
            # 1. Extract Text & Metadata
            text_preview = ""
            with pdfplumber.open(filepath) as pdf:
                if len(pdf.pages) > 0:
                     text_preview = pdf.pages[0].extract_text()[:500]

            # (Mock step 2: Extract arguments and relationships using local model)
            filename = os.path.basename(filepath)
            print(f"Extracted preview for {filename}: {text_preview[:50]}...")

            # 3. Serialize into YAML manifest
            self.update_manifest(filename)

        except Exception as e:
            print(f"[ERROR] Failed to process {filepath}: {e}")

    def update_manifest(self, filename):
        try:
            with open(MANIFEST_PATH, 'r') as f:
                manifest = yaml.safe_load(f)

            # Create a new node
            new_node = {
                "node_uuid": f"urn:uuid:{uuid.uuid4()}",
                "title": f"Auto-Ingested: {filename}",
                "content_path": f"pkm/auto_{filename}.md",
                "node_type": "PDF_Atom",
                "status": "transient",
                "version_number": 1,
                "epistemic_tag": "hypothetical",
                "meaning_space_anchor": {
                    "prototypical_vector": [0.0] * 5,  # Placeholder
                    "hyperspherical_radius": 0.1,
                    "embedding_model": "local-llama-3-8b"
                },
                "metadata_fields": {
                     "epistemic_risk_level": "Unknown",
                     "architectural_layer": "Raw_Ingest"
                }
            }

            if 'content_nodes' not in manifest:
                manifest['content_nodes'] = []
            manifest['content_nodes'].append(new_node)

            with open(MANIFEST_PATH, 'w') as f:
                yaml.safe_dump(manifest, f, default_flow_style=False)

            # Create a placeholder markdown file for the new node
            with open(f"pkm/auto_{filename}.md", 'w') as f:
                f.write(f"# Auto-Ingested Context for {filename}\n\nReview pending.")

            print(f"[SUCCESS] Appended new node to {MANIFEST_PATH} for {filename}")

        except Exception as e:
            print(f"[ERROR] Failed to update manifest: {e}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)
        print(f"Created watch directory: {WATCH_DIR}")

    event_handler = ZoteroAttachmentHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()

    print(f"[*] Zotero Ingestion Loop active. Watching '{WATCH_DIR}' for new PDFs...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("[*] Ingestion Loop stopped.")
    observer.join()
