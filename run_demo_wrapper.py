import contextlib
import io
import sys

output_buffer = io.StringIO()
with contextlib.redirect_stdout(output_buffer):
    import run_demo

with open("demo_output_safe.txt", "w", encoding="utf-8") as f:
    f.write(output_buffer.getvalue())
