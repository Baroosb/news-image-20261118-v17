#!/usr/bin/env python3
import os
import sys
import stat
import hashlib
from pathlib import Path

EXPECTED_BYTES = 266519
EXPECTED_SHA256 = "28994209dd03e3822abfc119673890fd43ced6a383b19c4316665c7c7dd4327e"

def parse_jpeg_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 2 or data[0] != 0xFF or data[1] != 0xD8:
        raise SystemExit("Error: Invalid JPEG: Missing SOI marker")
    
    if len(data) < 4 or data[-2] != 0xFF or data[-1] != 0xD9:
        raise SystemExit("Error: Invalid JPEG: Missing EOI marker")
    
    i = 2
    n = len(data)
    width = None
    height = None
    
    while i < n - 1:
        if data[i] != 0xFF:
            raise SystemExit(f"Error: Invalid JPEG: Expected marker at offset {i}, got 0x{data[i]:02X}")
        
        # Skip padding 0xFF bytes
        while i < n and data[i] == 0xFF:
            i += 1
        if i >= n:
            break
            
        marker = data[i]
        i += 1
        
        # Standalone markers without length
        if marker in (0xD8, 0xD9, 0x01) or (0xD0 <= marker <= 0xD7):
            continue
            
        if i + 2 > n:
            raise SystemExit("Error: Invalid JPEG: Unexpected end of data reading segment length")
            
        seg_len = (data[i] << 8) | data[i+1]
        if seg_len < 2:
            raise SystemExit(f"Error: Invalid JPEG: Invalid segment length {seg_len}")
            
        # SOF0 (0xC0) or SOF2 (0xC2)
        if marker in (0xC0, 0xC2):
            if i + 7 > n:
                raise SystemExit("Error: Invalid JPEG: Segment too short for SOF0/SOF2")
            # height is 2 bytes at offset i+3, width is 2 bytes at offset i+5
            height = (data[i+3] << 8) | data[i+4]
            width = (data[i+5] << 8) | data[i+6]
            break
            
        i += seg_len
        
    if width is None or height is None:
        raise SystemExit("Error: Invalid JPEG: Could not find SOF0/SOF2 segment for dimensions")
        
    if width > 1024 or height > 1024:
        raise SystemExit(f"Error: Dimensions {width}x{height} exceed maximum allowed dimension of 1024")
        
    return width, height

def main():
    path = Path(__file__).parent / "frontpage.jpg"
    if not path.is_file():
        raise SystemExit(f"Error: frontpage.jpg not found at {path}")
        
    data = path.read_bytes()
    actual_bytes = len(data)
    if actual_bytes != EXPECTED_BYTES:
        raise SystemExit(f"Error: Byte length {actual_bytes} does not match expected {EXPECTED_BYTES}")
        
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != EXPECTED_SHA256:
        raise SystemExit(f"Error: SHA256 {actual_sha256} does not match expected {EXPECTED_SHA256}")
        
    width, height = parse_jpeg_dimensions(data)
    
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    output_dir = Path(output_dir_env) if output_dir_env else Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "entry.png"
    output_file.write_bytes(data)
    
    os.chmod(output_file, 0o644)
    
    written_data = output_file.read_bytes()
    written_bytes = len(written_data)
    written_sha256 = hashlib.sha256(written_data).hexdigest()
    
    if written_bytes != EXPECTED_BYTES or written_sha256 != EXPECTED_SHA256:
        raise SystemExit("Error: Re-read verification failed for written entry.png")
        
    if stat.S_IMODE(output_file.stat().st_mode) != 0o644:
        raise SystemExit(f"Error: File permissions are not 0o644")
        
    print(f"Successfully wrote entry.png: {width}x{height}, {written_bytes} bytes")

if __name__ == "__main__":
    main()
