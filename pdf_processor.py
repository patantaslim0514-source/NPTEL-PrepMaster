import io
import re
from typing import Dict, Any, List
from pypdf import PdfReader

class PDFProcessor:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Extracts clean text, page-by-page mapping, and metadata from PDF bytes.
        """
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            total_pages = len(reader.pages)
            
            if total_pages == 0:
                raise ValueError("The uploaded PDF has no readable pages.")
            
            pages_data = []
            full_text_list = []
            
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                # Basic cleanup
                page_text_clean = re.sub(r'[\r\n]+', '\n', page_text).strip()
                if page_text_clean:
                    pages_data.append({
                        "page_number": idx + 1,
                        "text": page_text_clean,
                        "word_count": len(page_text_clean.split())
                    })
                    full_text_list.append(f"--- Page {idx + 1} ---\n{page_text_clean}")
            
            combined_text = "\n\n".join(full_text_list)
            total_words = sum(p["word_count"] for p in pages_data)
            
            # Simple heuristic for potential course/lecture title from first page
            detected_title = filename.replace(".pdf", "").replace("_", " ").title()
            if pages_data:
                first_lines = [l.strip() for l in pages_data[0]["text"].split("\n") if len(l.strip()) > 5]
                if first_lines:
                    # Look for something that looks like a title
                    candidate = first_lines[0]
                    if len(candidate) < 100:
                        detected_title = candidate
            
            # Estimate reading time (average 200 words per minute)
            read_time_mins = max(1, round(total_words / 200))
            
            return {
                "success": True,
                "filename": filename,
                "detected_title": detected_title,
                "total_pages": total_pages,
                "total_words": total_words,
                "estimated_read_time_mins": read_time_mins,
                "pages": pages_data,
                "full_text": combined_text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to parse PDF: {str(e)}"
            }

    @staticmethod
    def chunk_text(text: str, max_chars: int = 15000) -> List[str]:
        """
        Chunks text if it exceeds context limit.
        Gemini 2.5/1.5 has massive context (1M+ tokens), but chunking helps 
        for structured extraction if text is exceptionally large.
        """
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        paragraphs = text.split("\n\n")
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            if current_length + len(para) > max_chars and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_length = len(para)
            else:
                current_chunk.append(para)
                current_length += len(para)
                
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks
