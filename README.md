## TODO

[X] Imports: from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
[X] UUID support: Column(UUID(as_uuid=True))
[X] ARRAY support: Column(MutableList.as_mutable(ARRAY(Integer, dimensions=1)))

## Examples

```bash
python src/py_pydantic_sqlalchemy/main.py --parser-config config/parser_config.example.yaml workspace/pydantic_user.py workspace/sqla_user.py
```
