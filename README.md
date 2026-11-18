<div align="center">

# rag-smoke-local

**Smoke del workspace de labs** · Angel Salazar

`¿están todos los repos vivos y con estructura mínima?`

</div>

---

### `$ whoami`

```text
antes de evaluar métricas: verificar que el laboratorio completo existe
sin cloud · sin red · solo filesystem + convenciones
```

---

### `$ ./smoke.sh`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m rag_smoke --workspace ..
```

---

Hecho en Lima · Angel Salazar · CIP 404730
