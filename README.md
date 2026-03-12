# Master Level Pro (Tkinter)

Ye app aapke leveling calculation ke liye hai, jisme English/Hindi UI, shim thickness calculation aur PDF report export ka support hai.

## GitHub par kaise chalaye

GitHub website par desktop GUI app direct run nahi hoti (Tkinter ke liye local display chahiye).

Lekin GitHub par aap:
- Code host kar sakte ho
- CI check run kar sakte ho (included GitHub Action)
- Local machine par app run kar sakte ho

## Local run steps

1. Python 3.10+ install karein.
2. Repo clone karein:

```bash
git clone <your-repo-url>
cd SB
```

3. Dependency install karein:

```bash
pip install -r requirements.txt
```

4. App run karein:

```bash
python main.py
```

## Features

- Bilingual UI: English / Hindi
- Shim thickness calculation:

```text
shim = (error_reading * shim_distance) / level_length
```

- PDF report save and open

## Notes

- `tkinter` usually Python ke saath bundled aata hai.
- Agar PDF issue aaye to verify karein:

```bash
pip install fpdf2
```
