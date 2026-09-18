# Vendored font support

The active manuscript uses WileyNJDv5 with `HARVARD,Utopia2COL`. The corresponding local typography support is organized here:

```text
paper/vendor/fonts/
├── utopia/
│   ├── README.md
│   └── upstream/
│       ├── utopia.zip
│       └── psnfss.zip
└── mathastext/
    ├── README.md
    └── upstream/
        ├── README.md
        ├── mathastext.dtx
        └── mathastext.pdf
```

Do not unpack generated TeX files into Git. Use:

```powershell
python -m scripts.vendor_utopia_fonts
```

The generated local TeX tree lives under `paper/build/vendor_fonts/`, which is ignored by Git.
