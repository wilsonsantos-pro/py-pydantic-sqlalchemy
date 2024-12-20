## Template for a main SQLAlchemy model class
% for _import in imports:
from ${_import.package} import ${_import.name}
% endfor
% for _global_def in global_defs:
${_global_def}
% endfor
% for model in models:
<%
base_model = ",".join(b.name for b in model.model_bases)
%>
class ${model.class_name}(${base_model}):
    __tablename__ = "${model.table_name}"\

% for column in model.columns:
<% code_str = ""
extra_kwargs = ""
type_args = ""
if column.foreign_key:
    extra_kwargs += f', ForeignKey("{column.related_table.lower()}.id")'
if column.primary_key:
    extra_kwargs += ", primary_key=True"
if column.type_definition.nullable:
    extra_kwargs += ", nullable=True"
else:
    extra_kwargs += ", nullable=False"
if column.type_definition.type_args:
  type_args = f"({column.type_definition.type_args})"
code_str += f"{column.type_definition.type}{type_args}{extra_kwargs}"
%>
    ${column.name} = Column(${code_str})\
% endfor ## columns
% if include_relationships:
% for relationship_name, relationship_def in model.relationships.items():
    ${relationship_name} = relationship(${relationship_def.lower()})\
% endfor ## relationships
% endif

% endfor  ## model

